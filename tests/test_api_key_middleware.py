"""Unit tests for API key middleware."""

import pytest
from unittest.mock import Mock, patch
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from app.api_key_manager import APIKeyManager
from app.middleware.api_key_middleware import APIKeyMiddleware

@pytest.fixture
async def api_key_manager():
    manager = APIKeyManager()
    return manager

@pytest.fixture
def app(api_key_manager):
    app = FastAPI()
    app.add_middleware(APIKeyMiddleware, api_key_manager=api_key_manager)
    
    @app.get("/test")
    async def test_endpoint():
        return {"status": "ok"}
        
    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}
    
    return app

@pytest.fixture
def client(app):
    return TestClient(app)

async def test_valid_api_key(client, api_key_manager):
    """Test request with valid API key."""
    # Create a test key
    key_data = await api_key_manager.create_key("test-client", ["read"])
    
    # Make request with key
    response = client.get(
        "/test",
        headers={"Authorization": f"Bearer {key_data['api_key']}"}
    )
    
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

async def test_invalid_api_key(client):
    """Test request with invalid API key."""
    response = client.get(
        "/test",
        headers={"Authorization": "Bearer invalid-key"}
    )
    
    assert response.status_code == 401
    assert "Invalid API key" in response.json()["error"]

async def test_missing_api_key(client):
    """Test request without API key."""
    response = client.get("/test")
    
    assert response.status_code == 401
    assert "API key missing" in response.json()["error"]

async def test_skip_auth_paths(client):
    """Test paths that should skip authentication."""
    response = client.get("/health")
    
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

async def test_different_key_formats(client, api_key_manager):
    """Test different API key formats."""
    key_data = await api_key_manager.create_key("test-client", ["read"])
    api_key = key_data["api_key"]
    
    # Test Bearer token
    response = client.get(
        "/test",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    assert response.status_code == 200
    
    # Test X-API-Key header
    response = client.get(
        "/test",
        headers={"X-API-Key": api_key}
    )
    assert response.status_code == 200
    
    # Test query parameter
    response = client.get(f"/test?api_key={api_key}")
    assert response.status_code == 200

async def test_invalid_scope(client, api_key_manager):
    """Test request with invalid scope."""
    # Create key with read scope only
    key_data = await api_key_manager.create_key("test-client", ["read"])
    
    # Try to use key for write operation
    response = client.post(
        "/test",
        headers={"Authorization": f"Bearer {key_data['api_key']}"}
    )
    
    assert response.status_code == 401