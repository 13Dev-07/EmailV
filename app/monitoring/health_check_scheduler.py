"""Scheduler for periodic health checks of connections."""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class HealthCheckScheduler:
    """Schedules and manages health checks for connection pools."""
    
    def __init__(self, check_interval: int = 300):
        """
        Initialize the health check scheduler.
        
        Args:
            check_interval: Time between health checks in seconds
        """
        self.check_interval = check_interval
        self.logger = logging.getLogger(__name__)
        self._last_check = {}
        self._is_running = False
        
    async def start(self):
        """Start the health check scheduler."""
        self._is_running = True
        while self._is_running:
            try:
                await self._run_checks()
            except Exception as e:
                self.logger.error(f"Error during health checks: {str(e)}")
            finally:
                await asyncio.sleep(self.check_interval)
                
    def stop(self):
        """Stop the health check scheduler."""
        self._is_running = False
        
    async def _run_checks(self):
        """Run health checks on all registered pools."""
        current_time = datetime.now()
        for pool_id, last_check in self._last_check.items():
            if current_time - last_check >= timedelta(seconds=self.check_interval):
                await self._check_pool(pool_id)
                self._last_check[pool_id] = current_time
                
    async def _check_pool(self, pool_id: str):
        """Run health checks for a specific pool."""
        from .smtp_health_check import SMTPHealthChecker
        
        checker = SMTPHealthChecker()
        pool = self._pools.get(pool_id)
        
        if not pool:
            return
            
        for connection in pool.get_all_connections():
            is_healthy = await checker.check_connection(connection)
            if not is_healthy:
                settings_valid = await checker.verify_connection_settings(connection)
                if not settings_valid:
                    await pool.remove_connection(connection)
            
        self._last_check[pool_id] = datetime.now()