"""
PyTest configuration and fixtures.
"""

import pytest
import redis
from typing import Generator
from app.utils.cache_manager import CacheManager
from app.utils.redis_cache import RedisCache

@pytest.fixture
def redis_url() -> str:
    """Redis connection URL for testing."""
    return "redis://localhost:6379/0"

@pytest.fixture
def redis_client(redis_url: str) -> Generator[redis.Redis, None, None]:
    """Redis client fixture."""
    client = redis.from_url(redis_url)
    yield client
    # Cleanup after tests
    client.flushdb()
    client.close()

@pytest.fixture
def cache_manager(redis_url: str) -> Generator[CacheManager, None, None]:
    """Cache manager fixture."""
    manager = CacheManager(redis_url)
    yield manager
    # Cleanup cached data
    manager.invalidate_pattern("*")