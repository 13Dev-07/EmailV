"""SMTP Connection Pool Metrics."""
from prometheus_client import Counter, Gauge, Histogram

# Connection pool metrics
smtp_connection_pool_size = Gauge(
    'smtp_connection_pool_size',
    'Current number of connections in the SMTP connection pool',
    ['server']
)

smtp_connection_wait_time = Histogram(
    'smtp_connection_wait_time_seconds',
    'Time spent waiting for an SMTP connection',
    buckets=(0.1, 0.5, 1.0, 2.0, 5.0)
)

smtp_connection_errors = Counter(
    'smtp_connection_errors_total',
    'Total number of SMTP connection errors',
    ['server', 'error_type']
)

smtp_connection_lifetime = Histogram(
    'smtp_connection_lifetime_seconds',
    'Lifetime of SMTP connections',
    buckets=(300, 600, 1800, 3600, 7200)
)

smtp_connection_reuse = Counter(
    'smtp_connection_reuse_total',
    'Number of times connections were reused from the pool',
    ['server']
)

smtp_health_check_failures = Counter(
    'smtp_health_check_failures_total',
    'Number of failed health checks',
    ['server']
)