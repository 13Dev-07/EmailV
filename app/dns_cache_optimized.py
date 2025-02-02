"""Optimized DNS caching implementation with improved concurrency."""
import threading
import time
import uuid
from typing import Dict, List, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
from dataclasses import dataclass
from dns.resolver import DNSRecord
from monitoring.dns_metrics import DNSMetricsCollector

@dataclass
class CacheEntry:
    """Cache entry containing DNS records and expiration time."""
    records: List[DNSRecord]
    expiry: float

class DNSCache:
    """Thread-safe DNS cache implementation with improved concurrency."""
    
    def __init__(self, default_ttl: int = 300, num_shards: int = 16):
        self._shards = [dict() for _ in range(num_shards)]
        self._locks = [threading.Lock() for _ in range(num_shards)]
        self._default_ttl = default_ttl
        self._executor = ThreadPoolExecutor(max_workers=4)
        self._metrics = DNSMetricsCollector()
        
    def _get_shard(self, domain: str) -> int:
        """Get the shard index for a domain using consistent hashing."""
        return hash(domain) % len(self._shards)
        
    def get(self, domain: str) -> Optional[List[DNSRecord]]:
        """Get DNS records for a domain from cache if available and not expired."""
        operation_id = str(uuid.uuid4())
        self._metrics.start_operation(operation_id)
        shard_idx = self._get_shard(domain)
        lock_start = time.time()
        with self._locks[shard_idx]:
            self._metrics.record_lock_contention(time.time() - lock_start)
            if domain in self._shards[shard_idx]:
                entry = self._shards[shard_idx][domain]
                if entry.expiry > time.time():
                    self._metrics.record_hit(operation_id, shard_idx)
                    return entry.records
                else:
                    del self._shards[shard_idx][domain]
            self._metrics.record_miss(operation_id, shard_idx)
            return None
            
    def set(self, domain: str, records: List[DNSRecord], ttl: Optional[int] = None) -> None:
        """Store DNS records in cache with TTL."""
        ttl = ttl or self._default_ttl
        expiry = time.time() + ttl
        shard_idx = self._get_shard(domain)
        with self._locks[shard_idx]:
            self._shards[shard_idx][domain] = CacheEntry(records=records, expiry=expiry)
            
    async def bulk_set(self, entries: Dict[str, Tuple[List[DNSRecord], Optional[int]]]) -> None:
        """Bulk store DNS records in cache with optional TTLs."""
        # Group entries by shard to minimize lock contention
        shard_entries = defaultdict(dict)
        for domain, (records, ttl) in entries.items():
            shard_idx = self._get_shard(domain)
            shard_entries[shard_idx][domain] = (records, ttl or self._default_ttl)
            
        # Update each shard
        for shard_idx, shard_data in shard_entries.items():
            with self._locks[shard_idx]:
                current_time = time.time()
                for domain, (records, ttl) in shard_data.items():
                    expiry = current_time + ttl
                    self._shards[shard_idx][domain] = CacheEntry(records=records, expiry=expiry)
                    
    async def get_missing_domains(self, domains: List[str]) -> List[str]:
        """Get list of domains not in cache or expired."""
        missing = []
        current_time = time.time()
        
        # Group domains by shard
        shard_domains = defaultdict(list)
        for domain in domains:
            shard_idx = self._get_shard(domain)
            shard_domains[shard_idx].append(domain)
            
        # Check each shard
        for shard_idx, domains_to_check in shard_domains.items():
            with self._locks[shard_idx]:
                for domain in domains_to_check:
                    if domain not in self._shards[shard_idx] or \
                       self._shards[shard_idx][domain].expiry <= current_time:
                        missing.append(domain)
        return missing
        
    def clear(self) -> None:
        """Clear all cached entries."""
        for idx in range(len(self._shards)):
            with self._locks[idx]:
                self._shards[idx].clear()
                
    def cleanup(self) -> None:
        """Remove expired entries from cache."""
        def clean_shard(idx: int) -> None:
            current_time = time.time()
            with self._locks[idx]:
                expired = [
                    domain for domain, entry in self._shards[idx].items()
                    if entry.expiry <= current_time
                ]
                for domain in expired:
                    del self._shards[idx][domain]
                    
        # Clean shards concurrently
        futures = [
            self._executor.submit(clean_shard, idx)
            for idx in range(len(self._shards))
        ]
        for future in futures:
            future.result()  # Wait for cleanup to complete