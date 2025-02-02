"""
Syntax Validator Module
Provides functionality to validate email syntax according to RFC 5322 standards.
"""

import re
import idna
from typing import Tuple
from app.utils.constants import (
    EMAIL_REGEX, DOMAIN_MAX_LENGTH, LOCAL_PART_MAX_LENGTH,
    ERR_INVALID_SYNTAX, ERR_LOCAL_TOO_LONG, ERR_DOMAIN_TOO_LONG,
    ERR_INVALID_LOCAL_CHARS, ERR_INVALID_DOMAIN_CHARS,
    ERR_CONSECUTIVE_DOTS, ERR_DOT_START_END
)
from app.utils.exceptions import ValidationError
from app.utils.validation_result import ValidationResult

def validate_syntax(email: str) -> ValidationResult:
    """
    Validates the email syntax based on RFC 5322 standards with support for
    internationalized email addresses (IDNA).
    
    Args:
        email (str): The email address to validate.
    
    Returns:
        ValidationResult: Object containing validation results and any errors/warnings.
    """
    result = ValidationResult(email)
    
    try:
        # Basic checks
        if not email or '@' not in email:
            result.add_error(ERR_INVALID_SYNTAX)
            return result

        local_part, domain = email.rsplit('@', 1)
        
        # Validate lengths
        if len(local_part) > LOCAL_PART_MAX_LENGTH:
            result.add_error(ERR_LOCAL_TOO_LONG)
        if len(domain) > DOMAIN_MAX_LENGTH:
            result.add_error(ERR_DOMAIN_TOO_LONG)
            
        # Check for consecutive dots
        if '..' in local_part or '..' in domain:
            result.add_error(ERR_CONSECUTIVE_DOTS)
            
        # Check for dots at start/end
        if local_part.startswith('.') or local_part.endswith('.'):
            result.add_error(ERR_DOT_START_END)
            
        # Validate against RFC 5322 pattern
        if not re.match(EMAIL_REGEX, email, re.VERBOSE):
            result.add_error(ERR_INVALID_SYNTAX)
            
        # Handle internationalized domain names
        try:
            domain_ascii = idna.encode(domain).decode('ascii')
            result.add_detail('domain_ascii', domain_ascii)
        except idna.IDNAError:
            result.add_error(ERR_INVALID_DOMAIN_CHARS)
            
        # Set validity based on presence of errors
        result.syntax_valid = len(result.errors) == 0
        result.is_valid = result.syntax_valid
        
        return result
        
    except Exception as e:
        result.add_error(str(e))
        return result

def split_email(email: str) -> Tuple[str, str]:
    """
    Splits an email address into local part and domain.
    
    Args:
        email (str): The email address to split.
        
    Returns:
        Tuple[str, str]: Tuple containing (local_part, domain)
        
    Raises:
        ValidationError: If email cannot be split properly
    """
    try:
        local_part, domain = email.rsplit('@', 1)
        return local_part, domain
    except ValueError:
        raise ValidationError(ERR_INVALID_SYNTAX)