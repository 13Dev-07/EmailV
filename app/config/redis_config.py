"""Redis configuration module."""

from typing import Optional
from pydantic import BaseSettings

class RedisSettings(BaseSettings):
    """Redis connection settings."""
    
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    REDIS_MAX_CONNECTIONS: int = 10
    REDIS_SOCKET_TIMEOUT: float = 1.0
    REDIS_RETRY_ON_TIMEOUT: bool = True
    
    # Cache settings
    DEFAULT_CACHE_TTL: int = 3600  # 1 hour
    DNS_CACHE_TTL: int = 300  # 5 minutes
    EMAIL_VALIDATION_CACHE_TTL: int = 86400  # 24 hours
    
    # Rate limiting settings
    DEFAULT_RATE_LIMIT: int = 100  # requests
    DEFAULT_RATE_WINDOW: int = 60  # seconds
    
    class Config:
        case_sensitive = True
        env_prefix = ""