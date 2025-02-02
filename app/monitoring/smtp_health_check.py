"""SMTP connection health checking implementation."""

import asyncio
import logging
from typing import Optional
from datetime import datetime

from prometheus_client import Counter, Gauge, Histogram

# Metrics
SMTP_HEALTH_CHECK_DURATION = Histogram(
    'smtp_health_check_duration_seconds',
    'Duration of SMTP health checks'
)

SMTP_HEALTH_CHECK_FAILURES = Counter(
    'smtp_health_check_failures_total',
    'Number of failed SMTP health checks',
    ['server', 'error_type']
)

SMTP_LAST_CHECK_TIME = Gauge(
    'smtp_last_health_check_timestamp',
    'Timestamp of last health check per server',
    ['server']
)

class SMTPHealthChecker:
    """Performs health checks on SMTP connections."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    async def check_connection(self, connection) -> bool:
        """
        Perform a health check on an SMTP connection.
        
        Args:
            connection: The SMTPConnection instance to check
            
        Returns:
            bool: True if connection is healthy, False otherwise
        """
        start_time = datetime.now()
        try:
            # Basic NOOP command to test connection
            connection.connection.noop()
            
            # Record successful check
            duration = (datetime.now() - start_time).total_seconds()
            SMTP_HEALTH_CHECK_DURATION.observe(duration)
            SMTP_LAST_CHECK_TIME.labels(server=connection.server).set_to_current_time()
            
            return True
            
        except Exception as e:
            # Record failure with specific error type
            error_type = type(e).__name__
            SMTP_HEALTH_CHECK_FAILURES.labels(
                server=connection.server,
                error_type=error_type
            ).inc()
            
            self.logger.warning(
                f"Health check failed for SMTP connection to {connection.server}: {str(e)}"
            )
            return False

    async def verify_connection_settings(self, connection) -> bool:
        """
        Verify connection settings are still valid.
        
        Args:
            connection: The SMTPConnection instance to verify
            
        Returns:
            bool: True if settings are valid, False otherwise
        """
        try:
            # Verify connection parameters still match configuration
            if not connection.connection:
                return False
                
            # Check if the connection settings match current expectations
            settings_ok = (
                connection.server == connection.connection.host and
                connection.port == connection.connection.port and
                not connection.in_use
            )
            
            if not settings_ok:
                self.logger.warning(
                    f"Connection settings mismatch for {connection.server}:{connection.port}"
                )
                return False
                
            return True
        except Exception as e:
            self.logger.error(f"Connection settings verification failed: {str(e)}")
            return False