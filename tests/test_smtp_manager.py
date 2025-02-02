"""Tests for SMTP connection management system."""

import pytest
from unittest.mock import Mock, patch
import asyncio

from app.monitoring.health_manager import HealthManager
from app.monitoring.smtp_health_check import SMTPHealthChecker
from app.smtp_connection_pool import SMTPConnectionPool, SMTPConnection

@pytest.fixture
def health_manager():
    manager = HealthManager(check_interval=1)
    yield manager
    manager.stop()

@pytest.fixture
def connection_pool():
    pool = SMTPConnectionPool(
        max_connections=2,
        cleanup_interval=1
    )
    yield pool
    pool.close_all()

async def test_health_check_integration(health_manager, connection_pool):
    """Test integration between health manager and connection pool."""
    server = "test.smtp.com"
    port = 587

    with patch('smtplib.SMTP') as mock_smtp:
        # Create a test connection
        conn = SMTPConnection(server, port)
        connection_pool._pool[f"{server}:{port}"] = [conn]

        # Set up mock behavior
        mock_smtp.return_value.noop.side_effect = Exception("Connection failed")
        conn.connection = mock_smtp.return_value

        # Run health check
        await health_manager._check_server(server)

        # Verify connection was removed due to health check failure
        assert len(connection_pool._pool) == 0

async def test_connection_lifecycle_with_health_checks(health_manager, connection_pool):
    """Test full connection lifecycle with health monitoring."""
    server = "test.smtp.com"
    
    with patch('smtplib.SMTP') as mock_smtp:
        # Create and acquire connection
        async with connection_pool.get_connection(server) as conn:
            assert conn is not None
            assert conn.noop.call_count == 0

        # Verify health check
        await health_manager._check_server(server)
        
        # Connection should still be in pool if healthy
        assert f"{server}:25" in connection_pool._pool

async def test_failed_server_tracking(health_manager):
    """Test tracking of failed servers."""
    server = "bad.smtp.com"
    
    # Mark server as failed
    health_manager.mark_server_failed(server)
    assert not health_manager.is_server_healthy(server)
    
    # Simulate successful health check
    with patch.object(SMTPHealthChecker, 'check_server', return_value=True):
        await health_manager._check_server(server)
        assert health_manager.is_server_healthy(server)

async def test_cleanup_with_failed_health_checks(connection_pool):
    """Test cleanup behavior with failed health checks."""
    server = "test.smtp.com"
    port = 587
    
    # Add test connection
    conn = SMTPConnection(server, port)
    connection_pool._pool[f"{server}:{port}"] = [conn]
    
    # Simulate failed health check during cleanup
    with patch.object(SMTPConnection, 'is_valid', return_value=False):
        await connection_pool._cleanup_if_needed()
        
    # Pool should be empty after cleanup
    assert len(connection_pool._pool) == 0