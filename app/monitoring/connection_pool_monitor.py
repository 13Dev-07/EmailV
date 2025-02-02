"""Connection pool monitoring implementation."""

import logging
import time
from typing import Optional

from prometheus_client import Counter, Gauge, Histogram

# Connection pool metrics
CONNECTION_REQUESTS = Counter(
    "smtp_connection_requests_total",
    "Total number of connection requests",
    ["server"]
)

CONNECTION_ERRORS = Counter(
    "smtp_connection_errors_total",
    "Number of failed connection attempts",
    ["server", "error_type"]
)

POOL_SIZE = Gauge(
    "smtp_pool_size_current",
    "Current size of connection pool",
    ["server", "status"]
)

CONNECTION_WAIT_TIME = Histogram(
    "smtp_connection_wait_seconds",
    "Time spent waiting for an available connection",
    ["server"]
)

class ConnectionPoolMonitor:
    """Monitors SMTP connection pool health and metrics."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._request_start_times = {}
        
    def start_connection_request(self, request_id: str):
        """Record the start of a connection request."""
        self._request_start_times[request_id] = time.time()
        
    def complete_connection_request(self, request_id: str, server: str):
        """Record completion of a connection request."""
        start_time = self._request_start_times.pop(request_id, None)
        if start_time:
            duration = time.time() - start_time
            CONNECTION_WAIT_TIME.labels(server=server).observe(duration)
            
    def record_connection_error(self, server: str, error_type: str):
        """Record a connection error."""
        CONNECTION_ERRORS.labels(
            server=server,
            error_type=error_type
        ).inc()
        
    def record_connection_added(self, server: str):
        """Record addition of a new connection."""
        POOL_SIZE.labels(server=server, status="total").inc()
        
    def record_connection_removed(self):
        """Record removal of a connection."""
        POOL_SIZE.labels(status="total").dec()
        
    def record_connection_released(self):
        """Record return of a connection to the pool."""
        POOL_SIZE.labels(status="available").inc()
        
    def record_connection_acquired(self):
        """Record acquisition of a connection from the pool."""
        POOL_SIZE.labels(status="in_use").inc()