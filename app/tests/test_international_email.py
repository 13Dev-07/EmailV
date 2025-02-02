"""Tests for internationalized email address validation."""

import pytest
from app.validators import RFC5322EmailValidator, ValidationResult

@pytest.fixture
def validator():
    return RFC5322EmailValidator()

def test_chinese_email(validator):
    result = validator.validate_email("用户@例子.中国")
    assert result.is_valid
    assert "normalized_email" in result.details

def test_cyrillic_email(validator):
    result = validator.validate_email("пользователь@пример.рф")
    assert result.is_valid
    assert "normalized_email" in result.details

def test_japanese_email(validator):
    result = validator.validate_email("ユーザー@例.日本")
    assert result.is_valid
    assert "normalized_email" in result.details

def test_arabic_email(validator):
    result = validator.validate_email("مستخدم@مثال.مصر")
    assert result.is_valid
    assert "normalized_email" in result.details

def test_mixed_script_email(validator):
    result = validator.validate_email("user.测试@例子.com")
    assert result.is_valid
    assert "normalized_email" in result.details

def test_emoji_in_local_part(validator):
    result = validator.validate_email("😊user@example.com")
    assert not result.is_valid
    assert "Invalid characters in local part" in result.error_message

def test_normalized_length_exceeded(validator):
    # Create a local part that's valid in Unicode but exceeds 64 bytes when encoded
    local_part = "测" * 32  # Each Chinese character is 3 bytes in UTF-8
    result = validator.validate_email(f"{local_part}@example.com")
    assert not result.is_valid
    assert "maximum length" in result.error_message

def test_punycode_conversion(validator):
    result = validator.validate_email("user@bücher.example")
    assert result.is_valid
    details = result.details
    assert "xn--" in details["normalized_email"]

def test_rtl_domain_name(validator):
    result = validator.validate_email("user@شركة.مصر")
    assert result.is_valid
    assert "normalized_email" in result.details

def test_korean_email(validator):
    result = validator.validate_email("사용자@예시.한국")
    assert result.is_valid
    assert "normalized_email" in result.details