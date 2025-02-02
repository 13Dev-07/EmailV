"""API key validation middleware."""

import logging
from typing import Optional

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from prometheus_client import Counter, Histogram

from app.api_key_manager import APIKeyManager

# Metrics
API_KEY_VALIDATION_TIME = Histogram(
    "api_key_validation_seconds",
    "Time spent validating API keys",
    ["endpoint"]
)

INVALID_KEY_REQUESTS = Counter(
    "invalid_api_key_requests_total",
    "Number of requests with invalid API keys",
    ["endpoint"]
)

class APIKeyMiddleware:
    """Middleware for API key validation."""

    def __init__(self, api_key_manager: APIKeyManager):
        self.key_manager = api_key_manager
        self.logger = logging.getLogger(__name__)

    async def __call__(self, request: Request, call_next):
        """Process the request and validate API key."""
        # Skip validation for certain paths
        if self._should_skip_auth(request.url.path):
            return await call_next(request)

        api_key = self._extract_api_key(request)
        if not api_key:
            INVALID_KEY_REQUESTS.labels(endpoint=request.url.path).inc()
            return JSONResponse(
                status_code=401,
                content={"error": "API key missing"}
            )

        # Get required scopes for the endpoint
        required_scopes = self._get_required_scopes(request)

        # Validate the API key
        with API_KEY_VALIDATION_TIME.labels(endpoint=request.url.path).time():
            is_valid = await self.key_manager.validate_key(api_key, required_scopes)

        if not is_valid:
            INVALID_KEY_REQUESTS.labels(endpoint=request.url.path).inc()
            return JSONResponse(
                status_code=401,
                content={"error": "Invalid API key"}
            )

        # Continue with the request
        response = await call_next(request)
        return response

    def _extract_api_key(self, request: Request) -> Optional[str]:
        """Extract API key from request headers or query parameters."""
        # Try Authorization header first
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            return auth_header.split(" ")[1]

        # Try X-API-Key header next
        api_key = request.headers.get("X-API-Key")
        if api_key:
            return api_key

        # Finally, try query parameter
        return request.query_params.get("api_key")

    def _should_skip_auth(self, path: str) -> bool:
        """Check if authentication should be skipped for this path."""
        skip_paths = {
            "/docs",
            "/redoc",
            "/openapi.json",
            "/metrics",
            "/health",
            "/readiness"
        }
        return path in skip_paths

    def _get_required_scopes(self, request: Request) -> list:
        """Get required scopes for the endpoint."""
        # This could be enhanced to read from route metadata
        # For now, return basic scopes based on method
        if request.method == "GET":
            return ["read"]
        elif request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            return ["write"]
        return ["default"]