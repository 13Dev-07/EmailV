"""Unit tests for connection pool monitoring."""

import pytest
from unittest.mock import Mock
import time

from app.monitoring.connection_pool_monitor import ConnectionPoolMonitor

@pytest.fixture
def monitor():
    return ConnectionPoolMonitor()

def test_connection_request_tracking(monitor):
    """Test connection request timing tracking."""
    request_id = "test-123"
    server = "smtp.test.com"
    
    # Start request
    monitor.start_connection_request(request_id)
    time.sleep(0.1)  # Simulate some work
    
    # Complete request
    monitor.complete_connection_request(request_id, server)
    
    # Request ID should be removed
    assert request_id not in monitor._request_start_times

def test_connection_lifecycle_metrics(monitor):
    """Test connection lifecycle metric recording."""
    server = "smtp.test.com"
    
    # Add connection
    monitor.record_connection_added(server)
    
    # Acquire connection
    monitor.record_connection_acquired()
    
    # Release connection
    monitor.record_connection_released()
    
    # Remove connection
    monitor.record_connection_removed()

def test_error_recording(monitor):
    """Test error recording."""
    server = "smtp.test.com"
    error_type = "ConnectionTimeout"
    
    monitor.record_connection_error(server, error_type)