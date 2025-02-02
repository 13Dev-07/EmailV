"""Performance and load testing suite for email validation service."""
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
import pytest
from locust import HttpUser, task, between
from app.api.service import EmailValidationService
from app.cache import CacheManager

class LoadTestUser(HttpUser):
    """Simulates user behavior for load testing."""
    
    wait_time = between(1, 2.5)
    
    def on_start(self):
        """Setup before tests."""
        self.headers = {"Authorization": f"Bearer {self.environment.parsed_options.api_key}"}
    
    @task(3)
    def validate_single_email(self):
        """Test single email validation performance."""
        self.client.post(
            "/validate",
            json={"email": "test@example.com"},
            headers=self.headers
        )
    
    @task(1)
    def validate_batch_emails(self):
        """Test batch email validation performance."""
        self.client.post(
            "/validate/batch",
            json={
                "emails": [
                    f"test{i}@example.com" for i in range(10)
                ]
            },
            headers=self.headers
        )

@pytest.mark.benchmark
class TestPerformance:
    """Performance benchmarking test suite."""
    
    @pytest.fixture
    def validation_service(self):
        """Create validation service instance."""
        return EmailValidationService()
    
    def test_single_validation_performance(self, validation_service, benchmark):
        """Benchmark single email validation."""
        def validate():
            return validation_service.validate_email("test@example.com")
        
        result = benchmark(validate)
        assert result["is_valid"] is not None
        assert benchmark.stats["mean"] < 0.1  # Mean time should be under 100ms
    
    def test_batch_validation_performance(self, validation_service, benchmark):
        """Benchmark batch email validation."""
        emails = [f"test{i}@example.com" for i in range(100)]
        
        def validate_batch():
            return validation_service.validate_batch(emails)
        
        result = benchmark(validate_batch)
        assert len(result["results"]) == 100
        assert benchmark.stats["mean"] < 2.0  # Mean time should be under 2s
    
    @pytest.mark.asyncio
    async def test_concurrent_validation_performance(self, validation_service):
        """Test performance under concurrent load."""
        start_time = time.time()
        
        async def validate_email(email):
            return await validation_service.validate_email_async(email)
        
        # Create 50 concurrent validation tasks
        emails = [f"test{i}@example.com" for i in range(50)]
        tasks = [validate_email(email) for email in emails]
        results = await asyncio.gather(*tasks)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        assert len(results) == 50
        assert total_time < 5.0  # Should complete within 5 seconds
        
    def test_cache_performance(self, validation_service, redis_client):
        """Test caching performance."""
        email = "cache-test@example.com"
        
        # First request (uncached)
        start_time = time.time()
        validation_service.validate_email(email)
        uncached_time = time.time() - start_time
        
        # Second request (cached)
        start_time = time.time()
        validation_service.validate_email(email)
        cached_time = time.time() - start_time
        
        assert cached_time < uncached_time / 2  # Cached should be at least 2x faster
    
    def test_high_throughput_performance(self, validation_service):
        """Test performance under high throughput."""
        def worker(emails):
            return [validation_service.validate_email(email) for email in emails]
        
        # Create 1000 emails split across 4 threads
        all_emails = [f"test{i}@example.com" for i in range(1000)]
        chunk_size = len(all_emails) // 4
        email_chunks = [
            all_emails[i:i + chunk_size]
            for i in range(0, len(all_emails), chunk_size)
        ]
        
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(worker, email_chunks))
        total_time = time.time() - start_time
        
        # Flatten results
        all_results = [item for sublist in results for item in sublist]
        
        assert len(all_results) == 1000
        assert total_time < 20.0  # Should complete within 20 seconds
        
    def test_dns_cache_performance(self, validation_service):
        """Test DNS resolution caching performance."""
        email = "dns-test@gmail.com"
        
        # First request (uncached DNS)
        start_time = time.time()
        validation_service.validate_email(email)
        uncached_time = time.time() - start_time
        
        # Second request (cached DNS)
        start_time = time.time()
        validation_service.validate_email(email)
        cached_time = time.time() - start_time
        
        assert cached_time < uncached_time  # Cached should be faster