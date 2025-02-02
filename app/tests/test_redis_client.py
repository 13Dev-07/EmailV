"""Tests for Redis client implementation."""

import pytest
import redis
from unittest.mock import Mock, patch
from datetime import datetime
from app.caching.redis_client import RedisClient, RedisCacheManager

@pytest.fixture
def redis_client():
    return RedisClient(
        host="localhost",
        port=6379,
        db=0
    )

@pytest.fixture
def cache_manager(redis_client):
    return RedisCacheManager(redis_client)

def test_set_cache(redis_client):
    with patch('redis.Redis.set') as mock_set:
        mock_set.return_value = True
        
        result = redis_client.set_cache(
            "test_key",
            "test_value",
            expire_in=60
        )
        
        assert result is True
        mock_set.assert_called_once()

def test_get_cache(redis_client):
    with patch('redis.Redis.get') as mock_get:
        mock_get.return_value = '"cached_value"'
        
        result = redis_client.get_cache("test_key")
        
        assert result == "cached_value"
        mock_get.assert_called_once_with("test_key")

@pytest.mark.asyncio
async def test_rate_limit(redis_client):
    mock_pipeline = Mock()
    mock_pipeline.execute.return_value = [1, 1, 5, 1]  # zremrangebyscore, zadd, zcard, expire
    
    with patch('aioredis.Redis.pipeline') as mock_pipeline_creator:
        mock_pipeline_creator.return_value = mock_pipeline
        
        is_allowed, remaining = await redis_client.rate_limit(
            "test_key",
            limit=10,
            window=60
        )
        
        assert is_allowed is True
        assert remaining == 5

def test_cache_decorator(cache_manager):
    # Test function to cache
    @cache_manager.cache_result(expire_in=60)
    def test_func(arg1, arg2):
        return f"{arg1}:{arg2}"
    
    with patch('app.caching.redis_client.RedisClient.get_cache') as mock_get:
        with patch('app.caching.redis_client.RedisClient.set_cache') as mock_set:
            # First call - cache miss
            mock_get.return_value = None
            result1 = test_func("a", "b")
            
            assert result1 == "a:b"
            mock_set.assert_called_once()
            
            # Second call - cache hit
            mock_get.return_value = "a:b"
            result2 = test_func("a", "b")
            
            assert result2 == "a:b"
            assert mock_set.call_count == 1  # Should not set cache again

@pytest.mark.asyncio
async def test_cache_decorator_async(cache_manager):
    # Test async function to cache
    @cache_manager.cache_result_async(expire_in=60)
    async def test_func_async(arg1, arg2):
        return f"{arg1}:{arg2}"
    
    with patch('app.caching.redis_client.RedisClient.get_cache') as mock_get:
        with patch('app.caching.redis_client.RedisClient.set_cache') as mock_set:
            # First call - cache miss
            mock_get.return_value = None
            result1 = await test_func_async("a", "b")
            
            assert result1 == "a:b"
            mock_set.assert_called_once()
            
            # Second call - cache hit
            mock_get.return_value = "a:b"
            result2 = await test_func_async("a", "b")
            
            assert result2 == "a:b"
            assert mock_set.call_count == 1  # Should not set cache again