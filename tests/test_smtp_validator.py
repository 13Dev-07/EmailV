"""Unit tests for SMTP validator component."""

import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from app.smtp_validator import SMTPValidator, SMTPValidationResult
from app.dns_resolver import DNSResolver, DNSRecord
from app.redis_client import RedisClient

@pytest.fixture
def mock_dns_resolver():
    resolver = MagicMock(spec=DNSResolver)
    resolver.resolve_mx = AsyncMock(return_value=[
        DNSRecord(value="mx1.example.com", record_type="MX", priority=10),
        DNSRecord(value="mx2.example.com", record_type="MX", priority=20)
    ])
    return resolver

@pytest.fixture
def mock_redis_client():
    client = MagicMock(spec=RedisClient)
    client.get_cache = AsyncMock(return_value=None)
    client.set_cache = AsyncMock()
    return client

@pytest.fixture
def smtp_validator(mock_dns_resolver, mock_redis_client):
    return SMTPValidator(
        dns_resolver=mock_dns_resolver,
        redis_client=mock_redis_client
    )

@pytest.mark.asyncio
async def test_verify_email_valid(smtp_validator):
    """Test successful email verification."""
    with patch('smtplib.SMTP') as mock_smtp:
        # Configure mock SMTP responses
        mock_smtp.return_value.mail.return_value = (250, b'OK')
        mock_smtp.return_value.rcpt.return_value = (250, b'OK')
        
        result = await smtp_validator.verify_email("test@example.com")
        
        assert result.is_valid
        assert not result.error_message
        assert result.smtp_response == 'OK'

@pytest.mark.asyncio
async def test_verify_email_invalid(smtp_validator):
    """Test invalid email verification."""
    with patch('smtplib.SMTP') as mock_smtp:
        mock_smtp.return_value.mail.return_value = (250, b'OK')
        mock_smtp.return_value.rcpt.return_value = (550, b'User unknown')
        
        result = await smtp_validator.verify_email("invalid@example.com")
        
        assert not result.is_valid
        assert result.error_message == "Email address does not exist"
        assert result.smtp_response == "User unknown"

@pytest.mark.asyncio
async def test_verify_email_connection_error(smtp_validator):
    """Test handling of SMTP connection errors."""
    with patch('smtplib.SMTP') as mock_smtp:
        mock_smtp.return_value.connect.side_effect = ConnectionError("Connection failed")
        
        result = await smtp_validator.verify_email("test@example.com")
        
        assert not result.is_valid
        assert "Connection failed" in result.error_message

@pytest.mark.asyncio
async def test_verify_email_no_mx_records(smtp_validator, mock_dns_resolver):
    """Test handling of missing MX records."""
    mock_dns_resolver.resolve_mx = AsyncMock(return_value=[])
    
    result = await smtp_validator.verify_email("test@example.com")
    
    assert not result.is_valid
    assert result.error_message == "No MX records found for domain"

@pytest.mark.asyncio
async def test_verify_email_cached_result(smtp_validator, mock_redis_client):
    """Test that cached results are returned when available."""
    cached_result = {
        "is_valid": True,
        "error_message": None,
        "smtp_response": "OK",
        "mx_used": "mx1.example.com"
    }
    mock_redis_client.get_cache.return_value = cached_result
    
    result = await smtp_validator.verify_email("test@example.com")
    
    assert result.is_valid
    assert result.smtp_response == "OK"
    assert result.mx_used == "mx1.example.com"

@pytest.mark.asyncio
async def test_verify_email_retries(smtp_validator):
    """Test retry behavior on temporary failures."""
    with patch('smtplib.SMTP') as mock_smtp:
        # First attempt fails, second succeeds
        mock_smtp.return_value.connect.side_effect = [
            ConnectionError("Temporary failure"),
            None
        ]
        mock_smtp.return_value.mail.return_value = (250, b'OK')
        mock_smtp.return_value.rcpt.return_value = (250, b'OK')
        
        result = await smtp_validator.verify_email("test@example.com")
        
        assert result.is_valid
        assert result.smtp_response == "OK"