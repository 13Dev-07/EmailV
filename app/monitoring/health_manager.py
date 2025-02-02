"""Health check management for connection pools."""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, Set

from .smtp_health_check import SMTPHealthChecker
from ..exceptions.connection_errors import HealthCheckError

class HealthManager:
    """Manages health checks for connection pools."""
    
    def __init__(self, check_interval: int = 300):
        self.check_interval = check_interval
        self.logger = logging.getLogger(__name__)
        self._last_checks: Dict[str, datetime] = {}
        self._failed_servers: Set[str] = set()
        self._checker = SMTPHealthChecker()
        self._is_running = False
        
    async def start(self):
        """Start the health check manager."""
        self._is_running = True
        while self._is_running:
            try:
                await self._run_checks()
            except Exception as e:
                self.logger.error(f"Error during health checks: {str(e)}")
            finally:
                await asyncio.sleep(self.check_interval)
                
    def stop(self):
        """Stop the health check manager."""
        self._is_running = False
        
    def mark_server_failed(self, server: str):
        """Mark a server as failed."""
        self._failed_servers.add(server)
        
    def is_server_healthy(self, server: str) -> bool:
        """Check if a server is considered healthy."""
        return server not in self._failed_servers
        
    async def _run_checks(self):
        """Run health checks on all tracked connections."""
        current_time = datetime.now()
        for server, last_check in list(self._last_checks.items()):
            if current_time - last_check >= timedelta(seconds=self.check_interval):
                await self._check_server(server)
                
    async def _check_server(self, server: str):
        """Check health of a specific server."""
        try:
            is_healthy = await self._checker.check_server(server)
            if is_healthy and server in self._failed_servers:
                self._failed_servers.remove(server)
            elif not is_healthy:
                self.mark_server_failed(server)
        except Exception as e:
            self.logger.error(f"Health check failed for {server}: {str(e)}")
            self.mark_server_failed(server)
        finally:
            self._last_checks[server] = datetime.now()