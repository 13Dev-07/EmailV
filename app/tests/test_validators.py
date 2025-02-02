"""Tests for the email validator implementation."""

import pytest
from app.validators import RFC5322EmailValidator, ValidationResult

@pytest.fixture
def validator():
    return RFC5322EmailValidator()

def test_basic_valid_email(validator):
    result = validator.validate_email("user@example.com")
    assert result.is_valid
    assert result.error_message is None

def test_invalid_email_format(validator):
    result = validator.validate_email("invalid-email")
    assert not result.is_valid
    assert "RFC 5322 format" in result.error_message

def test_empty_email(validator):
    result = validator.validate_email("")
    assert not result.is_valid
    assert "non-empty string" in result.error_message

def test_none_email(validator):
    result = validator.validate_email(None)
    assert not result.is_valid
    assert "non-empty string" in result.error_message

def test_long_local_part(validator):
    local_part = "a" * 65
    result = validator.validate_email(f"{local_part}@example.com")
    assert not result.is_valid
    assert "maximum length" in result.error_message

def test_international_domain(validator):
    result = validator.validate_email("user@bücher.com")
    assert result.is_valid

def test_special_characters_local_part(validator):
    result = validator.validate_email('user+test!#$%&\'*+-/=?^_`{|}~@example.com')
    assert result.is_valid

def test_quoted_local_part(validator):
    result = validator.validate_email('"very.unusual.@.unusual.com"@example.com')
    assert result.is_valid

def test_multiple_at_signs(validator):
    result = validator.validate_email("user@@example.com")
    assert not result.is_valid

def test_missing_domain(validator):
    result = validator.validate_email("user@")
    assert not result.is_valid

def test_missing_local_part(validator):
    result = validator.validate_email("@example.com")
    assert not result.is_valid

def test_invalid_domain_characters(validator):
    result = validator.validate_email("user@exam ple.com")
    assert not result.is_valid
    assert "invalid characters" in result.error_message