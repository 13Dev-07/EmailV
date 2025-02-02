"""Enhanced metrics collection for detailed performance monitoring."""

from typing import Dict, List
from prometheus_client import Counter, Histogram, Gauge
from functools import wraps
import time

# Validation Pipeline Metrics
VALIDATION_STEPS = Histogram(
    "email_validation_step_duration_seconds",
    "Duration of each validation step",
    ["step_name"],
    buckets=(0.001, 0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0)
)

VALIDATION_STEP_FAILURES = Counter(
    "email_validation_step_failures_total",
    "Number of failures per validation step",
    ["step_name", "error_type"]
)

# DNS Resolution Metrics
DNS_RESOLUTION_TIME = Histogram(
    "dns_resolution_duration_seconds",
    "DNS resolution duration",
    ["record_type", "cached"],
    buckets=(0.001, 0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0)
)

DNS_FAILURES = Counter(
    "dns_resolution_failures_total",
    "Number of DNS resolution failures",
    ["record_type", "error_type"]
)

# SMTP Connection Metrics
SMTP_CONNECTION_POOL_SIZE = Gauge(
    "smtp_connection_pool_size",
    "Current number of connections in the SMTP pool",
    ["status"]  # active, idle, total
)

SMTP_CONNECTION_TIME = Histogram(
    "smtp_connection_duration_seconds",
    "SMTP connection establishment duration",
    buckets=(0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0)
)

# Cache Performance Metrics
CACHE_OPERATIONS = Counter(
    "cache_operations_total",
    "Cache operations count",
    ["operation", "status"]
)

CACHE_SIZE = Gauge(
    "cache_size_bytes",
    "Current cache size in bytes"
)

# Rate Limiting Metrics
RATE_LIMIT_REMAINING = Gauge(
    "rate_limit_remaining",
    "Remaining rate limit quota",
    ["endpoint"]
)

def track_validation_step(step_name: str):
    """Decorator to track validation step performance."""
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                VALIDATION_STEPS.labels(step_name=step_name).observe(
                    time.time() - start_time
                )
                return result
            except Exception as e:
                VALIDATION_STEP_FAILURES.labels(
                    step_name=step_name,
                    error_type=e.__class__.__name__
                ).inc()
                raise
        return async_wrapper
    return decorator

class EnhancedMetricsCollector:
    """Collects and manages enhanced metrics."""
    
    @staticmethod
    def record_validation_step(step_name: str, duration: float):
        VALIDATION_STEPS.labels(step_name=step_name).observe(duration)
    
    @staticmethod
    def record_dns_resolution(record_type: str, duration: float, cached: bool):
        DNS_RESOLUTION_TIME.labels(
            record_type=record_type,
            cached=str(cached)
        ).observe(duration)
    
    @staticmethod
    def record_dns_failure(record_type: str, error_type: str):
        DNS_FAILURES.labels(
            record_type=record_type,
            error_type=error_type
        ).inc()
    
    @staticmethod
    def update_smtp_pool_metrics(active: int, idle: int):
        SMTP_CONNECTION_POOL_SIZE.labels(status="active").set(active)
        SMTP_CONNECTION_POOL_SIZE.labels(status="idle").set(idle)
        SMTP_CONNECTION_POOL_SIZE.labels(status="total").set(active + idle)
    
    @staticmethod
    def record_cache_operation(operation: str, status: str):
        CACHE_OPERATIONS.labels(
            operation=operation,
            status=status
        ).inc()
    
    @staticmethod
    def update_cache_size(size_bytes: int):
        CACHE_SIZE.set(size_bytes)
    
    @staticmethod
    def update_rate_limit(endpoint: str, remaining: int):
        RATE_LIMIT_REMAINING.labels(endpoint=endpoint).set(remaining)