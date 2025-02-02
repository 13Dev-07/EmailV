"""
Exceptions Module
Defines custom exceptions for the Ultimate Email Validation System.
"""

class ValidationError(Exception):
    """Exception raised for validation-related errors."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class RateLimitError(Exception):
    """Exception raised when rate limits are exceeded."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class SMTPVerificationError(Exception):
    """Exception raised during SMTP verification failures."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message