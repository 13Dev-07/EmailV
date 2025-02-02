"""API key management and rotation system."""

import logging
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set

from prometheus_client import Counter, Gauge, Histogram

# Metrics
API_KEY_USAGE = Counter(
    "api_key_usage_total",
    "Total number of API key usages",
    ["key_id", "endpoint"]
)

API_KEY_ERRORS = Counter(
    "api_key_errors_total",
    "Number of API key validation errors",
    ["key_id", "error_type"]
)

API_KEY_ROTATIONS = Counter(
    "api_key_rotations_total",
    "Total number of API key rotations",
    ["key_id"]
)

ACTIVE_API_KEYS = Gauge(
    "active_api_keys",
    "Number of active API keys"
)

class APIKeyManager:
    """Manages API key lifecycle and validation."""

    def __init__(self, rotation_interval: int = 86400, max_keys_per_client: int = 2):
        self.logger = logging.getLogger(__name__)
        self.rotation_interval = rotation_interval  # Default 24 hours
        self.max_keys_per_client = max_keys_per_client
        self._keys: Dict[str, Dict] = {}
        self._client_keys: Dict[str, Set[str]] = {}

    async def create_key(self, client_id: str, scopes: List[str] = None) -> Dict:
        """Create a new API key for a client."""
        if client_id in self._client_keys and \
           len(self._client_keys[client_id]) >= self.max_keys_per_client:
            raise ValueError("Maximum number of keys reached for client")

        key_id = str(uuid.uuid4())
        api_key = str(uuid.uuid4())
        created_at = datetime.utcnow()

        key_data = {
            "key_id": key_id,
            "client_id": client_id,
            "api_key": api_key,
            "scopes": scopes or ["default"],
            "created_at": created_at,
            "rotated_at": None,
            "is_active": True
        }

        self._keys[key_id] = key_data
        if client_id not in self._client_keys:
            self._client_keys[client_id] = set()
        self._client_keys[client_id].add(key_id)

        ACTIVE_API_KEYS.inc()
        return key_data

    async def rotate_key(self, key_id: str) -> Dict:
        """Rotate an existing API key."""
        if key_id not in self._keys:
            raise KeyError("API key not found")

        key_data = self._keys[key_id]
        new_api_key = str(uuid.uuid4())
        key_data["api_key"] = new_api_key
        key_data["rotated_at"] = datetime.utcnow()

        API_KEY_ROTATIONS.labels(key_id=key_id).inc()
        return key_data

    async def validate_key(self, api_key: str, required_scopes: List[str] = None) -> bool:
        """Validate an API key and its scopes."""
        for key_data in self._keys.values():
            if key_data["api_key"] == api_key and key_data["is_active"]:
                if required_scopes:
                    if not all(scope in key_data["scopes"] for scope in required_scopes):
                        API_KEY_ERRORS.labels(
                            key_id=key_data["key_id"],
                            error_type="InvalidScope"
                        ).inc()
                        return False

                API_KEY_USAGE.labels(
                    key_id=key_data["key_id"],
                    endpoint="validate"
                ).inc()
                return True

        API_KEY_ERRORS.labels(
            key_id="unknown",
            error_type="InvalidKey"
        ).inc()
        return False

    async def deactivate_key(self, key_id: str) -> None:
        """Deactivate an API key."""
        if key_id not in self._keys:
            raise KeyError("API key not found")

        self._keys[key_id]["is_active"] = False
        ACTIVE_API_KEYS.dec()

        client_id = self._keys[key_id]["client_id"]
        if client_id in self._client_keys:
            self._client_keys[client_id].remove(key_id)
            if not self._client_keys[client_id]:
                del self._client_keys[client_id]

    async def cleanup_expired_keys(self) -> None:
        """Clean up expired API keys."""
        current_time = datetime.utcnow()
        for key_id, key_data in list(self._keys.items()):
            created_at = key_data["created_at"]
            if current_time - created_at > timedelta(seconds=self.rotation_interval * 2):
                await self.deactivate_key(key_id)

    async def get_client_keys(self, client_id: str) -> List[Dict]:
        """Get all active keys for a client."""
        if client_id not in self._client_keys:
            return []
        return [
            self._keys[key_id] for key_id in self._client_keys[client_id]
            if self._keys[key_id]["is_active"]
        ]