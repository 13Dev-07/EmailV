"""
API Authentication Module
Handles API key verification and access control.
"""

from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
from typing import Optional
from app.utils.metrics import AUTH_FAILURES
from app.utils.logger import get_logger
from app.config import settings

logger = get_logger(__name__)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(
    api_key_header: str = Security(api_key_header),
    request: Request = None
) -> APIKey:
    """
    Verify the provided API key.
    
    Args:
        api_key_header: API key from request header
        request: FastAPI request object for IP tracking
        
    Returns:
        APIKey: Verified API key details
        
    Raises:
        HTTPException: If API key is invalid or IP is blocked
    """
    # Check for IP blocking first
    if request:
        await ip_blocker.check_ip_blocked(request)
    if not api_key_header:
        AUTH_FAILURES.labels(reason="missing_key").inc()
        await SecurityAuditLogger.log_request(
            request,
            event_type="authentication_failure",
            status_code=HTTP_403_FORBIDDEN,
            details={"reason": "missing_key"}
        )
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="API key required"
        )
        
    # Validate API key using key manager
    key_details = key_manager.validate_key(api_key_header)
    if not key_details:
        AUTH_FAILURES.labels(reason="invalid_key").inc()
        logger.warning(f"Invalid API key attempt: {api_key_header}")
        if request:
            ip_blocker.record_failed_attempt(request)
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Invalid API key"
        )
        
    # Log successful authentication
    await SecurityAuditLogger.log_request(
        request,
        event_type="authentication_success",
        status_code=200,
        api_key=api_key_header,
        details={"tier": key_details.tier}
    )
    
    return key_details

def _is_valid_api_key(api_key: str) -> bool:
    """
    Check if API key is valid.
    
    Args:
        api_key: API key to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    return api_key in settings.VALID_API_KEYS