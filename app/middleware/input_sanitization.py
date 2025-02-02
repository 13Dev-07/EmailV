"""Input sanitization middleware for FastAPI application."""
import re
from typing import Any, Dict, List, Union

from fastapi import FastAPI, Request
from fastapi.middleware.base import BaseHTTPMiddleware
from starlette.datastructures import UploadFile
from pydantic import BaseModel

class InputSanitizer:
    """Handles input sanitization for various data types."""
    
    @staticmethod
    def sanitize_string(value: str) -> str:
        """
        Sanitize a string value:
        - Remove any control characters
        - Remove any NULL bytes
        - Trim whitespace
        - HTML encode special characters
        """
        if not isinstance(value, str):
            return value
            
        # Remove control characters and null bytes
        value = "".join(char for char in value if ord(char) >= 32)
        value = value.replace("\x00", "")
        
        # Trim whitespace
        value = value.strip()
        
        # HTML encode special characters
        value = (
            value.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
                .replace("'", "&#x27;")
        )
        
        return value
        
    @staticmethod
    def sanitize_dict(data: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively sanitize all string values in a dictionary."""
        result = {}
        for key, value in data.items():
            if isinstance(value, str):
                result[key] = InputSanitizer.sanitize_string(value)
            elif isinstance(value, dict):
                result[key] = InputSanitizer.sanitize_dict(value)
            elif isinstance(value, list):
                result[key] = InputSanitizer.sanitize_list(value)
            else:
                result[key] = value
        return result
        
    @staticmethod
    def sanitize_list(data: List[Any]) -> List[Any]:
        """Recursively sanitize all string values in a list."""
        result = []
        for item in data:
            if isinstance(item, str):
                result.append(InputSanitizer.sanitize_string(item))
            elif isinstance(item, dict):
                result.append(InputSanitizer.sanitize_dict(item))
            elif isinstance(item, list):
                result.append(InputSanitizer.sanitize_list(item))
            else:
                result.append(item)
        return result
        
class InputSanitizationMiddleware(BaseHTTPMiddleware):
    """Middleware to sanitize all incoming request data."""
    
    async def dispatch(self, request: Request, call_next):
        """Process the request, sanitizing all input data."""
        # Only sanitize POST, PUT, PATCH requests
        if request.method not in ["POST", "PUT", "PATCH"]:
            return await call_next(request)
            
        # Store original receive
        original_receive = request.receive
        
        # Override receive to sanitize the payload
        async def receive():
            payload = await original_receive()
            
            # Only process 'http.request' messages
            if payload["type"] == "http.request":
                body = payload.get("body", b"").decode()
                if body:
                    # Handle JSON data
                    if request.headers.get("content-type") == "application/json":
                        try:
                            import json
                            data = json.loads(body)
                            sanitized = InputSanitizer.sanitize_dict(data)
                            payload["body"] = json.dumps(sanitized).encode()
                        except json.JSONDecodeError:
                            pass
                            
                    # Handle form data
                    elif request.headers.get("content-type", "").startswith("multipart/form-data"):
                        # Form data is handled by FastAPI's form processing
                        pass
                        
                    # Handle URL-encoded form data
                    elif request.headers.get("content-type") == "application/x-www-form-urlencoded":
                        from urllib.parse import parse_qs, urlencode
                        data = parse_qs(body)
                        sanitized = {k: [InputSanitizer.sanitize_string(v) for v in vals]
                                   for k, vals in data.items()}
                        payload["body"] = urlencode(sanitized, doseq=True).encode()
                        
            return payload
            
        # Replace receive with our sanitizing version
        request._receive = receive
        
        # Process the request
        response = await call_next(request)
        return response
        
def add_input_sanitization(app: FastAPI) -> None:
    """Add input sanitization middleware to FastAPI application."""
    app.add_middleware(InputSanitizationMiddleware)