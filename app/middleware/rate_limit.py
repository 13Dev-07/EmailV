"""Rate limiting middleware for FastAPI application."""
from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.status import HTTP_429_TOO_MANY_REQUESTS
from app.api.rate_limiter import RateLimiter
from app.api.authentication import verify_api_key

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware to enforce rate limits on API endpoints."""
    
    def __init__(self, app: FastAPI, rate_limiter: RateLimiter):
        super().__init__(app)
        self.rate_limiter = rate_limiter
        
    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for non-API routes
        if not request.url.path.startswith("/api/"):
            return await call_next(request)
            
        # Get API key from header
        api_key = request.headers.get("X-API-Key")
        if not api_key:
            raise HTTPException(status_code=403, detail="API key required")
            
        # Check rate limit
        if not await self.rate_limiter.check_rate_limit(api_key):
            # Log rate limit exceeded event
            await SecurityAuditLogger.log_request(
                request,
                event_type="rate_limit_exceeded",
                status_code=HTTP_429_TOO_MANY_REQUESTS,
                api_key=api_key
            )
            raise HTTPException(
                status_code=HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded"
            )
            
        return await call_next(request)

def add_rate_limit_middleware(app: FastAPI, rate_limiter: RateLimiter) -> None:
    """Add rate limiting middleware to FastAPI application."""
    app.add_middleware(RateLimitMiddleware, rate_limiter=rate_limiter)