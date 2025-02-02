"""Security headers middleware for FastAPI application."""
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.types import ASGIApp

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware to add security headers to all responses."""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        
        # Add security headers
        headers = {
            'X-Frame-Options': 'DENY',  # Prevent clickjacking
            'X-Content-Type-Options': 'nosniff',  # Prevent MIME type sniffing
            'X-XSS-Protection': '1; mode=block',  # Enable XSS filtering
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',  # Enforce HTTPS
            'Content-Security-Policy': "default-src 'self'",  # Restrict content sources
            'Referrer-Policy': 'strict-origin-when-cross-origin',  # Control referrer information
            'Permissions-Policy': 'geolocation=(), microphone=()',  # Restrict browser features
        }
        
        for header_name, header_value in headers.items():
            response.headers[header_name] = header_value
            
        return response

def add_security_headers(app: FastAPI) -> None:
    """Add security headers middleware to FastAPI application."""
    app.add_middleware(SecurityHeadersMiddleware)