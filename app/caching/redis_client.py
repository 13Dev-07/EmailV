"""Redis client module for caching and rate limiting."""

import redis
from typing import Optional, Any, Union
import json
import logging
from datetime import datetime, timedelta
import asyncio
from functools import wraps
import aioredis

logger = logging.getLogger(__name__)

class RedisClient:
    """Handles Redis operations for caching and rate limiting."""
    
    def __init__(
        self, 
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
        socket_timeout: float = 2.0,
        retry_on_timeout: bool = True,
        max_connections: int = 50,
        health_check_interval: int = 30
    ):
        """
        Initialize Redis client.
        
        Args:
            host: Redis server hostname.
            port: Redis server port.
            db: Redis database number.
            password: Redis password.
            socket_timeout: Socket timeout in seconds.
            retry_on_timeout: Whether to retry on timeout.
            max_connections: Maximum number of connections.
        """
        self.redis_pool = redis.ConnectionPool(
            host=host,
            port=port,
            db=db,
            password=password,
            socket_timeout=socket_timeout,
            retry_on_timeout=retry_on_timeout,
            max_connections=max_connections,
            health_check_interval=health_check_interval
        )
        
        self.async_pool = None
        self._initialize_async_pool_lock = asyncio.Lock()

    @property
    def client(self) -> redis.Redis:
        """Get Redis client from pool."""
        return redis.Redis(connection_pool=self.redis_pool)

    async def get_async_pool(self) -> aioredis.Redis:
        """Get or create async Redis connection pool."""
        if self.async_pool is None:
            async with self._initialize_async_pool_lock:
                if self.async_pool is None:
                    self.async_pool = await aioredis.create_redis_pool(
                        f'redis://{self.redis_pool.connection_kwargs["host"]}:'
                        f'{self.redis_pool.connection_kwargs["port"]}',
                        password=self.redis_pool.connection_kwargs.get("password"),
                        db=self.redis_pool.connection_kwargs["db"],
                        minsize=1,
                        maxsize=self.redis_pool.max_connections
                    )
        return self.async_pool

    def set_cache(
        self,
        key: str,
        value: Any,
        expire_in: int = 3600,
        nx: bool = False
    ) -> bool:
        """
        Set a cache value with expiration.
        
        Args:
            key: Cache key.
            value: Value to cache.
            expire_in: Expiration time in seconds.
            nx: Only set if key doesn't exist.
            
        Returns:
            True if value was set, False otherwise.
        """
        try:
            serialized = json.dumps(value)
            return bool(
                self.client.set(
                    key,
                    serialized,
                    ex=expire_in,
                    nx=nx
                )
            )
        except Exception as e:
            logger.error(f"Redis set error: {str(e)}")
            return False

    def get_cache(self, key: str) -> Optional[Any]:
        """
        Get a cached value.
        
        Args:
            key: Cache key.
            
        Returns:
            Cached value if found and not expired, None otherwise.
        """
        try:
            value = self.client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Redis get error: {str(e)}")
            return None

    async def rate_limit(
        self,
        key: str,
        limit: int,
        window: int
    ) -> tuple[bool, int]:
        """
        Check rate limit for a key.
        
        Args:
            key: Rate limit key.
            limit: Maximum number of requests.
            window: Time window in seconds.
            
        Returns:
            Tuple of (is_allowed, remaining_requests).
        """
        try:
            redis = await self.get_async_pool()
            
            pipeline = redis.pipeline()
            now = datetime.now().timestamp()
            
            # Remove old entries
            pipeline.zremrangebyscore(
                key,
                0,
                now - window
            )
            
            # Add current request
            pipeline.zadd(key, now, str(now))
            
            # Count requests in window
            pipeline.zcard(key)
            
            # Set expiration
            pipeline.expire(key, window)
            
            _, _, count, _ = await pipeline.execute()
            
            is_allowed = count <= limit
            remaining = max(0, limit - count)
            
            return is_allowed, remaining
            
        except Exception as e:
            logger.error(f"Rate limit error: {str(e)}")
            return True, limit  # Fail open

    def close(self):
        """Close Redis connections."""
        self.client.close()
        if self.async_pool:
            self.async_pool.close()

class RedisCacheManager:
    """Manages caching operations with Redis."""
    
    def __init__(self, redis_client: RedisClient):
        """
        Initialize cache manager.
        
        Args:
            redis_client: Redis client instance.
        """
        self.redis = redis_client

    def cache_result(
        self,
        expire_in: int = 3600,
        key_prefix: str = "",
        include_args: bool = True
    ):
        """
        Cache decorator for function results.
        
        Args:
            expire_in: Cache expiration time in seconds.
            key_prefix: Prefix for cache keys.
            include_args: Whether to include function arguments in cache key.
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Generate cache key
                if include_args:
                    key_parts = [key_prefix, func.__name__]
                    key_parts.extend(str(arg) for arg in args)
                    key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
                    cache_key = ":".join(key_parts)
                else:
                    cache_key = f"{key_prefix}:{func.__name__}"

                # Try to get from cache
                cached = self.redis.get_cache(cache_key)
                if cached is not None:
                    return cached

                # Execute function and cache result
                result = func(*args, **kwargs)
                self.redis.set_cache(cache_key, result, expire_in)
                return result

            return wrapper
        return decorator

    async def cache_result_async(
        self,
        expire_in: int = 3600,
        key_prefix: str = "",
        include_args: bool = True
    ):
        """
        Async cache decorator for coroutine results.
        
        Args:
            expire_in: Cache expiration time in seconds.
            key_prefix: Prefix for cache keys.
            include_args: Whether to include function arguments in cache key.
        """
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # Generate cache key
                if include_args:
                    key_parts = [key_prefix, func.__name__]
                    key_parts.extend(str(arg) for arg in args)
                    key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
                    cache_key = ":".join(key_parts)
                else:
                    cache_key = f"{key_prefix}:{func.__name__}"

                # Try to get from cache
                cached = await self.redis.get_cache(cache_key)
                if cached is not None:
                    return cached

                # Execute function and cache result
                result = await func(*args, **kwargs)
                await self.redis.set_cache(cache_key, result, expire_in)
                return result

            return wrapper
        return decorator