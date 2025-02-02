"""SMTP-related custom exceptions."""

class SMTPPoolError(Exception):
    """Base exception for SMTP connection pool errors."""
    pass

class SMTPConnectionError(SMTPPoolError):
    """Raised when a connection cannot be established."""
    pass

class SMTPHealthCheckError(SMTPPoolError):
    """Raised when a health check fails."""
    pass

class SMTPPoolExhaustedError(SMTPPoolError):
    """Raised when the connection pool is exhausted."""
    pass