"""Rate limiting implementation for API endpoints."""

import time
from typing import Dict, Optional
import threading
from dataclasses import dataclass
from prometheus_client import Counter

rate_limit_exceeded = Counter(
    'rate_limit_exceeded_total',
    'Number of times rate limits were exceeded',
    ['endpoint']
)

@dataclass
class RateLimitEntry:
    count: int
    window_start: float

class RateLimiter:
    """Thread-safe rate limiter implementation."""
    
    def __init__(self, max_requests: int = 100, window_size: int = 60):
        """
        Initialize rate limiter.
        
        Args:
            max_requests: Maximum number of requests allowed in the window.
            window_size: Time window in seconds.
        """
        self._max_requests = max_requests
        self._window_size = window_size
        self._counters: Dict[str, RateLimitEntry] = {}
        self._lock = threading.Lock()
        
    def is_allowed(self, key: str) -> bool:
        """
        Check if request is allowed under rate limit.
        
        Args:
            key: Identifier for the client (e.g. IP address, API key)
            
        Returns:
            True if request is allowed, False if rate limit exceeded.
        """
        with self._lock:
            current_time = time.time()
            
            # Clean up old entries
            self._cleanup(current_time)
            
            # Get or create entry
            if key not in self._counters:
                self._counters[key] = RateLimitEntry(0, current_time)
            
            entry = self._counters[key]
            
            # Reset counter if window has expired
            if current_time - entry.window_start >= self._window_size:
                entry.count = 0
                entry.window_start = current_time
            
            # Check if limit exceeded
            if entry.count >= self._max_requests:
                rate_limit_exceeded.labels(endpoint='email_validation').inc()
                return False
            
            # Increment counter
            entry.count += 1
            return True
            
    def _cleanup(self, current_time: float) -> None:
        """Remove expired entries."""
        expired = [
            key for key, entry in self._counters.items()
            if current_time - entry.window_start >= self._window_size
        ]
        for key in expired:
            del self._counters[key]
            
    def get_remaining(self, key: str) -> Dict:
        """Get remaining requests and time until reset."""
        with self._lock:
            if key not in self._counters:
                return {
                    'remaining': self._max_requests,
                    'reset_in': self._window_size
                }
                
            entry = self._counters[key]
            current_time = time.time()
            time_passed = current_time - entry.window_start
            
            if time_passed >= self._window_size:
                return {
                    'remaining': self._max_requests,
                    'reset_in': self._window_size
                }
                
            return {
                'remaining': max(0, self._max_requests - entry.count),
                'reset_in': self._window_size - time_passed
            }

# Global rate limiter instance
email_validator_limiter = RateLimiter()