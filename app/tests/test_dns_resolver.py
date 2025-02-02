"""Tests for DNS resolution module."""

import pytest
import dns.resolver
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
from app.dns_resolver import DNSResolver, DNSCache, DNSRecord

@pytest.fixture
def dns_cache():
    return DNSCache(default_ttl=60)

@pytest.fixture
def dns_resolver():
    return DNSResolver(timeout=2.0, cache_ttl=60)

def test_dns_cache_expiration(dns_cache):
    # Create expired and non-expired records
    expired = DNSRecord(
        value="mail.example.com",
        record_type="MX",
        priority=10,
        expiration=datetime.now() - timedelta(seconds=1)
    )
    
    valid = DNSRecord(
        value="mail2.example.com",
        record_type="MX",
        priority=20,
        expiration=datetime.now() + timedelta(seconds=60)
    )
    
    # Manually insert records
    dns_cache._cache["example.com"] = {"MX": [expired, valid]}
    
    # Get records - should only return non-expired
    records = dns_cache.get("example.com", "MX")
    assert len(records) == 1
    assert records[0].value == "mail2.example.com"

@pytest.mark.asyncio
async def test_mx_resolution(dns_resolver):
    domain = "example.com"
    
    # Mock DNS resolver response
    mock_mx = Mock()
    mock_mx.exchange = dns.name.from_text("mail.example.com")
    mock_mx.preference = 10
    
    with patch("dns.resolver.Resolver.resolve") as mock_resolve:
        mock_resolve.return_value = [mock_mx]
        
        records = await dns_resolver.resolve_mx(domain)
        assert len(records) == 1
        assert records[0].value == "mail.example.com"
        assert records[0].priority == 10

@pytest.mark.asyncio
async def test_mx_fallback_to_a(dns_resolver):
    domain = "example.com"
    
    with patch("dns.resolver.Resolver.resolve") as mock_resolve:
        # Make MX lookup fail
        def side_effect(domain, record_type):
            if record_type == "MX":
                raise dns.exception.DNSException()
            return [Mock(address="192.0.2.1")]
            
        mock_resolve.side_effect = side_effect
        
        records = await dns_resolver.resolve_mx(domain)
        assert len(records) == 1
        assert records[0].value == "192.0.2.1"
        assert records[0].record_type == "A"

@pytest.mark.asyncio
async def test_dns_cache_hit(dns_resolver):
    domain = "example.com"
    cached_record = DNSRecord(
        value="mail.example.com",
        record_type="MX",
        priority=10,
        expiration=datetime.now() + timedelta(seconds=60)
    )
    
    dns_resolver.cache._cache[domain] = {"MX": [cached_record]}
    
    with patch("dns.resolver.Resolver.resolve") as mock_resolve:
        records = await dns_resolver.resolve_mx(domain)
        assert len(records) == 1
        assert records[0].value == "mail.example.com"
        mock_resolve.assert_not_called()  # Should use cached value

@pytest.mark.asyncio
async def test_timeout_handling(dns_resolver):
    domain = "example.com"
    
    with patch("dns.resolver.Resolver.resolve") as mock_resolve:
        mock_resolve.side_effect = dns.exception.Timeout()
        
        with pytest.raises(dns.exception.DNSException):
            await dns_resolver.resolve_mx(domain)