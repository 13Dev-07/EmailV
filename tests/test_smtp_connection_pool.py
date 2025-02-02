"""Unit tests for SMTP connection pool."""
import pytest
import time
from unittest.mock import Mock, patch
from app.smtp_connection_pool import SMTPConnection, SMTPConnectionPool

@pytest.fixture
def mock_smtp():
    with patch('smtplib.SMTP') as mock:
        yield mock

@pytest.fixture
def connection_pool():
    pool = SMTPConnectionPool(
        max_connections=2,
        connection_timeout=1,
        max_lifetime=5,
        cleanup_interval=1
    )
    yield pool
    pool.close_all()

async def test_connection_lifecycle(connection_pool, mock_smtp):
    """Test basic connection lifecycle."""
    server = "test.smtp.com"
    port = 587
    
    async with connection_pool.get_connection(server, port) as conn:
        assert conn is not None
        mock_smtp.assert_called_once_with(server, port, timeout=10)
        
    # Check connection was returned to pool
    assert len(connection_pool._pool[f"{server}:{port}"]) == 1
    
async def test_connection_retry(connection_pool, mock_smtp):
    """Test connection retry logic."""
    mock_smtp.side_effect = [Exception("Connection failed"), Mock()]
    
    async with connection_pool.get_connection("test.smtp.com") as conn:
        assert conn is not None
    
    assert mock_smtp.call_count == 2

async def test_connection_health_check(connection_pool, mock_smtp):
    """Test connection health checking."""
    server = "test.smtp.com"
    conn = SMTPConnection(server, 587)
    connection_pool._pool[f"{server}:587"] = [conn]
    
    # Simulate failed health check
    conn.connection = Mock()
    conn.connection.noop.side_effect = Exception("Connection lost")
    
    await connection_pool._check_connections_health()
    
    assert len(connection_pool._pool) == 0  # Bad connection removed