"""
Disposable Email Detection Module
Detects disposable, temporary, and throwaway email addresses.
"""

import os
import re
from typing import Set, Dict, Optional
from app.utils.cache_manager import CacheManager
from app.utils.domain_constants import (
    DISPOSABLE_DOMAINS_FILE,
    DISPOSABLE_CACHE_TTL,
    ERR_DISPOSABLE_EMAIL
)

class DisposableDetector:
    """Detects disposable and temporary email addresses."""
    
    def __init__(self, cache_manager: Optional[CacheManager] = None):
        """
        Initialize the detector with cache support.
        
        Args:
            cache_manager: Optional cache manager for results caching
        """
        self.cache_manager = cache_manager
        self._disposable_domains: Set[str] = set()
        self._load_disposable_domains()
        
    def _load_disposable_domains(self) -> None:
        """Load disposable domain patterns from file."""
        if os.path.exists(DISPOSABLE_DOMAINS_FILE):
            with open(DISPOSABLE_DOMAINS_FILE, 'r') as f:
                self._disposable_domains = {
                    line.strip().lower() for line in f if line.strip()
                }
    
    def is_disposable(self, domain: str) -> bool:
        """Check if a domain is a disposable email provider.
        
        Args:
            domain: Domain to check
            
        Returns:
            bool: True if domain is disposable, False otherwise
        """
        # Check cache first
        if self.cache_manager:
            cached_result = self.cache_manager.get(f"disposable:{domain}")
            if cached_result is not None:
                return cached_result
                
        # Check known disposable domains
        if domain in self.disposable_domains:
            self._cache_result(domain, True)
            return True
            
        # Check domain patterns
        if self._is_temporary_pattern(domain) or self._has_suspicious_pattern(domain):
            self._cache_result(domain, True)
            return True
            
        # Check domain reputation
        reputation = self.reputation_checker.check_domain(domain)
        if reputation.is_disposable or reputation.spam_score > 0.8:
            self._cache_result(domain, True)
            return True
            
        # Domain appears legitimate
        self._cache_result(domain, False)
        return False
        """
        Check if a domain is from a disposable email provider.
        
        Args:
            domain: Domain to check
            
        Returns:
            bool: True if domain is disposable, False otherwise
        """
        domain = domain.lower()
        
        # Check cache first
        if self.cache_manager:
            cache_key = f"disposable:{domain}"
            cached_result = self.cache_manager.get(cache_key)
            if cached_result is not None:
                return cached_result
        
        # Check exact match
        is_disposable = domain in self._disposable_domains
        
        # Check pattern match
        if not is_disposable:
            is_disposable = any(
                pattern for pattern in self._disposable_domains
                if pattern.startswith('*') and domain.endswith(pattern[1:])
            )
        
        # Cache result
        if self.cache_manager:
            self.cache_manager.set(cache_key, is_disposable, DISPOSABLE_CACHE_TTL)
            
        return is_disposable
        
    def check_domain(self, domain: str) -> Dict[str, bool]:
        """
        Comprehensive check of a domain for disposable characteristics.
        
        Args:
            domain: Domain to analyze
            
        Returns:
            Dict with analysis results
        """
        return {
            "is_disposable": self.is_disposable(domain),
            "is_temporary": self._is_temporary_pattern(domain),
            "is_suspicious": self._has_suspicious_pattern(domain)
        }
        
    def _is_temporary_pattern(self, domain: str) -> bool:
        """Check if domain follows temporary email patterns."""
        patterns = [
            r'\d{3,}',  # Multiple numbers
            r'temp',
            r'disposable',
            r'throwaway',
            r'trash',
            r'fake',
            r'spam'
        ]
        return any(re.search(pattern, domain.lower()) for pattern in patterns)
        
    def _has_suspicious_pattern(self, domain: str) -> bool:
        """Check for suspicious patterns indicating disposable service."""
        suspicious = [
            r'mail\d+\.',
            r'temp\d+\.',
            r'[a-z]{2}\d{4,}\.',
            r'\d{2,}min\.',
            r'mailinator',
            r'guerrilla',
            r'minute',
            r'disposa',
            r'wegwerf',
            r'tempmail',
            r'tmpmail',
            r'spam'
        ]
        return any(re.search(pattern, domain.lower()) for pattern in suspicious)