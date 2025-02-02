"""Tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, AsyncMock, patch
from app.api.models import ValidationRequest, ValidationResponse
from app.api.router import router
from app.validators import ValidationResult
from app.dns_resolver import DNSRecord
from app.smtp_validator import SMTPValidationResult

@pytest.fixture
def client():
    return TestClient(router)

@pytest.fixture
def mock_validators():
    syntax_validator = Mock()
    dns_resolver = AsyncMock()
    smtp_validator = AsyncMock()
    return syntax_validator, dns_resolver, smtp_validator

def test_validate_email_syntax_only(client, mock_validators):
    syntax_validator, _, _ = mock_validators
    
    # Mock successful syntax validation
    syntax_validator.validate_email.return_value = ValidationResult(
        is_valid=True,
        details={
            "local_part": "user",
            "domain": "example.com",
            "normalized_email": "user@example.com"
        }
    )
    
    with patch("app.api.router.get_validators", return_value=mock_validators):
        response = client.post(
            "/validate",
            json={
                "email": "user@example.com",
                "check_mx": False,
                "check_smtp": False
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["is_valid"] is True
        assert data["validation_type"] == "syntax"

def test_validate_email_with_mx(client, mock_validators):
    syntax_validator, dns_resolver, _ = mock_validators
    
    # Mock successful validations
    syntax_validator.validate_email.return_value = ValidationResult(
        is_valid=True,
        details={
            "local_part": "user",
            "domain": "example.com",
            "normalized_email": "user@example.com"
        }
    )
    
    dns_resolver.resolve_mx.return_value = [
        DNSRecord(
            value="mx1.example.com",
            record_type="MX",
            priority=10
        )
    ]
    
    with patch("app.api.router.get_validators", return_value=mock_validators):
        response = client.post(
            "/validate",
            json={
                "email": "user@example.com",
                "check_mx": True,
                "check_smtp": False
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["is_valid"] is True
        assert data["validation_type"] == "mx"
        assert len(data["details"]["mx_records"]) == 1

def test_validate_email_with_smtp(client, mock_validators):
    syntax_validator, dns_resolver, smtp_validator = mock_validators
    
    # Mock successful validations
    syntax_validator.validate_email.return_value = ValidationResult(
        is_valid=True,
        details={
            "local_part": "user",
            "domain": "example.com",
            "normalized_email": "user@example.com"
        }
    )
    
    dns_resolver.resolve_mx.return_value = [
        DNSRecord(
            value="mx1.example.com",
            record_type="MX",
            priority=10
        )
    ]
    
    smtp_validator.verify_email.return_value = SMTPValidationResult(
        is_valid=True,
        smtp_response="Recipient OK",
        mx_used="mx1.example.com"
    )
    
    with patch("app.api.router.get_validators", return_value=mock_validators):
        response = client.post(
            "/validate",
            json={
                "email": "user@example.com",
                "check_mx": True,
                "check_smtp": True
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["is_valid"] is True
        assert data["validation_type"] == "smtp"
        assert data["details"]["smtp_check"]["mx_used"] == "mx1.example.com"

def test_validate_email_invalid_syntax(client, mock_validators):
    syntax_validator, _, _ = mock_validators
    
    # Mock failed syntax validation
    syntax_validator.validate_email.return_value = ValidationResult(
        is_valid=False,
        error_message="Invalid email format"
    )
    
    with patch("app.api.router.get_validators", return_value=mock_validators):
        response = client.post(
            "/validate",
            json={
                "email": "invalid-email",
                "check_mx": True,
                "check_smtp": True
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["is_valid"] is False
        assert data["validation_type"] == "syntax"
        assert "Invalid email format" in data["error_message"]

def test_validate_email_no_mx_records(client, mock_validators):
    syntax_validator, dns_resolver, _ = mock_validators
    
    # Mock successful syntax but no MX records
    syntax_validator.validate_email.return_value = ValidationResult(
        is_valid=True,
        details={
            "local_part": "user",
            "domain": "example.com",
            "normalized_email": "user@example.com"
        }
    )
    
    dns_resolver.resolve_mx.return_value = []
    
    with patch("app.api.router.get_validators", return_value=mock_validators):
        response = client.post(
            "/validate",
            json={
                "email": "user@example.com",
                "check_mx": True,
                "check_smtp": False
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["is_valid"] is False
        assert data["validation_type"] == "mx"
        assert "No MX records found" in data["error_message"]

def test_validate_email_smtp_error(client, mock_validators):
    syntax_validator, dns_resolver, smtp_validator = mock_validators
    
    # Mock successful validations until SMTP fails
    syntax_validator.validate_email.return_value = ValidationResult(
        is_valid=True,
        details={
            "local_part": "user",
            "domain": "example.com",
            "normalized_email": "user@example.com"
        }
    )
    
    dns_resolver.resolve_mx.return_value = [
        DNSRecord(
            value="mx1.example.com",
            record_type="MX",
            priority=10
        )
    ]
    
    smtp_validator.verify_email.return_value = SMTPValidationResult(
        is_valid=False,
        error_message="Connection failed",
        mx_used="mx1.example.com"
    )
    
    with patch("app.api.router.get_validators", return_value=mock_validators):
        response = client.post(
            "/validate",
            json={
                "email": "user@example.com",
                "check_mx": True,
                "check_smtp": True
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["is_valid"] is False
        assert data["validation_type"] == "smtp"
        assert "Connection failed" in data["error_message"]

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "version" in data
    assert "components" in data