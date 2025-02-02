"""
DNS-related constants for email validation system.
"""

# DNS record types
MX_RECORD = 'MX'
A_RECORD = 'A'
AAAA_RECORD = 'AAAA'
NS_RECORD = 'NS'
PTR_RECORD = 'PTR'

# Timeouts (in seconds)
DNS_TIMEOUT = 10
CACHE_TTL = 3600  # 1 hour

# Error messages
ERR_DNS_TIMEOUT = "DNS lookup timed out"
ERR_NO_RECORDS = "No DNS records found"
ERR_INVALID_MX = "Invalid MX record format"
ERR_DNS_ERROR = "DNS resolution error"

# Cache keys
CACHE_KEY_PREFIX = "dns:"
MX_CACHE_PREFIX = f"{CACHE_KEY_PREFIX}mx:"
A_CACHE_PREFIX = f"{CACHE_KEY_PREFIX}a:"
AAAA_CACHE_PREFIX = f"{CACHE_KEY_PREFIX}aaaa:"
NS_CACHE_PREFIX = f"{CACHE_KEY_PREFIX}ns:"
PTR_CACHE_PREFIX = f"{CACHE_KEY_PREFIX}ptr:"