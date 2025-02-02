"""Unit tests for SMTP health checks."""
import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta

from app.monitoring.smtp_health_check import SMTPHealthChecker
from app.smtp_connection_pool import SMTPConnection

@pytest.fixture
def health_checker():
    return SMTPHealthChecker()

@pytest.fixture
def mock_connection():
    conn = SMTPConnection("test.smtp.com", 587)
    conn.connection = Mock()
    return conn

async def test_check_healthy_connection(health_checker, mock_connection):
    """Test health check for healthy connection."""
    mock_connection.connection.noop.return_value = None
    
    result = await health_checker.check_connection(mock_connection)
    
    assert result is True
    mock_connection.connection.noop.assert_called_once()

async def test_check_unhealthy_connection(health_checker, mock_connection):
    """Test health check for unhealthy connection."""
    mock_connection.connection.noop.side_effect = Exception("Connection lost")
    
    result = await health_checker.check_connection(mock_connection)
    
    assert result is False
    mock_connection.connection.noop.assert_called_once()

async def test_verify_valid_connection_settings(health_checker, mock_connection):
    """Test verification of valid connection settings."""
    mock_connection.connection.host = mock_connection.server
    mock_connection.connection.port = mock_connection.port
    mock_connection.in_use = False
    
    result = await health_checker.verify_connection_settings(mock_connection)
    
    assert result is True

async def test_verify_invalid_connection_settings(health_checker, mock_connection):
    """Test verification of invalid connection settings."""
    mock_connection.connection.host = "wrong.server.com"
    
    result = await health_checker.verify_connection_settings(mock_connection)
    
    assert result is False