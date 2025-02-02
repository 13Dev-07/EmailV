"""Application configuration settings."""

from typing import Optional
from pydantic import BaseSettings, Field
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Service info
    SERVICE_NAME: str = "email-validator"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # API settings
    API_WORKERS: int = 4
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_PREFIX: str = "/api/v1"
    
    # DNS settings
    DNS_TIMEOUT: float = 5.0
    DNS_CACHE_TTL: int = 300
    
    # SMTP settings
    SMTP_TIMEOUT: float = 10.0
    SMTP_MAX_CONNECTIONS: int = 10
    SMTP_MAX_RETRIES: int = 3
    SMTP_RETRY_DELAY: float = 1.0
    VERIFY_FROM_EMAIL: str = "verify@yourdomain.com"
    
    # Redis settings
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    REDIS_MAX_CONNECTIONS: int = 10
    
    # Cache settings
    DEFAULT_CACHE_TTL: int = 3600
    EMAIL_VALIDATION_CACHE_TTL: int = 86400
    
    # Rate limiting
    RATE_LIMIT_ENABLED: bool = True
    DEFAULT_RATE_LIMIT: int = 100
    DEFAULT_RATE_WINDOW: int = 60
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Metrics
    METRICS_ENABLED: bool = True
    METRICS_PORT: int = 9090
    
    class Config:
        case_sensitive = True
        env_prefix = "EMAIL_VALIDATOR_"

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()