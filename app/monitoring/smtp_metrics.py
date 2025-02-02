"""SMTP connection and operation metrics."""

from prometheus_client import Counter, Gauge, Histogram

# Connection pool metrics
SMTP_POOL_SIZE = Gauge(
    "smtp_pool_size",
    "Number of SMTP connections in the pool",
    ["server", "state"]
)

SMTP_CONNECTION_ERRORS = Counter(
    "smtp_connection_errors_total",
    "Number of SMTP connection errors",
    ["server", "error_type"]
)

SMTP_OPERATION_DURATION = Histogram(
    "smtp_operation_duration_seconds",
    "Duration of SMTP operations",
    ["operation_type"]
)

SMTP_CONNECTION_LIFETIME = Histogram(
    "smtp_connection_lifetime_seconds",
    "Lifetime of SMTP connections"
)

class SMTPMetrics:
    @staticmethod
    def record_connection_error(server: str, error_type: str):
        """Record a connection error."""
        SMTP_CONNECTION_ERRORS.labels(
            server=server,
            error_type=error_type
        ).inc()

    @staticmethod
    def update_pool_size(server: str, state: str, delta: int):
        """Update the connection pool size metrics."""
        SMTP_POOL_SIZE.labels(
            server=server,
            state=state
        ).inc(delta)

    @staticmethod
    def observe_operation_duration(operation_type: str, duration: float):
        """Record the duration of an SMTP operation."""
        SMTP_OPERATION_DURATION.labels(
            operation_type=operation_type
        ).observe(duration)

    @staticmethod
    def record_connection_lifetime(lifetime: float):
        """Record the lifetime of a connection that is being closed."""
        SMTP_CONNECTION_LIFETIME.observe(lifetime)