"""Security audit logging functionality."""
import json
import logging
from datetime import datetime
from typing import Any, Dict, Optional

from fastapi import Request
from pydantic import BaseModel

logger = logging.getLogger("security_audit")

class AuditLog(BaseModel):
    """Audit log entry details."""
    timestamp: datetime
    event_type: str
    api_key: Optional[str]
    client_ip: str
    request_path: str
    request_method: str
    status_code: int
    details: Dict[str, Any]

class SecurityAuditLogger:
    """Handles security-related audit logging."""
    
    @staticmethod
    async def log_request(
        request: Request,
        event_type: str,
        status_code: int,
        api_key: Optional[str] = None,
        **kwargs
    ) -> None:
        """
        Log a security audit event for an API request.
        
        Args:
            request: The FastAPI request object
            event_type: Type of security event (e.g., "authentication", "rate_limit")
            status_code: HTTP status code of the response
            api_key: API key used in the request (if any)
            **kwargs: Additional details to include in the audit log
        """
        # Get client IP
        client_ip = request.headers.get("X-Forwarded-For", request.client.host)
        if isinstance(client_ip, str) and "," in client_ip:
            client_ip = client_ip.split(",")[0].strip()
            
        # Create audit log entry
        audit_entry = AuditLog(
            timestamp=datetime.utcnow(),
            event_type=event_type,
            api_key=api_key,
            client_ip=client_ip,
            request_path=str(request.url),
            request_method=request.method,
            status_code=status_code,
            details=kwargs
        )
        
        # Log as JSON for easy parsing
        logger.info(audit_entry.json())
        
    @staticmethod
    def configure(log_file: str = "security_audit.log") -> None:
        """Configure the security audit logger."""
        handler = logging.FileHandler(log_file)
        handler.setFormatter(logging.Formatter("%(message)s"))
        
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
        logger.propagate = False  # Don't propagate to root logger