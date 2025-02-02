"""SMTP Connection Pool implementation for improved performance."""

import asyncio
import logging
import smtplib
import threading
import time
import uuid
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Dict, List, Optional, Union

from .exceptions.smtp_errors import (
    SMTPConnectionError,
    SMTPHealthCheckError,
    SMTPPoolError,
    SMTPPoolExhaustedError
)
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
    """Represents a single SMTP connection in the pool with enhanced monitoring and health checks."""

    MAX_RETRY_DELAY = 30  # Maximum retry delay in seconds
    INITIAL_RETRY_DELAY = 1  # Initial retry delay in seconds
    DEFAULT_MAX_RETRIES = 3  # Default maximum number of retry attempts
    
    def __init__(self, server: str, port: int):
        """Initialize a new SMTP connection object.
        
        Args:
            server: SMTP server hostname
            port: SMTP server port
        """
        self.server = server
        self.port = port
        self.connection: Optional[smtplib.SMTP] = None
        self.last_used: float = time.time()
        self.created_at: float = time.time()
        self.in_use: bool = False
        self.failed_attempts: int = 0
        self.last_health_check: float = time.time()
        self.logger = logging.getLogger(__name__)
        
    def connect(self) -> None:
        """Establish the SMTP connection with retry logic and exponential backoff."""
        retry_count = 0
        current_delay = self.INITIAL_RETRY_DELAY
        last_error = None
        
        while retry_count < self.DEFAULT_MAX_RETRIES:
            try:
                if self.connection:
                    try:
                        self.connection.quit()
                    except Exception:
                        pass
                self.connection = smtplib.SMTP(timeout=30)
                self.connection.connect(self.server, self.port)
                self.connection.noop()  # Verify connection is responsive
                self.last_used = time.time()
                self.last_health_check = time.time()
                self.failed_attempts = 0
                return
            except (socket.gaierror, socket.timeout, smtplib.SMTPException) as e:
                last_error = str(e)
                retry_count += 1
                self.failed_attempts += 1
                if retry_count >= self.DEFAULT_MAX_RETRIES:
                    self.logger.error(f"Failed to connect after {retry_count} attempts: {last_error}")
                    raise ConnectionError(f"Failed to connect after {retry_count} attempts: {last_error}")
                self.logger.warning(f"Connection attempt {retry_count} failed: {last_error}")
                time.sleep(min(current_delay, self.MAX_RETRY_DELAY))
                current_delay *= 2
            # No additional retry logic needed here as it's handled above
                last_error = e
                self.failed_attempts += 1
                retry_count += 1
                
                if retry_count < self.DEFAULT_MAX_RETRIES:
                    time.sleep(min(delay, self.MAX_RETRY_DELAY))
                    delay *= 2  # Exponential backoff
                
                self.logger.warning(
                    f"SMTP connection attempt {retry_count} failed for {self.server}: {str(e)}"
                )

        self.logger.error(f"Failed to establish SMTP connection after {retry_count} attempts")
        raise last_error
        self.connection = None
            
    def disconnect(self) -> None:
        """Close the SMTP connection and cleanup resources."""
        if self.connection:
            try:
                self.connection.quit()
            except Exception as e:
                self.logger.warning(f"Error during SMTP quit: {str(e)}")
                try:
                    self.connection.close()
                except Exception as e:
                    self.logger.warning(f"Error during SMTP close: {str(e)}")
            finally:
                self.connection = None
                self.last_used = time.time()
                
    def is_valid(self, max_lifetime: int, max_retries: int) -> bool:
        """Check if the connection is still valid and healthy."""
        if not self.connection or self.in_use or self.failed_attempts >= max_retries:
            return False
            
        current_time = time.time()
        if current_time - self.created_at > max_lifetime:
            return False
        
        # Perform health check
        try:
            self.connection.noop()
            self.last_health_check = current_time
            return True
        except (smtplib.SMTPServerDisconnected, smtplib.SMTPException) as e:
            self.logger.warning(f"Health check failed: {str(e)}")
            self.failed_attempts += 1
            return False
        
    def mark_failed(self) -> None:
        """Mark the connection as failed and record metrics."""
        from .monitoring.smtp_metrics import SMTPMetrics
        
        self.failed_attempts += 1
        SMTPMetrics.record_connection_error(self.server, "ConnectionFailed")
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
                 max_retries: int = 3,
                 wait_timeout: int = 30):  # Maximum time to wait for connection
        """Initialize the SMTP connection pool.
        
        Args:
            max_connections: Maximum number of connections per server
            connection_timeout: Timeout for SMTP operations in seconds
            max_lifetime: Maximum lifetime of a connection in seconds
            cleanup_interval: Interval between cleanup runs in seconds
            max_retries: Maximum number of retries per connection
        """
        from monitoring.connection_pool_metrics import ConnectionPoolMonitor
        self._pool: Dict[str, List[SMTPConnection]] = {}
        self._lock = threading.Lock()
        self._max_connections = max_connections
        self._connection_timeout = connection_timeout
        self._cleanup_interval = cleanup_interval
        self._max_lifetime = max_lifetime
        self._max_retries = max_retries
        self._wait_timeout = wait_timeout
        self._last_cleanup = time.time()
        self.logger = logging.getLogger(__name__)
        
        # Start background cleanup thread
        self._cleanup_thread = threading.Thread(
            target=self._periodic_cleanup,
            daemon=True
        )
        self._cleanup_thread.start()
        self._metrics = ConnectionPoolMonitor()
        
    @contextmanager
    def get_connection(self, server: str, port: int = 25):
        """Get an SMTP connection from the pool and return it as a context manager."""
        connection = None
        request_id = str(uuid.uuid4())
        
        try:
            connection = self._get_connection(server, port, request_id)
            yield connection.connection
        except Exception as e:
            if connection:
                connection.failed_attempts += 1
                if connection.failed_attempts >= self._max_retries:
                    self._remove_connection(connection)
                    SMTPMetrics.record_connection_error(server, type(e).__name__)
            raise
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
                # Create new connection with proper error handling and metrics
                try:
                    smtp = smtplib.SMTP(timeout=self._connection_timeout)
                    smtp.connect(server, port)
                    conn = SMTPConnection(server=server, port=port)
                    conn.connection = smtp
                    # Validate connection before adding to pool
                    smtp.noop()
                    conn.in_use = True
                    conn.last_used = time.time()
                    self._pool[server].append(conn)
                    smtp_connection_pool_size.labels(server=server).inc()
                    smtp_connection_wait_time.observe(time.time() - start_time)
                    return conn
                except (socket.gaierror, socket.timeout, smtplib.SMTPException) as e:
                    self.logger.error(f"Failed to create SMTP connection: {str(e)}")
                    smtp_connection_failures.labels(server=server, error=str(e)).inc()
                    smtp_connection_wait_time.observe(time.time() - start_time)
                    if 'smtp' in locals():
                        try:
                            smtp.close()
                        except Exception:
                            pass
                    raise ConnectionError(f"SMTP connection failed: {str(e)}")
                except Exception as e:
                    self.logger.error(f"Unexpected error creating SMTP connection: {str(e)}")
                    if 'smtp' in locals():
                        try:
                            smtp.close()
                        except Exception:
                            pass
                    raise ConnectionError(f"Unexpected SMTP connection error: {str(e)}")
            
            # Wait for a connection with timeout
            start_wait = time.time()
            wait_time = 0.1  # Initial wait time
            while time.time() - start_wait < self._wait_timeout:
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
        """Return a connection to the pool with connection testing and metrics."""
        from .monitoring.smtp_metrics import SMTPMetrics
        with self._lock:
            try:
                # Test the connection before returning it
                connection.connection.noop()
                connection.in_use = False
                connection.last_used = time.time()
                connection.failed_attempts = 0  # Reset failed attempts on successful return
                SMTPMetrics.update_pool_size(connection.server, "idle", 1)
            except Exception as e:
                self.logger.warning(f"Connection test failed during return: {str(e)}")
                SMTPMetrics.record_connection_error(connection.server, type(e).__name__)
                self._remove_connection(connection)
            finally:
                self._metrics.record_connection_released()
    
    def _remove_connection(self, connection: SMTPConnection) -> None:
        """Remove a connection from the pool and clean up resources."""
        try:
            connection.disconnect()
        except Exception as e:
            self.logger.warning(f"Error disconnecting SMTP connection: {str(e)}")
        finally:
            with self._lock:
                server_key = f"{connection.server}:{connection.port}"
                if server_key in self._pool:
                    self._pool[server_key].remove(connection)
                    if not self._pool[server_key]:
                        del self._pool[server_key]
                self._metrics.record_connection_removed()
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
    
    def get_all_connections(self) -> List[SMTPConnection]:
        """Get all connections in the pool."""
        with self._lock:
            all_connections = []
            for connections in self._pool.values():
                all_connections.extend(connections)
            return all_connections

    def _cleanup_if_needed(self) -> None:
        """Clean up old and potentially stale connections with enhanced health checks."""
        from .monitoring.smtp_health_check import SMTPHealthChecker
        from .monitoring.smtp_metrics import SMTPMetrics
        
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
                        try:
                            conn.disconnect()
                            smtp_connection_pool_size.labels(server=server).dec()
                            smtp_connection_failures.labels(
                                server=server,
                                error="stale_connection"
                            ).inc()
                        except Exception as e:
                            self.logger.error(f"Error cleaning up connection: {e}")
                
                if active_connections:
                    self._pool[server] = active_connections
                else:
                    del self._pool[server]
                    
        # Schedule health check for remaining connections
        self._check_connections_health()
                
    def close_all(self) -> None:
        """Close all connections in the pool and clean up resources."""
        from .monitoring.smtp_metrics import SMTPMetrics
        
        self.logger.info("Shutting down SMTP connection pool")
        with self._lock:
            for server, connections in self._pool.items():
                for conn in connections:
                    try:
                        conn.connection.quit()
                    except Exception:
                        pass
                    smtp_connection_pool_size.labels(server=server).dec()
            self._pool.clear()