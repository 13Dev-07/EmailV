"""SMTP Connection Pool implementation with async support."""

import asyncio
import logging
import smtplib
import threading
import time
import uuid
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Dict, List, Optional, Union

from .exceptions.smtp_errors import (
    SMTPConnectionError,
    SMTPHealthCheckError,
    SMTPPoolError,
    SMTPPoolExhaustedError
)
from .monitoring.smtp_metrics import SMTPMetrics
from .monitoring.connection_pool_monitor import ConnectionPoolMonitor

logger = logging.getLogger(__name__)

@dataclass
class SMTPConnection:
    """Represents a single SMTP connection in the pool with enhanced monitoring and health checks."""

    MAX_RETRY_DELAY = 30  # Maximum retry delay in seconds
    INITIAL_RETRY_DELAY = 1  # Initial retry delay in seconds
    DEFAULT_MAX_RETRIES = 3  # Default maximum number of retry attempts
    
    def __init__(self, server: str, port: int):
        self.server = server
        self.port = port
        self.connection: Optional[smtplib.SMTP] = None
        self.last_used: float = time.time()
        self.created_at: float = time.time()
        self.in_use: bool = False
        self.failed_attempts: int = 0
        self.logger = logging.getLogger(__name__)

    async def connect(self) -> None:
        """Establish the SMTP connection with retry logic."""
        retry_count = 0
        delay = self.INITIAL_RETRY_DELAY
        last_error = None

        while retry_count < self.DEFAULT_MAX_RETRIES:
            try:
                self.connection = await asyncio.get_event_loop().run_in_executor(
                    None, 
                    lambda: smtplib.SMTP(self.server, self.port, timeout=10)
                )
                self.last_used = time.time()
                self.failed_attempts = 0
                return
            except Exception as e:
                last_error = e
                self.failed_attempts += 1
                retry_count += 1
                
                if retry_count < self.DEFAULT_MAX_RETRIES:
                    await asyncio.sleep(min(delay, self.MAX_RETRY_DELAY))
                    delay *= 2  # Exponential backoff
                
                self.logger.warning(
                    f"SMTP connection attempt {retry_count} failed for {self.server}: {str(e)}"
                )

        self.logger.error(f"Failed to establish SMTP connection after {retry_count} attempts")
        raise last_error

    async def disconnect(self) -> None:
        """Close the SMTP connection and cleanup resources."""
        if self.connection:
            try:
                await asyncio.get_event_loop().run_in_executor(
                    None,
                    self.connection.quit
                )
            except Exception as e:
                self.logger.warning(f"Error during SMTP quit: {str(e)}")
                try:
                    await asyncio.get_event_loop().run_in_executor(
                        None,
                        self.connection.close
                    )
                except Exception as e:
                    self.logger.warning(f"Error during SMTP close: {str(e)}")
            finally:
                self.connection = None
                self.last_used = time.time()

    async def is_valid(self, max_lifetime: int, max_retries: int) -> bool:
        """Check if the connection is still valid and healthy."""
        if not self.connection or self.in_use or self.failed_attempts >= max_retries:
            return False
            
        current_time = time.time()
        if current_time - self.created_at > max_lifetime:
            return False
            
        try:
            # Test connection with NOOP
            await asyncio.get_event_loop().run_in_executor(
                None,
                self.connection.noop
            )
            self.last_used = current_time
            return True
        except Exception as e:
            self.logger.warning(f"Connection health check failed: {str(e)}")
            self.failed_attempts += 1
            return False

    async def mark_failed(self) -> None:
        """Mark the connection as failed and record metrics."""
        self.failed_attempts += 1
        SMTPMetrics.record_connection_error(self.server, "ConnectionFailed")
        if self.connection:
            await self.disconnect()

class SMTPConnectionPoolAsync:
    """Async implementation of SMTP connection pool with enhanced connection management."""
    
    def __init__(self, 
                 max_connections: int = 10,
                 connection_timeout: int = 30,
                 max_lifetime: int = 3600,  # 1 hour maximum connection lifetime
                 cleanup_interval: int = 300,  # 5 minutes
                 max_retries: int = 3):
        self._pool: Dict[str, List[SMTPConnection]] = {}
        self._lock = asyncio.Lock()
        self._max_connections = max_connections
        self._connection_timeout = connection_timeout
        self._cleanup_interval = cleanup_interval
        self._max_lifetime = max_lifetime
        self._max_retries = max_retries
        self._last_cleanup = time.time()
        self._metrics = ConnectionPoolMonitor()
        self._cleanup_task = None
        self.logger = logging.getLogger(__name__)

    async def start(self):
        """Start the connection pool and periodic cleanup."""
        self._cleanup_task = asyncio.create_task(self._periodic_cleanup())

    async def stop(self):
        """Stop the connection pool and cleanup."""
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass
        await self.close_all()

    @asynccontextmanager
    async def get_connection(self, server: str, port: int = 25):
        """Get an SMTP connection from the pool and return it as a context manager."""
        connection = None
        request_id = str(uuid.uuid4())
        
        try:
            connection = await self._get_connection(server, port, request_id)
            yield connection.connection
        except Exception as e:
            if connection:
                connection.failed_attempts += 1
                if connection.failed_attempts >= self._max_retries:
                    await self._remove_connection(connection)
                SMTPMetrics.record_connection_error(server, type(e).__name__)
            raise
        finally:
            if connection and connection.failed_attempts < self._max_retries:
                await self._return_connection(connection)

    async def _periodic_cleanup(self):
        """Run cleanup periodically."""
        while True:
            try:
                await asyncio.sleep(self._cleanup_interval)
                await self._cleanup_if_needed()
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in periodic cleanup: {str(e)}")

    async def _cleanup_if_needed(self):
        """Clean up old and potentially stale connections."""
        current_time = time.time()
        if current_time - self._last_cleanup < self._cleanup_interval:
            return
            
        self._last_cleanup = current_time
        
        async with self._lock:
            for server in list(self._pool.keys()):
                active_connections = []
                for conn in self._pool[server]:
                    if await conn.is_valid(self._max_lifetime, self._max_retries):
                        active_connections.append(conn)
                    else:
                        await conn.disconnect()
                        SMTPMetrics.update_pool_size(server, "total", -1)
                
                if active_connections:
                    self._pool[server] = active_connections
                else:
                    del self._pool[server]

    async def close_all(self):
        """Close all connections in the pool."""
        self.logger.info("Shutting down SMTP connection pool")
        async with self._lock:
            for server, connections in self._pool.items():
                for conn in connections:
                    try:
                        await conn.disconnect()
                    except Exception as e:
                        self.logger.warning(f"Error closing connection: {str(e)}")
            self._pool.clear()
        self.logger.info("SMTP connection pool shutdown complete")