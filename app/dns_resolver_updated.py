"""DNS resolution module for email validation with improved error handling and resource management."""

import asyncio
import concurrent.futures
import logging
from contextlib import contextmanager
from typing import List, Optional, Union

import dns.resolver
from dns.resolver import Answer

from app.dns_cache import DNSCache, DNSRecord


class DNSResolver:
    """DNS resolver with caching and async support."""

    def __init__(self, timeout: float = 5.0, cache_ttl: int = 1800, max_workers: int = 10):
        """Initialize DNS resolver.
        
        Args:
            timeout: DNS query timeout in seconds
            cache_ttl: Cache TTL in seconds
            max_workers: Maximum number of worker threads for DNS resolution
        """
        self.resolver = dns.resolver.Resolver()
        self.resolver.lifetime = timeout
        self.cache = DNSCache(default_ttl=cache_ttl)
        self._lock = asyncio.Lock()
        self._executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=max_workers,
            thread_name_prefix='dns_resolver'
        )

    async def resolve_mx(self, domain: str) -> List[DNSRecord]:
        """
        Resolve MX records for a domain.
        
        Args:
            domain: Domain to resolve MX records for.
            
        Returns:
            List of MX records.
            
        Raises:
            dns.exception.DNSException: If resolution fails.
        """
        cached = self.cache.get(domain, 'MX')
        if cached:
            return cached

        try:
            records = await self._async_resolve(domain, 'MX')
            dns_records = [DNSRecord(str(r.exchange), r.preference) for r in records]
            self.cache.set(domain, 'MX', dns_records)
            return dns_records
        except dns.exception.DNSException as e:
            logging.error(f"Failed to resolve MX records for {domain}: {str(e)}")
            raise

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
        try:
            return await loop.run_in_executor(
                self._executor,
                lambda: self.resolver.resolve(domain, record_type)
            )
        except Exception as e:
            # Log the error before re-raising
            logging.error(f"DNS resolution failed for {domain} ({record_type}): {str(e)}")
            raise

    async def close(self):
        """Close the resolver and cleanup resources."""
        if hasattr(self, '_executor'):
            self._executor.shutdown(wait=True)