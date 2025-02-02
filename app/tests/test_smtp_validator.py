"""Tests for SMTP validator implementation."""

import pytest
import smtplib
from unittest.mock import Mock, patch, AsyncMock
from app.smtp_validator import SMTPValidator, SMTPValidationResult
from app.dns_resolver import DNSResolver, DNSRecord

@pytest.fixture
def dns_resolver():
    return Mock(spec=DNSResolver)

@pytest.fixture
def smtp_validator(dns_resolver):
    return SMTPValidator(
        dns_resolver=dns_resolver,
        connection_timeout=1.0,
        max_connections=5,
        max_retries=2,
        retry_delay=0.1
    )

@pytest.mark.asyncio
async def test_verify_valid_email(smtp_validator, dns_resolver):
    # Mock MX records
    dns_resolver.resolve_mx.return_value = [
        DNSRecord(value="mx1.example.com", record_type="MX", priority=10)
    ]
    
    # Mock SMTP connection
    mock_smtp = Mock(spec=smtplib.SMTP)
    mock_smtp.ehlo_or_helo_if_needed.return_value = (250, b"OK")
    mock_smtp.mail.return_value = (250, b"Sender OK")
    mock_smtp.rcpt.return_value = (250, b"Recipient OK")
    
    with patch('smtplib.SMTP') as mock_smtp_class:
        mock_smtp_class.return_value = mock_smtp
        
        result = await smtp_validator.verify_email("user@example.com")
        
        assert result.is_valid
        assert result.mx_used == "mx1.example.com"
        assert "Recipient OK" in result.smtp_response

@pytest.mark.asyncio
async def test_verify_invalid_email(smtp_validator, dns_resolver):
    # Mock MX records
    dns_resolver.resolve_mx.return_value = [
        DNSRecord(value="mx1.example.com", record_type="MX", priority=10)
    ]
    
    # Mock SMTP connection
    mock_smtp = Mock(spec=smtplib.SMTP)
    mock_smtp.ehlo_or_helo_if_needed.return_value = (250, b"OK")
    mock_smtp.mail.return_value = (250, b"Sender OK")
    mock_smtp.rcpt.return_value = (550, b"User not found")
    
    with patch('smtplib.SMTP') as mock_smtp_class:
        mock_smtp_class.return_value = mock_smtp
        
        result = await smtp_validator.verify_email("invalid@example.com")
        
        assert not result.is_valid
        assert "Email address does not exist" in result.error_message
        assert "User not found" in result.smtp_response

@pytest.mark.asyncio
async def test_verify_no_mx_records(smtp_validator, dns_resolver):
    # Mock empty MX records
    dns_resolver.resolve_mx.return_value = []
    
    result = await smtp_validator.verify_email("user@example.com")
    
    assert not result.is_valid
    assert "No MX records found" in result.error_message

@pytest.mark.asyncio
async def test_smtp_connection_error(smtp_validator, dns_resolver):
    # Mock MX records
    dns_resolver.resolve_mx.return_value = [
        DNSRecord(value="mx1.example.com", record_type="MX", priority=10)
    ]
    
    # Mock SMTP connection error
    with patch('smtplib.SMTP') as mock_smtp_class:
        mock_smtp_class.side_effect = ConnectionError("Connection failed")
        
        result = await smtp_validator.verify_email("user@example.com")
        
        assert not result.is_valid
        assert "Max retries exceeded" in result.error_message
        assert "Connection failed" in result.error_message

@pytest.mark.asyncio
async def test_mx_priority_order(smtp_validator, dns_resolver):
    # Mock multiple MX records with different priorities
    dns_resolver.resolve_mx.return_value = [
        DNSRecord(value="mx2.example.com", record_type="MX", priority=20),
        DNSRecord(value="mx1.example.com", record_type="MX", priority=10)
    ]
    
    # Mock SMTP connection
    mock_smtp = Mock(spec=smtplib.SMTP)
    mock_smtp.ehlo_or_helo_if_needed.return_value = (250, b"OK")
    mock_smtp.mail.return_value = (250, b"Sender OK")
    mock_smtp.rcpt.return_value = (250, b"Recipient OK")
    
    with patch('smtplib.SMTP') as mock_smtp_class:
        mock_smtp_class.return_value = mock_smtp
        
        result = await smtp_validator.verify_email("user@example.com")
        
        assert result.is_valid
        # Should use MX record with lowest priority first
        assert result.mx_used == "mx1.example.com"

@pytest.mark.asyncio
async def test_retry_logic(smtp_validator, dns_resolver):
    # Mock MX records
    dns_resolver.resolve_mx.return_value = [
        DNSRecord(value="mx1.example.com", record_type="MX", priority=10)
    ]
    
    # Mock SMTP connection with temporary failure then success
    mock_smtp_fail = Mock(spec=smtplib.SMTP)
    mock_smtp_fail.ehlo_or_helo_if_needed.side_effect = ConnectionError("Temporary failure")
    
    mock_smtp_success = Mock(spec=smtplib.SMTP)
    mock_smtp_success.ehlo_or_helo_if_needed.return_value = (250, b"OK")
    mock_smtp_success.mail.return_value = (250, b"Sender OK")
    mock_smtp_success.rcpt.return_value = (250, b"Recipient OK")
    
    with patch('smtplib.SMTP') as mock_smtp_class:
        mock_smtp_class.side_effect = [mock_smtp_fail, mock_smtp_success]
        
        result = await smtp_validator.verify_email("user@example.com")
        
        assert result.is_valid
        assert result.mx_used == "mx1.example.com"