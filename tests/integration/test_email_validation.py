"""Integration tests for the email validation service."""

import pytest
import asyncio
from typing import Dict, Any
import aiohttp
import aioredis
import os
from datetime import datetime

# Test configuration
TEST_API_URL = os.getenv("TEST_API_URL", "http://localhost:8000")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

@pytest.fixture(scope="module")
async def redis_client():
    client = await aioredis.create_redis_pool(REDIS_URL)
    yield client
    client.close()
    await client.wait_closed()

@pytest.fixture(scope="module")
async def http_client():
    async with aiohttp.ClientSession() as session:
        yield session

@pytest.mark.integration
class TestEmailValidation:
    """Integration tests for email validation endpoints."""

    @pytest.mark.asyncio
    async def test_validate_email_success(self, http_client):
        """Test successful email validation."""
        async with http_client.post(
            f"{TEST_API_URL}/validate",
            json={"email": "test@gmail.com"}
        ) as response:
            assert response.status == 200
            data = await response.json()
            assert data["is_valid"] is True

    @pytest.mark.asyncio
    async def test_validate_email_invalid(self, http_client):
        """Test validation of invalid email."""
        async with http_client.post(
            f"{TEST_API_URL}/validate",
            json={"email": "invalid-email"}
        ) as response:
            assert response.status == 400
            data = await response.json()
            assert data["is_valid"] is False
            assert "error" in data

    @pytest.mark.asyncio
    async def test_rate_limiting(self, http_client):
        """Test rate limiting functionality."""
        # Make multiple requests quickly
        responses = []
        for _ in range(10):
            async with http_client.post(
                f"{TEST_API_URL}/validate",
                json={"email": "test@example.com"}
            ) as response:
                responses.append(response.status)

        # Should see some 429 (Too Many Requests) responses
        assert 429 in responses

    @pytest.mark.asyncio
    async def test_caching_behavior(self, http_client, redis_client):
        """Test that results are properly cached."""
        test_email = "cache-test@example.com"
        
        # First request
        t1 = datetime.now()
        async with http_client.post(
            f"{TEST_API_URL}/validate",
            json={"email": test_email}
        ) as response1:
            await response1.json()

        # Second request (should be faster due to caching)
        t2 = datetime.now()
        async with http_client.post(
            f"{TEST_API_URL}/validate",
            json={"email": test_email}
        ) as response2:
            await response2.json()

        # Verify faster response time for cached result
        assert (t2 - t1).total_seconds() > (datetime.now() - t2).total_seconds()

    @pytest.mark.asyncio
    async def test_metrics_endpoint(self, http_client):
        """Test that metrics endpoint is working."""
        async with http_client.get(f"{TEST_API_URL}/metrics") as response:
            assert response.status == 200
            text = await response.text()
            assert "email_validation_requests_total" in text

    @pytest.mark.asyncio
    async def test_health_check(self, http_client):
        """Test health check endpoint."""
        async with http_client.get(f"{TEST_API_URL}/health") as response:
            assert response.status == 200
            data = await response.json()
            assert data["status"] == "healthy"
            assert "version" in data

    @pytest.mark.asyncio
    async def test_parallel_requests(self, http_client):
        """Test handling of parallel validation requests."""
        async def make_request(email: str) -> Dict[str, Any]:
            async with http_client.post(
                f"{TEST_API_URL}/validate",
                json={"email": email}
            ) as response:
                return await response.json()

        # Make multiple requests in parallel
        emails = [f"test{i}@example.com" for i in range(5)]
        tasks = [make_request(email) for email in emails]
        results = await asyncio.gather(*tasks)

        # Verify all requests completed successfully
        assert len(results) == 5
        assert all("is_valid" in result for result in results)

    @pytest.mark.asyncio
    async def test_input_sanitization(self, http_client):
        """Test input sanitization and security checks."""
        malicious_inputs = [
            {"email": "test@example.com<script>alert(1)</script>"},
            {"email": "admin@example.com; DROP TABLE users;"},
            {"email": "test@example.com' OR '1'='1"}
        ]

        for payload in malicious_inputs:
            async with http_client.post(
                f"{TEST_API_URL}/validate",
                json=payload
            ) as response:
                assert response.status == 400
                data = await response.json()
                assert not data["is_valid"]
                assert "security" in data["error"].lower()