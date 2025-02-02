"""
Rate Limiting Module
Implements rate limiting for API endpoints.
"""

import time
from typing import Dict, Tuple
from dataclasses import dataclass
from app.config import settings
from app.utils.metrics import RATE_LIMIT_EXCEEDED
from app.utils.logger import get_logger

logger = get_logger(__name__)

@dataclass
class RateLimitConfig:
    """Rate limit configuration."""
    requests: int  # Number of requests allowed
    window: int   # Time window in seconds
    
# Rate limit tiers with Redis-backed storage
RATE_LIMIT_TIERS = {
    "basic": RateLimitConfig(100, 3600),        # 100 requests per hour
    "pro": RateLimitConfig(1000, 3600),         # 1000 requests per hour
    "enterprise": RateLimitConfig(10000, 3600),  # 10000 requests per hour
    "unlimited": RateLimitConfig(-1, 3600)       # Unlimited requests
}

class RateLimiter:
    """Redis-backed rate limiting implementation with tiered limits."""
    
    def __init__(self, redis_client: RedisClient):
        """Initialize rate limiter with Redis client."""
        self.redis = redis_client
        self._rate_limit_prefix = "rate_limit:"
        
    async def check_rate_limit(
        self,
        api_key: str,
        multiplier: float = 1.0
    ) -> bool:
        """
        Check if request is within rate limits using Redis.
        
        Args:
            api_key: API key for identifying client
            multiplier: Rate limit multiplier for batch operations
            
        Returns:
            bool: True if within limits, False otherwise
        """
        tier = self._get_api_key_tier(api_key)
        limits = RATE_LIMIT_TIERS[tier]
        
        # Skip check for unlimited tier
        if limits.requests == -1:
            return True
            
        now = time.time()
        redis_key = f"{self._rate_limit_prefix}{api_key}"
        
        pipe = self.redis.pipeline()
        
        # Add current timestamp and get all requests in window
        pipe.zadd(redis_key, {str(now): now})
        pipe.zremrangebyscore(redis_key, "-inf", now - limits.window)
        pipe.zcard(redis_key)
        pipe.expire(redis_key, limits.window)
        
        _, _, num_requests, _ = await pipe.execute()
        
        # Check against adjusted limit
        adjusted_limit = int(limits.requests * multiplier)
        if num_requests > adjusted_limit:
            logger.warning(f"Rate limit exceeded for API key: {api_key}")
            RATE_LIMIT_EXCEEDED.labels(tier=tier).inc()
            return False
            
        return True
        
    def _get_api_key_tier(self, api_key: str) -> str:
        """Get rate limit tier from API key details."""
        key_details = key_manager.validate_key(api_key)
        if key_details:
            return key_details.tier
        return "basic"  # Default to basic tier if key is invalid