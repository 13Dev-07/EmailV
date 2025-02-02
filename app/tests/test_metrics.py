"""Tests for Prometheus metrics implementation."""

import pytest
import time
from unittest.mock import AsyncMock, patch
from prometheus_client import REGISTRY
from app.monitoring.prometheus_metrics import (
    MetricsCollector,
    MetricsMiddleware,
    track_time,
    EMAIL_VALIDATION_TOTAL,
    DNS_LOOKUP_TOTAL,
    SMTP_CONNECTIONS_TOTAL,
    reset_metrics
)

@pytest.fixture(autouse=True)
def clear_metrics():
    """Clear all metrics before each test."""
    reset_metrics()
    yield

@pytest.fixture
def metrics_collector():
    return MetricsCollector()

@pytest.fixture
def metrics_middleware():
    return MetricsMiddleware()

def test_validation_metrics(metrics_collector):
    # Record some validation results
    metrics_collector.record_validation_result(True)
    metrics_collector.record_validation_result(False)
    metrics_collector.record_validation_result(True)
    
    # Check metric values
    valid_count = EMAIL_VALIDATION_TOTAL.labels(result="valid")._value.get()
    invalid_count = EMAIL_VALIDATION_TOTAL.labels(result="invalid")._value.get()
    
    assert valid_count == 2
    assert invalid_count == 1

def test_dns_lookup_metrics(metrics_collector):
    # Record some DNS lookups
    metrics_collector.record_dns_lookup("MX", True)
    metrics_collector.record_dns_lookup("A", False)
    metrics_collector.record_dns_lookup("MX", True)
    
    # Check metric values
    mx_success = DNS_LOOKUP_TOTAL.labels(record_type="MX", result="success")._value.get()
    a_failure = DNS_LOOKUP_TOTAL.labels(record_type="A", result="failure")._value.get()
    
    assert mx_success == 2
    assert a_failure == 1

def test_smtp_connection_metrics(metrics_collector):
    # Record some SMTP connections
    metrics_collector.record_smtp_connection(True)
    metrics_collector.record_smtp_connection(False)
    metrics_collector.record_smtp_connection(True)
    
    # Check metric values
    success_count = SMTP_CONNECTIONS_TOTAL.labels(result="success")._value.get()
    failure_count = SMTP_CONNECTIONS_TOTAL.labels(result="failure")._value.get()
    
    assert success_count == 2
    assert failure_count == 1

@pytest.mark.asyncio
async def test_timing_decorator():
    # Test function with timing decorator
    @track_time(EMAIL_VALIDATION_DURATION.labels(validation_type="test"))
    async def test_func():
        await asyncio.sleep(0.1)
        return "test"
    
    # Execute function
    result = await test_func()
    
    # Verify timing was recorded
    assert result == "test"
    assert EMAIL_VALIDATION_DURATION.labels(validation_type="test")._sum.get() > 0

@pytest.mark.asyncio
async def test_metrics_middleware(metrics_middleware):
    # Mock request and response
    mock_request = AsyncMock()
    mock_request.url.path = "/test"
    mock_request.method = "GET"
    
    mock_response = AsyncMock()
    mock_response.status_code = 200
    
    async def mock_call_next(_):
        await asyncio.sleep(0.1)
        return mock_response
    
    # Process request through middleware
    response = await metrics_middleware(mock_request, mock_call_next)
    
    # Verify response and metrics
    assert response == mock_response
    # Request duration should be recorded
    assert any(
        "request_duration_seconds" in str(metric)
        for metric in REGISTRY.collect()
    )