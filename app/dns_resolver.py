"""DNS resolution module for email validation."""

import dns.resolver
import dns.exception
from typing import List, Optional, Dict, Union
from dataclasses import dataclass
from datetime import datetime, timedelta
import asyncio
import socket
import threading
import logging
from contextlib import contextmanager

logger = logging.getLogger(__name__)

@dataclass
class DNSRecord:
    """Represents a DNS record with TTL-based expiration."""
    value: str
    record_type: str
    priority: Optional[int] = None
    expiration: Optional[datetime] = None

    @property
    def is_expired(self) -> bool:
        """Check if the record has expired."""
        return (self.expiration is not None and 
                datetime.now() > self.expiration)

class DNSCache:
    """Thread-safe cache for DNS records."""
    
    def __init__(self, default_ttl: int = 300):
        """
        Initialize DNS cache.
        
        Args:
            default_ttl: Default time-to-live in seconds for cached records.
        """
        self._cache: Dict[str, Dict[str, List[DNSRecord]]] = {}
        self._lock = threading.Lock()
        self.default_ttl = default_ttl

    @contextmanager
    def _locked_cache(self):
        """Thread-safe context manager for cache access."""
        with self._lock:
            yield self._cache

    def get(self, domain: str, record_type: str) -> Optional[List[DNSRecord]]:
        """
        Get cached DNS records for a domain and type.
        
        Args:
            domain: Domain name to look up.
            record_type: Type of DNS record (e.g., 'MX', 'A').
            
        Returns:
            List of DNSRecord objects if found and not expired, None otherwise.
        """
        with self._locked_cache() as cache:
            if domain not in cache or record_type not in cache[domain]:
                return None
            
            records = cache[domain][record_type]
            if any(record.is_expired for record in records):
                del cache[domain][record_type]
                if not cache[domain]:
                    del cache[domain]
                return None
                
            return records

    def set(self, domain: str, record_type: str, 
            records: List[Union[dns.rdtypes.ANY.MX.MX, dns.rdtypes.IN.A.A]],
            ttl: Optional[int] = None):
        """
        Cache DNS records for a domain.
        
        Args:
            domain: Domain name to cache.
            record_type: Type of DNS record.
            records: DNS records to cache.
            ttl: Time-to-live in seconds (uses default_ttl if None).
        """
        ttl = ttl or self.default_ttl
        expiration = datetime.now() + timedelta(seconds=ttl)
        
        with self._locked_cache() as cache:
            if domain not in cache:
                cache[domain] = {}
                
            dns_records = []
            for record in records:
                if record_type == 'MX':
                    dns_records.append(DNSRecord(
                        value=str(record.exchange),
                        record_type=record_type,
                        priority=record.preference,
                        expiration=expiration
                    ))
                else:
                    dns_records.append(DNSRecord(
                        value=str(record),
                        record_type=record_type,
                        expiration=expiration
                    ))
                    
            cache[domain][record_type] = dns_records

class DNSResolver:
    """Handles DNS resolution with caching and fallback support."""
    
    def __init__(self, timeout: float = 5.0, cache_ttl: int = 1800):
        """
        Initialize DNS resolver with optimized settings.
        
        Args:
            timeout: Timeout for DNS queries in seconds.
            cache_ttl: Time-to-live for cached records in seconds (default: 1800 - 30 minutes).
        """
        self.timeout = timeout
        self.cache = DNSCache(default_ttl=cache_ttl)
        self.resolver = dns.resolver.Resolver()
        self.resolver.timeout = timeout
        self.resolver.lifetime = timeout

    async def resolve_mx(self, domain: str) -> List[DNSRecord]:
        """
        Resolve MX records for a domain with fallback to A/AAAA records.
        
        Args:
            domain: Domain to resolve MX records for.
            
        Returns:
            List of DNSRecord objects.
            
        Raises:
            dns.exception.DNSException: If resolution fails.
        """
        # Check cache first
        cached_records = self.cache.get(domain, 'MX')
        if cached_records:
            return cached_records

        try:
            # Attempt MX record lookup
            answers = await self._async_resolve(domain, 'MX')
            if answers:
                self.cache.set(domain, 'MX', answers)
                return [DNSRecord(
                    value=str(answer.exchange),
                    record_type='MX',
                    priority=answer.preference
                ) for answer in answers]

        except dns.exception.DNSException as e:
            logger.warning(f"MX lookup failed for {domain}: {str(e)}")
            
            try:
                # Fallback to A record
                a_records = await self._async_resolve(domain, 'A')
                if a_records:
                    self.cache.set(domain, 'A', a_records)
                    return [DNSRecord(
                        value=str(record),
                        record_type='A'
                    ) for record in a_records]
                    
            except dns.exception.DNSException as e:
                logger.warning(f"A record lookup failed for {domain}: {str(e)}")
                
                try:
                    # Final fallback to AAAA record
                    aaaa_records = await self._async_resolve(domain, 'AAAA')
                    if aaaa_records:
                        self.cache.set(domain, 'AAAA', aaaa_records)
                        return [DNSRecord(
                            value=str(record),
                            record_type='AAAA'
                        ) for record in aaaa_records]
                        
                except dns.exception.DNSException as e:
                    logger.warning(f"AAAA record lookup failed for {domain}: {str(e)}")
                    raise

        return []

    async def _async_resolve(self, domain: str, record_type: str) -> List[Union[dns.rdtypes.ANY.MX.MX, dns.rdtypes.IN.A.A]]:
        """
        Perform async DNS resolution.
        
        Args:
            domain: Domain to resolve.
            record_type: Type of DNS record to resolve.
            
        Returns:
            List of DNS records.
            
        Raises:
            dns.exception.DNSException: If resolution fails.
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self.resolver.resolve(domain, record_type)
        )