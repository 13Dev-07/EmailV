"""
Authentication utility functions for the API service.

This module handles API key generation, validation, and management.
"""

import secrets
from typing import Set
from .logger import logger
from .exceptions import AuthenticationError

# In-memory store of valid API keys
# In production, this should be replaced with a database
VALID_API_KEYS: Set[str] = set()

def generate_api_key() -> str:
    """
    Generates a new secure API key.
    
    Returns:
        str: A new API key
        
    Note:
        The generated key is automatically added to the valid keys set
    """
    new_key = secrets.token_urlsafe(32)
    VALID_API_KEYS.add(new_key)
    logger.info(f"Generated new API key: {new_key}")
    return new_key

def validate_api_key(api_key: str) -> bool:
    """
    Validates the provided API key.
    
    Args:
        api_key: The API key to validate
        
    Returns:
        bool: True if the API key is valid, False otherwise
        
    Note:
        This is a basic implementation. In production, this should:
        - Check against a secure database
        - Implement rate limiting per key
        - Check key expiration
        - Log validation attempts
    """
    if not api_key or not isinstance(api_key, str):
        logger.warning("Invalid API key format")
        return False
        
    is_valid = api_key in VALID_API_KEYS
    
    if not is_valid:
        logger.warning(f"Failed API key validation attempt")
    
    return is_valid

def revoke_api_key(api_key: str) -> bool:
    """
    Revokes an existing API key.
    
    Args:
        api_key: The API key to revoke
        
    Returns:
        bool: True if the key was found and revoked, False otherwise
    """
    if api_key in VALID_API_KEYS:
        VALID_API_KEYS.remove(api_key)
        logger.info(f"Revoked API key: {api_key}")
        return True
    return False

def list_valid_keys() -> Set[str]:
    """
    Returns the set of currently valid API keys.
    
    Returns:
        Set[str]: Set of valid API keys
    """
    return VALID_API_KEYS.copy()