"""
DNS Resolution Module
Provides functionality for DNS lookups and validation.

This module implements RFC 5321 compliant DNS resolution with support for:
- MX record lookups with proper prioritization
- Fallback to A/AAAA records
- Caching with TTL support
- Timeout handling
- IDNA domain name support
"""

import dns.resolver
import dns.exception
from dns.resolver import Answer
from typing import Dict, List, Tuple, Optional, Union
from app.utils.cache_manager import CacheManager
from app.utils.dns_constants import (
    MX_RECORD, A_RECORD, AAAA_RECORD, NS_RECORD, PTR_RECORD,
    DNS_TIMEOUT, CACHE_TTL,
    ERR_DNS_TIMEOUT, ERR_NO_RECORDS, ERR_INVALID_MX, ERR_DNS_ERROR,
    CACHE_KEY_PREFIX, MX_CACHE_PREFIX, A_CACHE_PREFIX,
    AAAA_CACHE_PREFIX, NS_CACHE_PREFIX, PTR_CACHE_PREFIX
)
from app.utils.exceptions import DNSError

class DNSResolver:
    """
    DNS resolver with caching support and comprehensive record validation.
    """
    
    def __init__(self, cache_manager: Optional[CacheManager] = None):
        """
        Initialize DNS resolver with optional cache manager.
        
        Args:
            cache_manager (Optional[CacheManager]): Cache manager for DNS results
        """
        self.cache_manager = cache_manager
        self._resolver = dns.resolver.Resolver()
        self._resolver.timeout = DNS_TIMEOUT
        self._resolver.lifetime = DNS_TIMEOUT

    def _get_cache_key(self, domain: str, record_type: str) -> str:
        """Generate cache key for domain and record type."""
        prefix = {
            MX_RECORD: MX_CACHE_PREFIX,
            A_RECORD: A_CACHE_PREFIX,
            AAAA_RECORD: AAAA_CACHE_PREFIX,
            NS_RECORD: NS_CACHE_PREFIX,
            PTR_RECORD: PTR_CACHE_PREFIX
        }.get(record_type, CACHE_KEY_PREFIX)
        return f"{prefix}{domain}"

    def encode_idn(self, domain: str) -> str:
        """
        Encode internationalized domain name to ASCII.
        
        Args:
            domain (str): Domain name to encode
            
        Returns:
            str: ASCII encoded domain name
            
        Raises:
            DNSError: If domain encoding fails
        """
        try:
            return domain.encode('idna').decode('ascii')
        except UnicodeError as e:
            raise DNSError(f"{ERR_INVALID_MX}: {str(e)}")

    def get_mx_records(self, domain: str) -> List[Tuple[int, str]]:
        """
        Get MX records for a domain with caching and fallback support.
        
        Args:
            domain (str): Domain to lookup MX records for.
        
        Returns:
            List[Tuple[int, str]]: List of tuples containing (priority, mailserver).
            
        Raises:
            DNSError: If DNS resolution fails after fallback attempts.
        """
        cache_key = self._get_cache_key(domain, MX_RECORD)
        
        # Check cache first
        if self.cache_manager:
            cached_result = self.cache_manager.get(cache_key)
            if cached_result is not None:
                return cached_result
                
        try:
            # Try MX lookup
            try:
                answers = self._resolver.resolve(domain, MX_RECORD)
                mx_records = [(rdata.preference, str(rdata.exchange)) for rdata in answers]
                
                # Cache successful result
                if self.cache_manager and mx_records:
                    self.cache_manager.set(cache_key, mx_records, CACHE_TTL)
                    
                return mx_records
                
            except dns.resolver.NoAnswer:
                # Fallback to A/AAAA records
                fallback_records = []
                try:
                    a_records = self._resolver.resolve(domain, A_RECORD)
                    fallback_records.extend([(10, domain) for _ in a_records])
                except Exception:
                    pass
                    
                try:
                    aaaa_records = self._resolver.resolve(domain, AAAA_RECORD)
                    fallback_records.extend([(10, domain) for _ in aaaa_records])
                except Exception:
                    pass
                    
                if fallback_records:
                    # Cache fallback results
                    if self.cache_manager:
                        self.cache_manager.set(cache_key, fallback_records, CACHE_TTL)
                    return fallback_records
                    
                raise DNSError(ERR_NO_RECORDS)
                
        except dns.resolver.NXDOMAIN:
            raise DNSError(ERR_NO_RECORDS)
        except dns.resolver.Timeout:
            raise DNSError(ERR_DNS_TIMEOUT)
        except Exception as e:
            raise DNSError(f"{ERR_DNS_ERROR}: {str(e)}")

    def verify_ptr_record(self, domain: str) -> Optional[str]:
        """
        Verify PTR record for a domain.
        
        Args:
            domain (str): Domain to verify PTR record for.
            
        Returns:
            Optional[str]: PTR record value if found, None otherwise.
        """
        cache_key = self._get_cache_key(domain, PTR_RECORD)
        
        # Check cache
        if self.cache_manager:
            cached_result = self.cache_manager.get(cache_key)
            if cached_result is not None:
                return cached_result

        try:
            answers = self._resolver.resolve(domain, PTR_RECORD)
            if answers:
                ptr_value = str(answers[0])
                # Cache result
                if self.cache_manager:
                    self.cache_manager.set(cache_key, ptr_value, CACHE_TTL)
                return ptr_value
        except Exception:
            pass
            
        return None

    def resolve_domain(self, domain: str) -> Dict[str, bool]:
        """
        Comprehensive domain resolution checking MX, A, AAAA, and NS records.
        
        Args:
            domain (str): Domain to resolve
            
        Returns:
            Dict[str, bool]: Dictionary with resolution results for each record type
        """
        result = {
            "mx_found": False,
            "a_found": False,
            "aaaa_found": False,
            "ns_found": False,
            "domain_exists": False
        }
        
        try:
            # Check MX records
            mx_records = self.get_mx_records(domain)
            result["mx_found"] = bool(mx_records)
            
            # Check A records
            try:
                a_records = self._resolver.resolve(domain, A_RECORD)
                result["a_found"] = bool(a_records)
            except Exception:
                pass
                
            # Check AAAA records
            try:
                aaaa_records = self._resolver.resolve(domain, AAAA_RECORD)
                result["aaaa_found"] = bool(aaaa_records)
            except Exception:
                pass
                
            # Check NS records
            try:
                ns_records = self._resolver.resolve(domain, NS_RECORD)
                result["ns_found"] = bool(ns_records)
            except Exception:
                pass
                
            # Domain exists if any record type is found
            result["domain_exists"] = any([
                result["mx_found"],
                result["a_found"],
                result["aaaa_found"],
                result["ns_found"]
            ])
            
        except Exception:
            # Leave all values as False if resolution fails
            pass
            
        return result