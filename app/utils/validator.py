"""
Validator Module
Provides auxiliary validation utilities.
"""

import re
from typing import Optional
from app.utils.exceptions import ValidationError

def is_valid_email_format(email: str) -> bool:
    """
    Validates the email format using a simplified regex.
    
    Args:
        email (str): The email address to validate.
    
    Returns:
        bool: True if format is valid, False otherwise.
    """
    regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(regex, email) is not None

def has_valid_length(email: str, max_length: int = 254) -> bool:
    """
    Ensures the email does not exceed the maximum allowed length.
    
    Args:
        email (str): The email address to check.
        max_length (int): Maximum allowed length.
    
    Returns:
        bool: True if within limits, False otherwise.
    """
    return len(email) <= max_length

def extract_domain(email: str) -> Optional[str]:
    """
    Extracts the domain part from the email address.
    
    Args:
        email (str): The email address.
    
    Returns:
        Optional[str]: The domain if extraction is successful, else None.
    """
    try:
        return email.split('@')[1].lower()
    except IndexError:
        return None

def is_valid_email(email: str) -> bool:
    """
    Comprehensive email validation combining multiple checks.
    
    Args:
        email (str): The email address to validate.
    
    Returns:
        bool: True if email is valid, False otherwise.
    """
    if not contains_only_allowed_characters(email):
        return False
    if not has_valid_length(email):
        return False
    if not is_valid_email_format(email):
        return False
    return True

def contains_only_allowed_characters(email: str) -> bool:
    """
    Ensures the email contains only allowed characters.
    
    Args:
        email (str): The email address to check.
    
    Returns:
        bool: True if only allowed characters are present, False otherwise.
    """
    allowed_regex = r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$"
    return re.match(allowed_regex, email) is not None