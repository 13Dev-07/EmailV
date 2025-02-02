"""Utilities for cache monitoring."""
from typing import Dict, Any
import time
import asyncio
from .dns_metrics import DNSMetricsCollector

async def _collect_redis_metrics(self) -> Dict[str, Any]:
    """Collect metrics from Redis cache."""
    try:
        info = await self.redis_client.info()
        keyspace = await self.redis_client.info("keyspace")
        
        hits = int(info.get("keyspace_hits", 0))
        misses = int(info.get("keyspace_misses", 0))
        total_ops = hits + misses
        
        metrics = {
            "hit_rate": hits / total_ops if total_ops > 0 else 0,
            "memory_used": int(info.get("used_memory", 0)),
            "total_connections": int(info.get("connected_clients", 0)),
            "evicted_keys": int(info.get("evicted_keys", 0)),
            "expired_keys": int(info.get("expired_keys", 0))
        }
        
        self._metrics["redis"] = metrics
        self._last_collection = time.time()
        return metrics
    except Exception as e:
        logger.error(f"Failed to collect Redis metrics: {str(e)}")
        return {}

async def collect_dns_metrics(dns_metrics: DNSMetricsCollector) -> Dict[str, Any]:
    """Collect metrics from DNS cache."""
    try:
        metrics = dns_metrics.metrics
        stats = metrics.get_stats()
        
        collected = {
            "hit_rate": stats.get("cache_hit_ratio", 0),
            "mean_resolution_time": stats.get("mean_resolution_time", 0),
            "parallel_resolution_ratio": stats.get("parallel_resolution_ratio", 0),
            "failure_rate": stats.get("failure_rate", 0),
            "total_operations": metrics.cache_hits + metrics.cache_misses,
            "active_resolutions": metrics.parallel_resolutions,
            "failed_resolutions": metrics.failed_resolutions
        }
        
        return collected
    except Exception as e:
        logger.error(f"Failed to collect DNS metrics: {str(e)}")
        return {}