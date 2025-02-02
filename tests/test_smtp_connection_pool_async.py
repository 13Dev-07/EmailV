"""Unit tests for async SMTP connection pool."""

import pytest
import asyncio
from unittest.mock import Mock, patch
from app.smtp_connection_pool_async import SMTPConnectionPoolAsync, SMTPConnection

@pytest.fixture
async def connection_pool():
    pool = SMTPConnectionPoolAsync(
        max_connections=2,
        connection_timeout=1,
        max_lifetime=5,
        cleanup_interval=1
    )
    await pool.start()
    yield pool
    await pool.stop()

@pytest.fixture
def mock_smtp():
    with patch('smtplib.SMTP') as mock:
        yield mock

async def test_connection_lifecycle(connection_pool, mock_smtp):
    """Test basic connection lifecycle."""
    server = "test.smtp.com"
    port = 587
    
    async with connection_pool.get_connection(server, port) as conn:
        assert conn is not None
        mock_smtp.assert_called_once_with(server, port, timeout=10)
        
    # Check connection was returned to pool
    assert len(connection_pool._pool[f"{server}:{port}"]) == 1

async def test_connection_cleanup(connection_pool, mock_smtp):
    """Test connection cleanup."""
    server = "test.smtp.com"
    port = 587

    # Add an expired connection
    conn = SMTPConnection(server, port)
    conn.created_at = 0  # Force connection to be expired
    connection_pool._pool[f"{server}:{port}"] = [conn]

    # Run cleanup
    await connection_pool._cleanup_if_needed()

    # Pool should be empty after cleanup
    assert f"{server}:{port}" not in connection_pool._pool

async def test_connection_retry(connection_pool, mock_smtp):
    """Test connection retry logic."""
    mock_smtp.side_effect = [Exception("Connection failed"), Mock()]
    
    async with connection_pool.get_connection("test.smtp.com") as conn:
        assert conn is not None
    
    assert mock_smtp.call_count == 2

async def test_pool_exhaustion(connection_pool):
    """Test pool exhaustion handling."""
    server = "test.smtp.com"
    
    # Fill up the pool
    async with connection_pool.get_connection(server):
        async with connection_pool.get_connection(server):
            with pytest.raises(SMTPPoolExhaustedError):
                async with connection_pool.get_connection(server):
                    pass