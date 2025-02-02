"""DNS caching implementation for improved performance."""

from typing import Dict, List, Optional
import time
import threading
from dataclasses import dataclass
from app.dns_resolver import DNSRecord

@dataclass
class CacheEntry:
    records: List[DNSRecord]
    expiry: float

class DNSCache:
    """Thread-safe DNS cache implementation."""
    
    def __init__(self, default_ttl: int = 300):  # 5 minutes default TTL
        self._cache: Dict[str, CacheEntry] = {}
        self._lock = threading.Lock()
        self._default_ttl = default_ttl
        
    def get(self, domain: str) -> Optional[List[DNSRecord]]:
        """Get DNS records for a domain from cache if available and not expired."""
        with self._lock:
            if domain in self._cache:
                entry = self._cache[domain]
                if entry.expiry > time.time():
                    return entry.records
                else:
                    del self._cache[domain]
            return None
            
    def set(self, domain: str, records: List[DNSRecord], ttl: Optional[int] = None) -> None:
        """Store DNS records in cache with TTL."""
        ttl = ttl or self._default_ttl
        expiry = time.time() + ttl
        with self._lock:
            self._cache[domain] = CacheEntry(records=records, expiry=expiry)
            
    async def bulk_set(self, entries: Dict[str, Tuple[List[DNSRecord], Optional[int]]]) -> None:
        """Store multiple DNS records in cache efficiently.
        
        Args:
            entries: Dictionary mapping domains to tuples of (records, ttl)
        """
        current_time = time.time()
        with self._lock:
            for domain, (records, ttl) in entries.items():
                ttl = ttl or self._default_ttl
                expiry = current_time + ttl
                self._cache[domain] = CacheEntry(records=records, expiry=expiry)
                
    async def get_missing_domains(self, domains: List[str]) -> List[str]:
        """Get list of domains that are not in cache or are expired.
        
        Args:
            domains: List of domains to check
            
        Returns:
            List of domains that need to be resolved
        """
        current_time = time.time()
        with self._lock:
            return [
                domain for domain in domains
                if domain not in self._cache or 
                self._cache[domain].expiry <= current_time
            ]
            
    def clear(self) -> None:
        """Clear all cached entries."""
        with self._lock:
            self._cache.clear()
            
    def cleanup(self) -> None:
        """Remove expired entries from cache."""
        current_time = time.time()
        with self._lock:
            expired = [
                domain for domain, entry in self._cache.items()
                if entry.expiry <= current_time
            ]
            for domain in expired:
                del self._cache[domain]

# Global DNS cache instance
dns_cache = DNSCache()