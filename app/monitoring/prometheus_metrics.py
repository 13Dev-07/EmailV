"""Prometheus metrics configuration and collection."""

from prometheus_client import Counter, Histogram, Gauge, Info
from functools import wraps
import time
from typing import Callable, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

# Email validation metrics
EMAIL_VALIDATION_TOTAL = Counter(
    'email_validation_total',
    'Total number of email validation requests',
    ['result']  # valid/invalid
)

EMAIL_VALIDATION_DURATION = Histogram(
    'email_validation_duration_seconds',
    'Time spent validating email addresses',
    ['validation_type']  # syntax/dns/smtp
)

VALIDATION_ERRORS = Counter(
    'email_validation_errors_total',
    'Total number of validation errors by type',
    ['error_type']
)

# DNS metrics
DNS_LOOKUP_TOTAL = Counter(
    'dns_lookup_total',
    'Total number of DNS lookups',
    ['record_type', 'result']  # MX/A/AAAA, success/failure
)

DNS_LOOKUP_DURATION = Histogram(
    'dns_lookup_duration_seconds',
    'Time spent on DNS lookups',
    ['record_type']
)

DNS_CACHE_HITS = Counter(
    'dns_cache_hits_total',
    'Total number of DNS cache hits',
    ['record_type']
)

DNS_CACHE_MISSES = Counter(
    'dns_cache_misses_total',
    'Total number of DNS cache misses',
    ['record_type']
)

# SMTP metrics
SMTP_CONNECTIONS_TOTAL = Counter(
    'smtp_connections_total',
    'Total number of SMTP connections attempted',
    ['result']  # success/failure
)

SMTP_VERIFICATION_DURATION = Histogram(
    'smtp_verification_duration_seconds',
    'Time spent on SMTP verification',
    ['status']  # success/failure
)

ACTIVE_SMTP_CONNECTIONS = Gauge(
    'active_smtp_connections',
    'Number of active SMTP connections'
)

SMTP_CONNECTION_ERRORS = Counter(
    'smtp_connection_errors_total',
    'Total number of SMTP connection errors by type',
    ['error_type']
)

# Redis metrics
REDIS_OPERATIONS_TOTAL = Counter(
    'redis_operations_total',
    'Total number of Redis operations',
    ['operation', 'result']  # get/set/etc, success/failure
)

REDIS_OPERATION_DURATION = Histogram(
    'redis_operation_duration_seconds',
    'Time spent on Redis operations',
    ['operation']
)

REDIS_CONNECTIONS = Gauge(
    'redis_connections',
    'Number of active Redis connections'
)

# Rate limiting metrics
RATE_LIMIT_EXCEEDED = Counter(
    'rate_limit_exceeded_total',
    'Total number of rate limit exceeded events',
    ['endpoint']
)

# System info
SYSTEM_INFO = Info('email_validator', 'Email validator system information')

@dataclass
class MetricsContext:
    """Context for tracking metrics."""
    start_time: float = 0.0
    error_type: str = ""
    validation_type: str = ""
    operation_type: str = ""
    is_success: bool = True

