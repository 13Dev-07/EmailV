"""
Unit tests for DNS resolution functionality.
"""

import pytest
from unittest.mock import Mock, patch
import dns.resolver
from dns.resolver import Answer
from app.utils.dns_resolver import DNSResolver
from app.utils.dns_constants import (
    MX_RECORD, A_RECORD, AAAA_RECORD,
    ERR_DNS_TIMEOUT, ERR_NO_RECORDS
)

@pytest.fixture
def dns_resolver(cache_manager):
    """DNS resolver fixture."""
    return DNSResolver(cache_manager=cache_manager)

def test_encode_idn():
    """Test IDNA encoding of internationalized domain names."""
    resolver = DNSResolver()
    result = resolver.encode_idn("münchen.de")
    assert result == "xn--mnchen-3ya.de"

@patch("dns.resolver.Resolver.resolve")
def test_get_mx_records(mock_resolve, dns_resolver):
    """Test MX record resolution."""
    # Mock MX record response
    mock_record = Mock()
    mock_record.preference = 10
    mock_record.exchange = dns.name.from_text("mail.example.com")
    mock_resolve.return_value = [mock_record]

    records = dns_resolver.get_mx_records("example.com")
    assert len(records) == 1
    assert records[0] == (10, "mail.example.com")
    mock_resolve.assert_called_with("example.com", MX_RECORD)

@patch("dns.resolver.Resolver.resolve")
def test_get_mx_records_fallback(mock_resolve, dns_resolver):
    """Test fallback to A/AAAA records when no MX exists."""
    # Mock no MX record scenario
    mock_resolve.side_effect = [
        dns.resolver.NoAnswer(),  # MX lookup fails
        [Mock()],  # A record exists
        dns.resolver.NoAnswer()  # No AAAA record
    ]

    records = dns_resolver.get_mx_records("example.com")
    assert len(records) == 1
    assert records[0][0] == 10  # Default priority
    assert records[0][1] == "example.com"

@patch("dns.resolver.Resolver.resolve")
def test_get_mx_records_no_records(mock_resolve, dns_resolver):
    """Test handling when no records exist."""
    mock_resolve.side_effect = dns.resolver.NoAnswer()
    
    with pytest.raises(Exception) as exc_info:
        dns_resolver.get_mx_records("nonexistent.com")
    assert str(exc_info.value) == ERR_NO_RECORDS

@patch("dns.resolver.Resolver.resolve")
def test_get_mx_records_timeout(mock_resolve, dns_resolver):
    """Test handling of DNS timeout."""
    mock_resolve.side_effect = dns.resolver.Timeout()
    
    with pytest.raises(Exception) as exc_info:
        dns_resolver.get_mx_records("slow.com")
    assert str(exc_info.value) == ERR_DNS_TIMEOUT

def test_resolve_domain(dns_resolver):
    """Test comprehensive domain resolution."""
    with patch.multiple(dns_resolver._resolver,
                       resolve=Mock(return_value=[Mock()])):
        result = dns_resolver.resolve_domain("example.com")
        assert isinstance(result, dict)
        assert "mx_found" in result
        assert "a_found" in result
        assert "aaaa_found" in result
        assert "ns_found" in result
        assert "domain_exists" in result