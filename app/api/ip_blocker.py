"""IP-based blocking for abuse prevention."""
import logging
from datetime import datetime, timedelta
from typing import Optional, Tuple

from redis import Redis
from fastapi import HTTPException, Request

logger = logging.getLogger(__name__)

class IPBlocker:
    """Manages IP-based blocking for abuse prevention."""
    
    def __init__(self, redis_client: Redis):
        self.redis = redis_client
        self._failed_attempts_prefix = "failed_attempts:"
        self._blocked_ip_prefix = "blocked_ip:"
        
        # Configuration
        self.max_failures = 5  # Maximum failed attempts before blocking
        self.failure_window = 300  # Window for counting failures (5 minutes)
        self.block_duration = 3600  # Block duration in seconds (1 hour)
        
    async def check_ip_blocked(self, request: Request) -> None:
        """
        Check if an IP is blocked and raise HTTPException if it is.
        Also performs cleanup of expired blocks.
        """
        client_ip = self._get_client_ip(request)
        if self._is_ip_blocked(client_ip):
            logger.warning(f"Blocked request from IP: {client_ip}")
            raise HTTPException(
                status_code=403,
                detail="Access denied due to suspicious activity"
            )
    
    def record_failed_attempt(self, request: Request) -> None:
        """Record a failed authentication attempt for an IP."""
        client_ip = self._get_client_ip(request)
        key = f"{self._failed_attempts_prefix}{client_ip}"
        
        # Increment failed attempts counter
        current = self.redis.incr(key)
        if current == 1:
            # Set expiry on first failure
            self.redis.expire(key, self.failure_window)
            
        # Check if we should block the IP
        if current >= self.max_failures:
            self._block_ip(client_ip)
            
    def _block_ip(self, ip: str) -> None:
        """Block an IP address for the configured duration."""
        key = f"{self._blocked_ip_prefix}{ip}"
        self.redis.setex(key, self.block_duration, "1")
        logger.warning(f"Blocked IP address for abuse: {ip}")
        
    def _is_ip_blocked(self, ip: str) -> bool:
        """Check if an IP is currently blocked."""
        key = f"{self._blocked_ip_prefix}{ip}"
        return bool(self.redis.exists(key))
        
    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP from request, considering forwarded headers."""
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            # Get the first IP in the chain
            return forwarded.split(",")[0].strip()
        return request.client.host