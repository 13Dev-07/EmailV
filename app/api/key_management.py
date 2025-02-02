"""API key management and rotation functionality."""
import logging
import secrets
from datetime import datetime, timedelta
from typing import Optional, Tuple

from fastapi import HTTPException
from redis import Redis
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class APIKey(BaseModel):
    """API key details"""
    key: str
    created_at: datetime
    expires_at: Optional[datetime]
    is_active: bool
    tier: str
    
class APIKeyManager:
    """Manages API key lifecycle including rotation and revocation."""
    
    def __init__(self, redis_client: Redis):
        self.redis = redis_client
        self._key_prefix = "apikey:"
        self._rotation_prefix = "rotation:"
        
    def generate_new_key(self, tier: str = "basic", expiry_days: int = 90) -> APIKey:
        """Generate a new API key with specified tier and expiration."""
        key = secrets.token_urlsafe(32)
        created_at = datetime.utcnow()
        expires_at = created_at + timedelta(days=expiry_days)
        
        api_key = APIKey(
            key=key,
            created_at=created_at,
            expires_at=expires_at,
            is_active=True,
            tier=tier
        )
        
        # Store key details in Redis
        self._store_key(api_key)
        return api_key
        
    def rotate_key(self, current_key: str) -> Tuple[APIKey, APIKey]:
        """
        Rotate an API key by generating a new one and maintaining both temporarily.
        Returns both old and new keys to allow for transition period.
        """
        current = self._get_key_details(current_key)
        if not current:
            raise HTTPException(status_code=404, detail="API key not found")
            
        # Generate new key with same tier
        new_key = self.generate_new_key(current.tier)
        
        # Store rotation relationship
        self.redis.setex(
            f"{self._rotation_prefix}{current_key}",
            timedelta(days=7),  # 7 day rotation window
            new_key.key
        )
        
        return current, new_key
        
    def revoke_key(self, key: str) -> None:
        """Revoke an API key immediately."""
        current = self._get_key_details(key)
        if current:
            current.is_active = False
            current.expires_at = datetime.utcnow()
            self._store_key(current)
            
    def validate_key(self, key: str) -> Optional[APIKey]:
        """
        Validate an API key and return its details if valid.
        Handles both current and rotating keys.
        """
        details = self._get_key_details(key)
        
        # Check if this is a rotated key
        if not details:
            # Check if it's in rotation
            original_key = self.redis.keys(f"{self._rotation_prefix}*{key}")
            if original_key:
                details = self._get_key_details(original_key[0].decode().split(':')[-1])
                
        if not details or not details.is_active:
            return None
            
        # Check expiration
        if details.expires_at and details.expires_at < datetime.utcnow():
            self.revoke_key(key)
            return None
            
        return details
        
    def _store_key(self, api_key: APIKey) -> None:
        """Store API key details in Redis."""
        self.redis.hmset(
            f"{self._key_prefix}{api_key.key}",
            {
                "created_at": api_key.created_at.isoformat(),
                "expires_at": api_key.expires_at.isoformat() if api_key.expires_at else "",
                "is_active": "1" if api_key.is_active else "0",
                "tier": api_key.tier
            }
        )
        
    def _get_key_details(self, key: str) -> Optional[APIKey]:
        """Retrieve API key details from Redis."""
        details = self.redis.hgetall(f"{self._key_prefix}{key}")
        if not details:
            return None
            
        return APIKey(
            key=key,
            created_at=datetime.fromisoformat(details[b"created_at"].decode()),
            expires_at=datetime.fromisoformat(details[b"expires_at"].decode()) if details[b"expires_at"] else None,
            is_active=details[b"is_active"] == b"1",
            tier=details[b"tier"].decode()
        )