"""
Redis Cache Manager Module
Provides Redis-based caching functionality with monitoring and invalidation.
"""

import json
import redis
from typing import Any, Optional, Dict
from datetime import datetime
from prometheus_client import Counter, Histogram
from app.utils.metrics import CACHE_HITS, CACHE_MISSES, CACHE_LATENCY

class RedisCache:
    """Redis cache implementation with monitoring."""
    
    def __init__(self, redis_url: str):
        """
        Initialize Redis cache manager.
        
        Args:
            redis_url: Redis connection URL
        """
        self.client = redis.from_url(redis_url)
        
        # Setup metrics
        self.cache_hits = Counter('cache_hits_total', 'Cache hits by key type',
                              ['cache_type'])
        self.cache_misses = Counter('cache_misses_total', 'Cache misses by key type',
                                ['cache_type'])
        self.cache_latency = Histogram('cache_operation_latency_seconds',
                                   'Cache operation latency',
                                   ['operation'])
                                   
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache with monitoring.
        
        Args:
            key: Cache key to retrieve
            
        Returns:
            Cached value if found, None otherwise
        """
        cache_type = self._get_cache_type(key)
        start_time = datetime.now()
        
        try:
            value = self.client.get(key)
            
            if value is not None:
                self.cache_hits.labels(cache_type=cache_type).inc()
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    return value
            else:
                self.cache_misses.labels(cache_type=cache_type).inc()
                return None
                
        finally:
            duration = (datetime.now() - start_time).total_seconds()
            self.cache_latency.labels(operation='get').observe(duration)
            
    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """
        Set value in cache with TTL and monitoring.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds (default: 1 hour)
            
        Returns:
            bool: True if successful, False otherwise
        """
        start_time = datetime.now()
        
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            return bool(self.client.setex(key, ttl, value))
        finally:
            duration = (datetime.now() - start_time).total_seconds()
            self.cache_latency.labels(operation='set').observe(duration)
            
    def delete(self, key: str) -> bool:
        """
        Delete key from cache.
        
        Args:
            key: Cache key to delete
            
        Returns:
            bool: True if key was deleted, False otherwise
        """
        start_time = datetime.now()
        
        try:
            return bool(self.client.delete(key))
        finally:
            duration = (datetime.now() - start_time).total_seconds()
            self.cache_latency.labels(operation='delete').observe(duration)
            
    def invalidate_pattern(self, pattern: str) -> int:
        """
        Invalidate all keys matching pattern.
        
        Args:
            pattern: Redis key pattern to match
            
        Returns:
            int: Number of keys invalidated
        """
        keys = self.client.keys(pattern)
        if keys:
            return self.client.delete(*keys)
        return 0
        
    def get_stats(self) -> Dict[str, int]:
        """Get cache statistics."""
        return {
            "total_keys": len(self.client.keys("*")),
            "hits": sum(self.cache_hits._value.values()),
            "misses": sum(self.cache_misses._value.values()),
            "memory_used": self.client.info()["used_memory"],
            "peak_memory": self.client.info()["used_memory_peak"]
        }
        
    def _get_cache_type(self, key: str) -> str:
        """Extract cache type from key for metrics."""
        if ':' in key:
            return key.split(':')[0]
        return 'unknown'
        
    def health_check(self) -> bool:
        """
        Check if Redis connection is healthy.
        
        Returns:
            bool: True if healthy, False otherwise
        """
        try:
            return bool(self.client.ping())
        except Exception:
            return False