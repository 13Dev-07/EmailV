"""Cache monitoring implementation."""
import time
from dataclasses import dataclass
from typing import Dict, Optional
import asyncio
import logging

from app.caching.redis_client import RedisClient
from app.config.redis_config import RedisSettings

logger = logging.getLogger(__name__)

@dataclass
class CacheMetrics:
    """Cache performance metrics."""
    hits: int = 0
    misses: int = 0
    total_keys: int = 0
    memory_used: float = 0.0  # in MB
    hit_rate: float = 0.0
    
class CacheMonitor:
    """Monitors cache performance and health across different caching systems."""
    
    def __init__(
        self, 
        redis_client: Optional[RedisClient] = None,
        settings: Optional[RedisSettings] = None,
        dns_cache: Optional['DNSCache'] = None,
        collection_interval: int = 60
    ):
        """Initialize cache monitor."""
        self.redis_client = redis_client
        self.settings = settings
        self.dns_cache = dns_cache
        self.collection_interval = collection_interval
        self._running = False
        self._metrics: Dict[str, CacheMetrics] = {}
        self._last_collection: Optional[float] = None
        self._dns_metrics: Optional[DNSMetricsCollector] = None
        if dns_cache:
            self._dns_metrics = dns_cache._metrics
        
    async def start_monitoring(self):
        """Start the monitoring process."""
        self._running = True
        while self._running:
            try:
                await self._collect_metrics()
                await asyncio.sleep(self.collection_interval)
            except Exception as e:
                logger.error(f"Error collecting cache metrics: {str(e)}")
                
    async def stop_monitoring(self):
        """Stop the monitoring process."""
        self._running = False
        
    async def _collect_metrics(self):
        """Collect cache performance metrics from all sources."""
        # Collect Redis metrics if configured
        if self.redis_client and self.settings:
            await self._collect_redis_metrics()
            
        # Collect DNS cache metrics if configured
        if self._dns_metrics:
            await self._collect_dns_metrics()
        try:
            client = self.redis_client.client
            info = client.info()
            
            current_metrics = CacheMetrics(
                hits=info.get('keyspace_hits', 0),
                misses=info.get('keyspace_misses', 0),
                total_keys=sum(db.get('keys', 0) for db in info.values() if isinstance(db, dict)),
                memory_used=info.get('used_memory', 0) / 1024 / 1024  # Convert to MB
            )
            
            # Calculate hit rate
            total_ops = current_metrics.hits + current_metrics.misses
            current_metrics.hit_rate = (
                current_metrics.hits / total_ops if total_ops > 0 else 0
            )
            
            self._metrics[time.time()] = current_metrics
            self._last_collection = time.time()
            
            # Log metrics
            logger.info(
                f"Cache metrics - Hit rate: {current_metrics.hit_rate:.2%}, "
                f"Total keys: {current_metrics.total_keys}, "
                f"Memory used: {current_metrics.memory_used:.2f}MB"
            )
            
            # Alert on low hit rate
            if current_metrics.hit_rate < 0.5 and total_ops > 1000:
                logger.warning(
                    f"Low cache hit rate detected: {current_metrics.hit_rate:.2%}"
                )
                
            # Alert on high memory usage
            if current_metrics.memory_used > 1024:  # 1GB
                logger.warning(
                    f"High cache memory usage: {current_metrics.memory_used:.2f}MB"
                )
                
        except Exception as e:
            logger.error(f"Failed to collect cache metrics: {str(e)}")
            raise