"""Security checks for input validation."""
import re
import unicodedata
from typing import List, Tuple

def check_sql_injection(text: str) -> Tuple[bool, str]:
    """Check for SQL injection patterns."""
    patterns = [
        r'--',
        r';',
        r'\/\*',
        r'\*\/',
        r'UNION\s+SELECT',
        r'DROP\s+TABLE',
        r'DELETE\s+FROM',
        r'INSERT\s+INTO',
        r'EXEC\(',
        r'EXECUTE\(',
    ]
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return False, "SQL injection pattern detected"
    return True, ""

def sanitize_input(text: str) -> str:
    """Sanitize input by escaping special characters."""
    escape_map = {
        '<': '&lt;',
        '>': '&gt;',
        '&': '&amp;',
        '"': '&quot;',
        "'": '&#x27;'
    }
    return ''.join(escape_map.get(c, c) for c in text)

def normalize_email(email: str) -> str:
    """Normalize email string using NFKC normalization."""
    return unicodedata.normalize('NFKC', email.strip().lower())

def check_blocked_tlds(domain: str) -> Tuple[bool, str]:
    """Check for blocked top-level domains."""
    blocked_tlds = {
        'temp', 'xyz', 'tk', 'ml', 'ga', 'cf', 'gq'
    }
    tld = domain.split('.')[-1].lower()
    if tld in blocked_tlds:
        return False, f"TLD '.{tld}' is blocked"
    return True, ""