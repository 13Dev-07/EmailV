"""Enhanced cache management with intelligent invalidation strategies."""

import time
from typing import Any, Dict, Optional, Set, Tuple
import logging
from prometheus_client import Counter, Gauge, Histogram
import asyncio
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# Cache metrics
CACHE_HITS = Counter(
    'cache_hits_total',
    'Number of cache hits',
    ['cache_type']
)

CACHE_MISSES = Counter(
    'cache_misses_total',
    'Number of cache misses',
    ['cache_type']
)

CACHE_SIZE = Gauge(
    'cache_size_bytes',
    'Size of cache in bytes',
    ['cache_type']
)

CACHE_ITEMS = Gauge(
    'cache_items',
    'Number of items in cache',
    ['cache_type']
)

CACHE_INVALIDATIONS = Counter(
    'cache_invalidations_total',
    'Number of cache invalidations',
    ['cache_type', 'reason']
)

CACHE_AGE = Histogram(
    'cache_entry_age_seconds',
    'Age of cache entries when accessed',
    ['cache_type']
)

class CacheEntry:
    """Represents a single cache entry with metadata."""
    
    def __init__(self, key: str, value: Any, ttl: int = 3600):
        self.key = key
        self.value = value
        self.ttl = ttl
        self.created_at = time.time()
        self.last_accessed = time.time()
        self.access_count = 0
        self.size_bytes = len(str(value).encode())

    def is_expired(self) -> bool:
        """Check if the entry has expired."""
        return time.time() > self.created_at + self.ttl

    def access(self) -> None:
        """Record an access to this cache entry."""
        self.last_accessed = time.time()
        self.access_count += 1

class CacheManager:
    """Manages cache with intelligent invalidation strategies."""
    
    def __init__(
        self,
        cache_type: str,
        max_size_bytes: int = 1024 * 1024 * 100,  # 100MB
        max_items: int = 10000,
        cleanup_interval: int = 300,  # 5 minutes
        min_access_threshold: int = 5
    ):
        self.cache_type = cache_type
        self.max_size_bytes = max_size_bytes
        self.max_items = max_items
        self.cleanup_interval = cleanup_interval
        self.min_access_threshold = min_access_threshold
        
        self._cache: Dict[str, CacheEntry] = {}
        self._current_size_bytes = 0
        self._lock = asyncio.Lock()
        
        # Start background cleanup task
        self._cleanup_task = asyncio.create_task(self._cleanup_loop())
        
        # Initialize metrics
        CACHE_SIZE.labels(cache_type=cache_type).set(0)
        CACHE_ITEMS.labels(cache_type=cache_type).set(0)
    
    async def get(self, key: str) -> Optional[Any]:
        """Get a value from the cache."""
        async with self._lock:
            entry = self._cache.get(key)
            
            if entry is None:
                CACHE_MISSES.labels(cache_type=self.cache_type).inc()
                return None
            
            if entry.is_expired():
                await self._remove_entry(key)
                CACHE_MISSES.labels(cache_type=self.cache_type).inc()
                return None
            
            entry.access()
            CACHE_HITS.labels(cache_type=self.cache_type).inc()
            CACHE_AGE.labels(cache_type=self.cache_type).observe(
                time.time() - entry.created_at
            )
            return entry.value
    
    async def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        """Set a value in the cache."""
        entry = CacheEntry(key, value, ttl)
        
        async with self._lock:
            # If key exists, remove it first
            if key in self._cache:
                await self._remove_entry(key)
            
            # Check if we need to make space
            if (
                self._current_size_bytes + entry.size_bytes > self.max_size_bytes or
                len(self._cache) >= self.max_items
            ):
                await self._evict_entries()
            
            self._cache[key] = entry
            self._current_size_bytes += entry.size_bytes
            
            # Update metrics
            CACHE_SIZE.labels(cache_type=self.cache_type).set(self._current_size_bytes)
            CACHE_ITEMS.labels(cache_type=self.cache_type).set(len(self._cache))
    
    async def invalidate(self, key: str) -> None:
        """Explicitly invalidate a cache entry."""
        async with self._lock:
            if key in self._cache:
                await self._remove_entry(key)
                CACHE_INVALIDATIONS.labels(
                    cache_type=self.cache_type,
                    reason="explicit"
                ).inc()
    
    async def _remove_entry(self, key: str) -> None:
        """Remove a cache entry and update metrics."""
        entry = self._cache.pop(key, None)
        if entry:
            self._current_size_bytes -= entry.size_bytes
            CACHE_SIZE.labels(cache_type=self.cache_type).set(self._current_size_bytes)
            CACHE_ITEMS.labels(cache_type=self.cache_type).set(len(self._cache))
    
    async def _evict_entries(self) -> None:
        """Evict entries based on intelligent selection."""
        if not self._cache:
            return
        
        # Calculate scores for each entry
        scores: List[Tuple[str, float]] = []
        current_time = time.time()
        
        for key, entry in self._cache.items():
            # Score based on:
            # 1. Age (older = higher score)
            # 2. Access frequency (less accessed = higher score)
            # 3. Size (larger = higher score)
            age_factor = (current_time - entry.created_at) / entry.ttl
            access_factor = 1.0 / (entry.access_count + 1)
            size_factor = entry.size_bytes / self.max_size_bytes
            
            score = (age_factor * 0.4) + (access_factor * 0.4) + (size_factor * 0.2)
            scores.append((key, score))
        
        # Sort by score (highest first) and remove entries until we have space
        scores.sort(key=lambda x: x[1], reverse=True)
        
        for key, _ in scores[:len(scores) // 4]:  # Remove up to 25% of entries
            await self._remove_entry(key)
            CACHE_INVALIDATIONS.labels(
                cache_type=self.cache_type,
                reason="eviction"
            ).inc()
    
    async def _cleanup_loop(self) -> None:
        """Background task to clean up expired entries."""
        while True:
            try:
                await asyncio.sleep(self.cleanup_interval)
                await self._cleanup_expired()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in cache cleanup: {e}")
                await asyncio.sleep(60)  # Wait a minute before retrying
    
    async def _cleanup_expired(self) -> None:
        """Remove expired entries and entries below access threshold."""
        async with self._lock:
            current_time = time.time()
            threshold_time = current_time - self.cleanup_interval
            
            keys_to_remove = []
            for key, entry in self._cache.items():
                if entry.is_expired():
                    keys_to_remove.append(key)
                elif (
                    entry.last_accessed < threshold_time and
                    entry.access_count < self.min_access_threshold
                ):
                    keys_to_remove.append(key)
            
            for key in keys_to_remove:
                await self._remove_entry(key)
                CACHE_INVALIDATIONS.labels(
                    cache_type=self.cache_type,
                    reason="cleanup"
                ).inc()
    
    async def close(self) -> None:
        """Clean up resources."""
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass