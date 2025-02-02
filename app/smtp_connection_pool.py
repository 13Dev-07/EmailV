"""SMTP Connection Pool implementation for improved performance."""
import logging
import smtplib
import threading
import time
from typing import Dict, List, Optional, Tuple
from contextlib import contextmanager

from app.utils.smtp_metrics import (
    smtp_connection_pool_size,
    smtp_connection_wait_time,
    smtp_connection_errors,
    smtp_connection_lifetime,
    smtp_connection_reuse,
    smtp_health_check_failures
)

logger = logging.getLogger(__name__)
import threading
import time
from contextlib import contextmanager
from typing import Dict, List, Optional
import smtplib
from dataclasses import dataclass
from prometheus_client import Gauge, Histogram

# Metrics
smtp_connection_pool_size = Gauge(
    'smtp_connection_pool_size',
    'Number of connections in the SMTP connection pool',
    ['server']
)

smtp_connection_wait_time = Histogram(
    'smtp_connection_wait_time_seconds',
    'Time spent waiting for an SMTP connection'
)

@dataclass
class SMTPConnection:
    """Represents a single SMTP connection in the pool."""
    
    def __init__(self, server: str, port: int):
        self.server = server
        self.port = port
        self.connection: Optional[smtplib.SMTP] = None
        self.last_used: float = time.time()
        self.created_at: float = time.time()
        self.in_use: bool = False
        self.failed_attempts: int = 0
        
    def connect(self) -> None:
        """Establish the SMTP connection."""
        try:
            self.connection = smtplib.SMTP(self.server, self.port, timeout=10)
            self.last_used = time.time()
            self.failed_attempts = 0
        except Exception as e:
            self.failed_attempts += 1
            logger.error(f"Failed to establish SMTP connection: {str(e)}")
            raise
            
    def disconnect(self) -> None:
        """Close the SMTP connection."""
        if self.connection:
            try:
                self.connection.quit()
            except Exception:
                try:
                    self.connection.close()
                except Exception:
                    pass
            finally:
                self.connection = None
                
    def is_valid(self, max_lifetime: int, max_retries: int) -> bool:
        """Check if the connection is still valid."""
        current_time = time.time()
        return (
            not self.in_use and
            self.connection is not None and
            current_time - self.created_at <= max_lifetime and
            self.failed_attempts < max_retries
        )
        
    def mark_failed(self) -> None:
        """Mark the connection as failed."""
        self.failed_attempts += 1
        if self.connection:
            try:
                self.connection.close()
            except Exception:
                pass
            self.connection = None

class SMTPConnectionPool:
    """Thread-safe SMTP connection pool with enhanced connection management."""
    
    def __init__(self, 
                 max_connections: int = 10, 
                 connection_timeout: int = 30,
                 max_lifetime: int = 3600,  # 1 hour maximum connection lifetime
                 cleanup_interval: int = 300,  # 5 minutes
                 max_retries: int = 3):
        from monitoring.connection_pool_metrics import ConnectionPoolMonitor
        """Initialize the SMTP connection pool.
        
        Args:
            max_connections: Maximum number of connections per server
            connection_timeout: Timeout for SMTP operations in seconds
            max_lifetime: Maximum lifetime of a connection in seconds
            cleanup_interval: Interval between cleanup runs in seconds
            max_retries: Maximum number of retries per connection
        """
        self._pool: Dict[str, List[SMTPConnection]] = {}
        self._lock = threading.Lock()
        self._max_connections = max_connections
        self._connection_timeout = connection_timeout
        self._cleanup_interval = cleanup_interval
        self._last_cleanup = time.time()
        self._max_lifetime = max_lifetime
        self._max_retries = max_retries
        
        # Start background cleanup thread
        self._cleanup_thread = threading.Thread(
            target=self._periodic_cleanup,
            daemon=True
        )
        self._cleanup_thread.start()
        self._metrics = ConnectionPoolMonitor()
        
    @contextmanager
    def get_connection(self, server: str, port: int = 25) -> smtplib.SMTP:
        """Get an SMTP connection from the pool."""
        request_id = str(uuid.uuid4())
        self._metrics.start_connection_request(request_id)
        """Get an SMTP connection from the pool or create a new one with enhanced error handling."""
        connection = None
        try:
            connection = self._get_connection(server, port)
            yield connection.connection
        except Exception as e:
            if connection:
                connection.failed_attempts += 1
                if connection.failed_attempts >= self._max_retries:
                    self._remove_connection(connection)
            raise e
        finally:
            if connection and connection.failed_attempts < self._max_retries:
                self._return_connection(connection)
            
    def _get_connection(self, server: str, port: int, request_id: str) -> SMTPConnection:
        """Get an SMTP connection from the pool or create a new one."""
        start_time = time.time()
        
        with self._lock:
            self._cleanup_if_needed()
            
            # Try to get an existing valid connection
            if server in self._pool:
                for conn in self._pool[server]:
                    if conn.is_valid(self._max_lifetime, self._max_retries):
                        conn.in_use = True
                        conn.last_used = time.time()
                        smtp_connection_wait_time.observe(time.time() - start_time)
                        return conn
            
            # Create new connection if pool isn't full
            if server not in self._pool:
                self._pool[server] = []
            
            if len(self._pool[server]) < self._max_connections:
                smtp = smtplib.SMTP(timeout=self._connection_timeout)
                try:
                    smtp.connect(server, port)
                    conn = SMTPConnection(server=server, port=port)
                    conn.connection = smtp
                    conn.in_use = True
                    conn.last_used = time.time()
                    self._pool[server].append(conn)
                    smtp_connection_pool_size.labels(server=server).inc()
                    smtp_connection_wait_time.observe(time.time() - start_time)
                    return conn
                except Exception as e:
                    smtp.close()
                    raise e
            
            # Wait for a connection with exponential backoff
            wait_time = 0.1
            max_wait_time = 5.0
            while True:
                for conn in self._pool[server]:
                    if (not conn.in_use and 
                        time.time() - conn.created_at <= self._max_lifetime and
                        conn.failed_attempts < self._max_retries):
                        conn.in_use = True
                        conn.last_used = time.time()
                        smtp_connection_wait_time.observe(time.time() - start_time)
                        return conn
                time.sleep(wait_time)
                wait_time = min(wait_time * 2, max_wait_time)
    
    def _return_connection(self, connection: SMTPConnection) -> None:
        """Return a connection to the pool."""
        self._metrics.record_connection_released()
        """Return a connection to the pool with connection testing."""
        with self._lock:
            try:
                # Test the connection before returning it
                connection.connection.noop()
                connection.in_use = False
                connection.last_used = time.time()
                connection.failed_attempts = 0  # Reset failed attempts on successful return
            except Exception:
                self._remove_connection(connection)
    
    def _remove_connection(self, connection: SMTPConnection) -> None:
        """Remove a connection from the pool."""
        try:
            connection.connection.quit()
        except Exception:
            pass
        
        if connection.server in self._pool:
            self._pool[connection.server] = [
                conn for conn in self._pool[connection.server] 
                if conn is not connection
            ]
            smtp_connection_pool_size.labels(server=connection.server).dec()
    
    def _cleanup_if_needed(self) -> None:
        """Clean up old and potentially stale connections."""
        current_time = time.time()
        if current_time - self._last_cleanup < self._cleanup_interval:
            return
            
        self._last_cleanup = current_time
        
        with self._lock:
            for server in list(self._pool.keys()):
                active_connections = []
                for conn in self._pool[server]:
                    if conn.is_valid(self._max_lifetime, self._max_retries):
                        active_connections.append(conn)
                    elif not conn.in_use:
                        conn.close()
                        smtp_connection_pool_size.labels(server=server).dec()
                
                if active_connections:
                    self._pool[server] = active_connections
                else:
                    del self._pool[server]
                    
        # Schedule health check for remaining connections
        self._check_connections_health()
                
    def close_all(self) -> None:
        """Close all connections in the pool."""
        with self._lock:
            for server, connections in self._pool.items():
                for conn in connections:
                    try:
                        conn.connection.quit()
                    except Exception:
                        pass
                    smtp_connection_pool_size.labels(server=server).dec()
            self._pool.clear()