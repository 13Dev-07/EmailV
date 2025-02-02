"""Unit tests for error handling scenarios in the email validation service."""
import pytest
from unittest.mock import patch
from app.api.service import EmailValidationService
from app.exceptions import (
    RateLimitExceeded,
    InvalidAuthToken,
    ValidationError,
    DNSResolutionError,
    SMTPVerificationError
)

@pytest.fixture
def validation_service():
    return EmailValidationService()

class TestErrorHandling:
    """Test suite for error handling scenarios."""

    def test_invalid_auth_token(self, validation_service):
        """Test handling of invalid authentication token."""
        with pytest.raises(InvalidAuthToken) as exc_info:
            with patch('app.auth.verify_token', return_value=False):
                validation_service.validate_email("test@example.com")
        assert "Invalid or expired authentication token" in str(exc_info.value)

    def test_rate_limit_exceeded(self, validation_service):
        """Test handling of rate limit exceeded scenario."""
        with pytest.raises(RateLimitExceeded) as exc_info:
            with patch('app.rate_limiter.check_limit', return_value=False):
                validation_service.validate_email("test@example.com")
        assert "Rate limit exceeded" in str(exc_info.value)

    def test_dns_resolution_failure(self, validation_service):
        """Test handling of DNS resolution failures."""
        with pytest.raises(DNSResolutionError) as exc_info:
            with patch('app.validators.dns.resolve_domain', side_effect=DNSResolutionError("DNS lookup failed")):
                validation_service.validate_email("test@nonexistent.com")
        assert "DNS lookup failed" in str(exc_info.value)

    def test_smtp_verification_timeout(self, validation_service):
        """Test handling of SMTP verification timeouts."""
        with pytest.raises(SMTPVerificationError) as exc_info:
            with patch('app.validators.smtp.verify_email', side_effect=SMTPVerificationError("Connection timed out")):
                validation_service.validate_email("test@example.com")
        assert "Connection timed out" in str(exc_info.value)

    @pytest.mark.parametrize("invalid_email", [
        "",  # Empty string
        "not-an-email",  # No @ symbol
        "@nodomain.com",  # No local part
        "spaces in@email.com",  # Spaces in local part
        "test@",  # No domain
        "test@invalid.",  # Invalid domain
        "test@domain..com",  # Double dots in domain
    ])
    def test_invalid_email_formats(self, validation_service, invalid_email):
        """Test handling of various invalid email formats."""
        with pytest.raises(ValidationError) as exc_info:
            validation_service.validate_email(invalid_email)
        assert "Invalid email format" in str(exc_info.value)

    def test_malformed_batch_request(self, validation_service):
        """Test handling of malformed batch validation requests."""
        with pytest.raises(ValidationError) as exc_info:
            validation_service.validate_batch(None)
        assert "Invalid batch request format" in str(exc_info.value)

        with pytest.raises(ValidationError) as exc_info:
            validation_service.validate_batch([])
        assert "Empty batch request" in str(exc_info.value)

    def test_concurrent_request_handling(self, validation_service):
        """Test handling of concurrent request errors."""
        with patch('app.cache.acquire_lock', return_value=False):
            with pytest.raises(ValidationError) as exc_info:
                validation_service.validate_email("test@example.com")
            assert "Service is busy" in str(exc_info.value)