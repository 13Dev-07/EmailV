"""Role account detection functionality."""
import logging
import re
from typing import Optional, Set

from app.utils.cache_manager import CacheManager
from app.utils.role_patterns import ROLE_PATTERNS, OPTIONAL_ROLE_PATTERNS

logger = logging.getLogger(__name__)

class RoleAccountDetector:
    """Detects role-based email accounts."""
    
    def __init__(self, 
                 cache_manager: Optional[CacheManager] = None,
                 include_optional_patterns: bool = True):
        """Initialize role account detector.
        
        Args:
            cache_manager: Optional cache manager for caching results
            include_optional_patterns: Whether to include optional role patterns
        """
        self.cache_manager = cache_manager
        self.patterns: Set[str] = set()
        self._load_patterns(include_optional_patterns)
        
    def _load_patterns(self, include_optional: bool = True) -> None:
        """Load role-based patterns.
        
        Args:
            include_optional: Whether to include optional patterns
        """
        self.patterns = set(ROLE_PATTERNS)
        if include_optional:
            self.patterns.update(OPTIONAL_ROLE_PATTERNS)
            
        # Compile patterns for performance
        self.compiled_patterns = [re.compile(p) for p in self.patterns]
        
    def is_role_account(self, email: str) -> bool:
        """Check if email address is a role account.
        
        Args:
            email: Email address to check
            
        Returns:
            bool: True if role account patterns match, False otherwise
        """
        # Check cache first
        if self.cache_manager:
            cached_result = self.cache_manager.get(f"role:{email}")
            if cached_result is not None:
                return cached_result
                
        # Normalize email for consistent matching
        email = email.lower().strip()
        
        # Check against role patterns
        for pattern in self.compiled_patterns:
            if pattern.match(email):
                self._cache_result(email, True)
                return True
                
        self._cache_result(email, False)
        return False
        
    def _cache_result(self, email: str, is_role: bool) -> None:
        """Cache role account detection result.
        
        Args:
            email: Email that was checked
            is_role: Whether email is a role account
        """
        if self.cache_manager:
            try:
                self.cache_manager.set(
                    f"role:{email}",
                    is_role,
                    expire=86400  # Cache for 24 hours
                )
            except Exception as e:
                logger.warning(f"Failed to cache role account result: {str(e)}")
                
    def add_patterns(self, patterns: Set[str]) -> None:
        """Add custom role patterns.
        
        Args:
            patterns: Set of regex patterns to add
        """
        for pattern in patterns:
            if not pattern.startswith('^'):
                pattern = '^' + pattern
            self.patterns.add(pattern)
            self.compiled_patterns.append(re.compile(pattern))
            
    def remove_patterns(self, patterns: Set[str]) -> None:
        """Remove role patterns.
        
        Args:
            patterns: Set of patterns to remove
        """
        self.patterns.difference_update(patterns)
        self.compiled_patterns = [re.compile(p) for p in self.patterns]