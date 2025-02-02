"""DNS resolution module with parallel resolution capabilities."""
import asyncio
import logging
from typing import Dict, List, Optional, Tuple, Union
import time
import dns.asyncresolver
from .monitoring.dns_metrics import DNSMetrics
import dns.exception
import dns.rdtypes.ANY.MX
import dns.rdtypes.IN.A
from .dns_cache import DNSCache, DNSRecord

logger = logging.getLogger(__name__)

class DNSResolver:
    """Handles DNS resolution with parallel resolution and caching support."""
    
    def __init__(self, timeout: float = 5.0, cache_ttl: int = 1800):
        """Initialize resolver with configurable timeout and cache TTL and metrics.
        
        Args:
            timeout: DNS query timeout in seconds
            cache_ttl: Cache TTL in seconds
        """
        self.timeout = timeout
        self.cache = DNSCache(default_ttl=cache_ttl)
        self.metrics = DNSMetrics()
        
    async def _async_resolve(self, domain: str, record_type: str) -> List[Union[dns.rdtypes.ANY.MX.MX, dns.rdtypes.IN.A.A]]:
        """Perform parallel DNS resolution against multiple nameservers.
        
        Args:
            domain: Domain name to resolve
            record_type: Type of DNS record to query
            
        Returns:
            List of resolved DNS records
        """
        try:
            resolver = dns.asyncresolver.Resolver()
            resolver.timeout = self.timeout
            resolver.lifetime = self.timeout
            
            # Query nameservers in parallel
            tasks = []
            for ns in resolver.nameservers[:3]:  # Use up to 3 nameservers
                resolver_copy = dns.asyncresolver.Resolver()
                resolver_copy.nameservers = [ns]
                resolver_copy.timeout = self.timeout / 2  # Shorter timeout for parallel queries
                tasks.append(resolver_copy.resolve(domain, record_type))
            
            # Wait for first successful result or all failures
            done, pending = await asyncio.wait(
                tasks,
                return_when=asyncio.FIRST_COMPLETED
            )
            
            # Cancel pending tasks
            for task in pending:
                task.cancel()
                
            # Get result from first completed task
            for task in done:
                try:
                    result = await task
                    return list(result)
                except Exception:
                    continue
                    
            raise dns.resolver.NoAnswer()
            
        except dns.resolver.NoAnswer:
            return []
        except dns.resolver.NXDOMAIN:
            return []
        except Exception as e:
            logger.error(f"DNS resolution error for {domain}: {str(e)}")
            return []
            
    async def resolve_mx(self, domains: Union[str, List[str]]) -> Union[List[DNSRecord], Dict[str, List[DNSRecord]]]:
        """Resolve MX records for one or more domains with fallback to A/AAAA records.
        Performance metrics are collected for monitoring and optimization.
        
        Args:
            domains: Single domain or list of domains to resolve
            
        Returns:
            If single domain provided: List of DNS records
            If multiple domains provided: Dict mapping domains to lists of DNS records
        """
        start_time = time.time()
        single_domain = isinstance(domains, str)
        if single_domain:
            domains = [domains]
            
        # Check cache first
        missing_domains = await self.cache.get_missing_domains(domains)
        results = {}
        
        # Get cached results
        for domain in domains:
            if domain not in missing_domains:
                results[domain] = self.cache.get(domain)
                
        if missing_domains:
            # Resolve missing domains in parallel
            resolution_tasks = []
            for domain in missing_domains:
                resolution_tasks.append(self._async_resolve(domain, 'MX'))
                
            resolved_records = await asyncio.gather(*resolution_tasks)
            
            # Store results in cache and results dict
            cache_entries = {}
            for domain, records in zip(missing_domains, resolved_records):
                if not records:  # Fallback to A/AAAA if no MX records
                    records = await self._async_resolve(domain, 'A')
                dns_records = [DNSRecord(r) for r in records]
                cache_entries[domain] = (dns_records, None)  # Use default TTL
                results[domain] = dns_records
                
            # Bulk cache update
            await self.cache.bulk_set(cache_entries)
            
        duration = time.time() - start_time
        for domain in domains:
            self.metrics.record_resolution(
                domain=domain,
                duration=duration / len(domains),
                cached=domain not in missing_domains,
                parallel=len(missing_domains) > 1,
                failed=domain not in results
            )
            
        return results[domains[0]] if single_domain else results