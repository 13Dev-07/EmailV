"""Connection-related exceptions."""

class ConnectionError(Exception):
    """Base exception for connection errors."""
    pass

class ConnectionPoolError(ConnectionError):
    """Base exception for connection pool errors."""
    pass

class PoolExhaustedError(ConnectionPoolError):
    """Raised when the connection pool is exhausted."""
    pass

class HealthCheckError(ConnectionPoolError):
    """Raised when a health check fails."""
    pass

class ConfigurationError(ConnectionPoolError):
    """Raised when there is a configuration error."""
    pass