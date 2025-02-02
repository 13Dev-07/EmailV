"""Connection pooling metrics collection."""
from dataclasses import dataclass, field
from typing import Dict, List, Optional
import time

@dataclass
class PoolMetrics:
    """Metrics for connection pool performance."""
    total_connections: int = 0
    active_connections: int = 0
    idle_connections: int = 0
    connection_errors: int = 0
    connection_timeouts: int = 0
    total_wait_time: float = 0.0
    total_requests: int = 0
    shard_distribution: Dict[str, int] = field(default_factory=dict)
    
    @property
    def average_wait_time(self) -> float:
        """Calculate average wait time for connections."""
        return self.total_wait_time / self.total_requests if self.total_requests > 0 else 0.0
    
    @property
    def utilization_rate(self) -> float:
        """Calculate pool utilization rate."""
        return self.active_connections / self.total_connections if self.total_connections > 0 else 0.0

class ConnectionPoolMonitor:
    """Monitor for connection pool metrics."""
    
    def __init__(self):
        self.metrics = PoolMetrics()
        self._start_times: Dict[str, float] = {}
    
    def start_connection_request(self, request_id: str):
        """Start timing a connection request."""
        self._start_times[request_id] = time.time()
    
    def record_connection_acquired(self, request_id: str, server: str):
        """Record successful connection acquisition."""
        if request_id in self._start_times:
            elapsed = time.time() - self._start_times.pop(request_id)
            self.metrics.total_wait_time += elapsed
        self.metrics.total_requests += 1
        self.metrics.active_connections += 1
        self.metrics.shard_distribution[server] = \
            self.metrics.shard_distribution.get(server, 0) + 1
    
    def record_connection_released(self):
        """Record connection being released back to pool."""
        self.metrics.active_connections -= 1
        self.metrics.idle_connections += 1
    
    def record_connection_error(self):
        """Record connection error."""
        self.metrics.connection_errors += 1
    
    def record_connection_timeout(self):
        """Record connection timeout."""
        self.metrics.connection_timeouts += 1
    
    def update_pool_size(self, total: int, active: int, idle: int):
        """Update pool size metrics."""
        self.metrics.total_connections = total
        self.metrics.active_connections = active
        self.metrics.idle_connections = idle
    
    def get_metrics(self) -> PoolMetrics:
        """Get current metrics."""
        return self.metrics
    
    def reset(self):
        """Reset all metrics."""
        self.metrics = PoolMetrics()
        self._start_times.clear()