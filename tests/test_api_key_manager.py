"""Unit tests for API key management system."""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from app.api_key_manager import APIKeyManager

@pytest.fixture
async def key_manager():
    manager = APIKeyManager(
        rotation_interval=3600,  # 1 hour for testing
        max_keys_per_client=2
    )
    return manager

async def test_create_key(key_manager):
    """Test API key creation."""
    client_id = "test-client"
    scopes = ["read", "write"]
    
    key_data = await key_manager.create_key(client_id, scopes)
    
    assert key_data["client_id"] == client_id
    assert key_data["scopes"] == scopes
    assert key_data["is_active"] is True
    assert isinstance(key_data["created_at"], datetime)

async def test_max_keys_limit(key_manager):
    """Test maximum keys per client limit."""
    client_id = "test-client"
    
    # Create max allowed keys
    await key_manager.create_key(client_id)
    await key_manager.create_key(client_id)
    
    # Attempt to create one more
    with pytest.raises(ValueError, match="Maximum number of keys reached"):
        await key_manager.create_key(client_id)

async def test_rotate_key(key_manager):
    """Test API key rotation."""
    client_id = "test-client"
    key_data = await key_manager.create_key(client_id)
    original_key = key_data["api_key"]
    
    # Rotate the key
    rotated = await key_manager.rotate_key(key_data["key_id"])
    
    assert rotated["api_key"] != original_key
    assert isinstance(rotated["rotated_at"], datetime)

async def test_validate_key(key_manager):
    """Test API key validation."""
    client_id = "test-client"
    scopes = ["read", "write"]
    
    key_data = await key_manager.create_key(client_id, scopes)
    
    # Test valid key and scopes
    assert await key_manager.validate_key(key_data["api_key"], ["read"])
    assert await key_manager.validate_key(key_data["api_key"], ["write"])
    
    # Test invalid scope
    assert not await key_manager.validate_key(key_data["api_key"], ["admin"])
    
    # Test invalid key
    assert not await key_manager.validate_key("invalid-key")

async def test_deactivate_key(key_manager):
    """Test API key deactivation."""
    client_id = "test-client"
    key_data = await key_manager.create_key(client_id)
    
    # Deactivate the key
    await key_manager.deactivate_key(key_data["key_id"])
    
    # Key should not validate
    assert not await key_manager.validate_key(key_data["api_key"])
    
    # Client should have no active keys
    client_keys = await key_manager.get_client_keys(client_id)
    assert len(client_keys) == 0

async def test_cleanup_expired_keys(key_manager):
    """Test cleanup of expired keys."""
    client_id = "test-client"
    key_data = await key_manager.create_key(client_id)
    
    # Modify creation time to make key expired
    key_manager._keys[key_data["key_id"]]["created_at"] = \
        datetime.utcnow() - timedelta(hours=48)
    
    # Run cleanup
    await key_manager.cleanup_expired_keys()
    
    # Key should be deactivated
    assert not await key_manager.validate_key(key_data["api_key"])
    
async def test_get_client_keys(key_manager):
    """Test retrieving client keys."""
    client_id = "test-client"
    key1 = await key_manager.create_key(client_id)
    key2 = await key_manager.create_key(client_id)
    
    client_keys = await key_manager.get_client_keys(client_id)
    
    assert len(client_keys) == 2
    assert key1["key_id"] in [k["key_id"] for k in client_keys]
    assert key2["key_id"] in [k["key_id"] for k in client_keys]