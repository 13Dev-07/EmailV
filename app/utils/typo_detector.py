"""
Typo Detector Module
Detects and suggests corrections for common typos in email addresses.
"""

import difflib
from typing import Optional

COMMON_EMAIL_DOMAINS = [
    "gmail.com",
    "yahoo.com",
    "outlook.com",
    "hotmail.com",
    "aol.com",
    "icloud.com",
    "mail.com",
    "gmx.com",
    "protonmail.com",
    "zoho.com"
]

def detect_typo(email: str) -> Optional[str]:
    """
    Detects typos in the domain part of the email and suggests corrections.
    
    Args:
        email (str): The email address to check.
    
    Returns:
        Optional[str]: Suggested correction if a typo is detected, else None.
    """
    try:
        local_part, domain = email.split('@')
    except ValueError:
        # Invalid email format; syntax validation should handle this
        return None
    
    domain = domain.lower()
    close_matches = difflib.get_close_matches(domain, COMMON_EMAIL_DOMAINS, n=1, cutoff=0.8)
    
    if close_matches and close_matches[0] != domain:
        return f"Did you mean '@{close_matches[0]}'?"
    return None

def is_typo_detected(email: str) -> bool:
    """
    Determines if a typo is detected in the email's domain.
    
    Args:
        email (str): The email address to evaluate.
    
    Returns:
        bool: True if a typo is detected, False otherwise.
    """
    return detect_typo(email) is not None