def track_time(metric: Histogram) -> Callable:
    """
    Decorator to track execution time of a function.
    
    Args:
        metric: Prometheus histogram to record timing.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                duration = time.time() - start_time
                metric.observe(duration)
                return result
            except Exception as e:
                duration = time.time() - start_time
                metric.observe(duration)
                raise

        @wraps(func)
        def sync_wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                metric.observe(duration)
                return result
            except Exception as e:
                duration = time.time() - start_time
                metric.observe(duration)
                raise

        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator

class MetricsCollector:
    """Collects and manages application metrics."""
    
    @staticmethod
    def record_validation_result(is_valid: bool):
        """Record email validation result."""
        EMAIL_VALIDATION_TOTAL.labels(
            result="valid" if is_valid else "invalid"
        ).inc()

    @staticmethod
    def record_validation_duration(duration: float, validation_type: str):
        """Record validation duration."""
        EMAIL_VALIDATION_DURATION.labels(
            validation_type=validation_type
        ).observe(duration)

    @staticmethod
    def record_validation_error(error_type: str):
        """Record validation error."""
        VALIDATION_ERRORS.labels(error_type=error_type).inc()

    @staticmethod
    def record_dns_lookup(record_type: str, is_success: bool):
        """Record DNS lookup attempt."""
        DNS_LOOKUP_TOTAL.labels(
            record_type=record_type,
            result="success" if is_success else "failure"
        ).inc()

    @staticmethod
    def record_dns_cache_status(record_type: str, is_hit: bool):
        """Record DNS cache hit/miss."""
        if is_hit:
            DNS_CACHE_HITS.labels(record_type=record_type).inc()
        else:
            DNS_CACHE_MISSES.labels(record_type=record_type).inc()

    @staticmethod
    def record_smtp_connection(is_success: bool):
        """Record SMTP connection attempt."""
        SMTP_CONNECTIONS_TOTAL.labels(
            result="success" if is_success else "failure"
        ).inc()

    @staticmethod
    def record_smtp_error(error_type: str):
        """Record SMTP error."""
        SMTP_CONNECTION_ERRORS.labels(error_type=error_type).inc()

    @staticmethod
    def update_smtp_connections(count: int):
        """Update active SMTP connections count."""
        ACTIVE_SMTP_CONNECTIONS.set(count)

    @staticmethod
    def record_redis_operation(operation: str, is_success: bool):
        """Record Redis operation."""
        REDIS_OPERATIONS_TOTAL.labels(
            operation=operation,
            result="success" if is_success else "failure"
        ).inc()

    @staticmethod
    def update_redis_connections(count: int):
        """Update active Redis connections count."""
        REDIS_CONNECTIONS.set(count)

    @staticmethod
    def record_rate_limit_exceeded(endpoint: str):
        """Record rate limit exceeded event."""
        RATE_LIMIT_EXCEEDED.labels(endpoint=endpoint).inc()

class MetricsMiddleware:
    """Middleware for collecting metrics in web applications."""
    
    def __init__(self):
        self.collector = MetricsCollector()
        
    async def __call__(self, request, call_next):
        """Process request and collect metrics."""
        context = MetricsContext(start_time=time.time())
        
        try:
            response = await call_next(request)
            context.is_success = 200 <= response.status_code < 400
            return response
            
        except Exception as e:
            context.is_success = False
            context.error_type = type(e).__name__
            raise
            
        finally:
            duration = time.time() - context.start_time
            
            # Record general request metrics
            REQUEST_DURATION.labels(
                endpoint=request.url.path,
                method=request.method,
                status="success" if context.is_success else "failure"
            ).observe(duration)
            
            if not context.is_success:
                REQUEST_ERRORS.labels(
                    endpoint=request.url.path,
                    error_type=context.error_type
                ).inc()

def initialize_metrics(app_info: dict):
    """Initialize system metrics with application information."""
    SYSTEM_INFO.info(app_info)
    
def reset_metrics():
    """Reset all metrics (mainly for testing)."""
    EMAIL_VALIDATION_TOTAL._metrics.clear()
    EMAIL_VALIDATION_DURATION._metrics.clear()
    VALIDATION_ERRORS._metrics.clear()
    DNS_LOOKUP_TOTAL._metrics.clear()
    DNS_LOOKUP_DURATION._metrics.clear()
    DNS_CACHE_HITS._metrics.clear()
    DNS_CACHE_MISSES._metrics.clear()
    SMTP_CONNECTIONS_TOTAL._metrics.clear()
    SMTP_VERIFICATION_DURATION._metrics.clear()
    ACTIVE_SMTP_CONNECTIONS._metrics.clear()
    SMTP_CONNECTION_ERRORS._metrics.clear()
    REDIS_OPERATIONS_TOTAL._metrics.clear()
    REDIS_OPERATION_DURATION._metrics.clear()
    REDIS_CONNECTIONS._metrics.clear()
    RATE_LIMIT_EXCEEDED._metrics.clear()