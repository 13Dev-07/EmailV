"""Unit tests for input validation."""

import pytest
from app.input_validation import EmailSanitizer

def test_valid_email():
    """Test validation of valid email addresses."""
    valid_emails = [
        "test@example.com",
        "user.name@domain.com",
        "user+tag@example.com",
        "a@b.com",
        "very.common@example.com",
        "disposable.style.email.with+symbol@example.com",
        "other.email-with-hyphen@example.com",
        "fully-qualified-domain@example.com",
        "user.name+tag+sorting@example.com",
        "example-indeed@strange-example.com",
    ]
    
    for email in valid_emails:
        result = EmailSanitizer.sanitize_and_validate(email)
        assert result.is_valid, f"Email should be valid: {email}"
        assert not result.error_message

def test_invalid_email():
    """Test validation of invalid email addresses."""
    invalid_emails = [
        "",  # Empty
        "not_an_email",  # Missing @
        "@no-local-part.com",  # No local part
        "spaces in@example.com",  # Space in local part
        ".dot-first@example.com",  # Dot at start
        "dot-last.@example.com",  # Dot at end
        "double..dot@example.com",  # Double dot
        "multi@ple@at.signs.com",  # Multiple @ signs
        "no-domain@",  # Missing domain
        "a" * 65 + "@example.com",  # Local part too long
        "test@" + "a" * 256 + ".com",  # Domain too long
    ]
    
    for email in invalid_emails:
        result = EmailSanitizer.sanitize_and_validate(email)
        assert not result.is_valid, f"Email should be invalid: {email}"
        assert result.error_message

def test_security_risks():
    """Test detection of security risks."""
    security_risk_emails = [
        "test@example.com<script>",  # XSS attempt
        "user@domain.com--",  # SQL injection attempt
        "admin@example.com;ls",  # Command injection attempt
        "user@domain.com\x00",  # Null byte
        "test@example.com%00",  # URL encoded null byte
    ]
    
    for email in security_risk_emails:
        result = EmailSanitizer.sanitize_and_validate(email)
        assert not result.is_valid, f"Email should be flagged as security risk: {email}"
        assert "security" in result.error_message.lower()

def test_whitespace_handling():
    """Test handling of whitespace in email addresses."""
    # Email with surrounding whitespace
    result = EmailSanitizer.sanitize_and_validate("   test@example.com  ")
    assert result.is_valid
    
    # Email with internal whitespace
    result = EmailSanitizer.sanitize_and_validate("test @ example.com")
    assert not result.is_valid

def test_case_sensitivity():
    """Test case sensitivity handling."""
    result = EmailSanitizer.sanitize_and_validate("Test.User@Example.COM")
    assert result.is_valid

def test_length_limits():
    """Test enforcement of length limits."""
    # Test maximum lengths
    long_local = "a" * EmailSanitizer.MAX_LOCAL_PART_LENGTH
    long_domain = "b" * (EmailSanitizer.MAX_DOMAIN_LENGTH - 4) + ".com"
    
    result = EmailSanitizer.sanitize_and_validate(f"{long_local}@{long_domain}")
    assert result.is_valid
    
    # Test exceeding maximum lengths
    too_long_local = "a" * (EmailSanitizer.MAX_LOCAL_PART_LENGTH + 1)
    result = EmailSanitizer.sanitize_and_validate(f"{too_long_local}@example.com")
    assert not result.is_valid
    
    too_long_domain = "b" * (EmailSanitizer.MAX_DOMAIN_LENGTH + 1)
    result = EmailSanitizer.sanitize_and_validate(f"test@{too_long_domain}")
    assert not result.is_valid