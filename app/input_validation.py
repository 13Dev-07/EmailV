"""Input validation and sanitization for email validator."""

import re
from typing import Optional, Dict
import logging
from dataclasses import dataclass
from email.utils import parseaddr
from app.monitoring.prometheus_metrics import validation_errors_total

logger = logging.getLogger(__name__)

@dataclass
class ValidationResult:
    """Result of input validation."""
    is_valid: bool
    error_message: Optional[str] = None

class EmailSanitizer:
    """Email input sanitization and validation."""
    
    # RFC 5322 compliant regex pattern
    EMAIL_REGEX = re.compile(r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])""", re.IGNORECASE)
    
    # Maximum lengths
    MAX_LOCAL_PART_LENGTH = 64
    MAX_DOMAIN_LENGTH = 255
    MAX_TOTAL_LENGTH = 320
    
    @classmethod
    def sanitize_and_validate(cls, email: str) -> ValidationResult:
        """
        Sanitize and validate email address.
        
        Args:
            email: Email address to validate.
            
        Returns:
            ValidationResult indicating if email is valid and any error message.
        """
        try:
            # Basic checks
            if not email or not isinstance(email, str):
                validation_errors_total.labels(error_type="invalid_type").inc()
                return ValidationResult(False, "Email must be a non-empty string")
            
            # Remove whitespace
            email = email.strip()
            
            # Check length constraints
            if len(email) > cls.MAX_TOTAL_LENGTH:
                validation_errors_total.labels(error_type="length_exceeded").inc()
                return ValidationResult(False, "Email exceeds maximum length")
            
            # Parse email into local part and domain
            local_part, domain = parseaddr(email)[1].split('@', 1)
            
            # Check component lengths
            if len(local_part) > cls.MAX_LOCAL_PART_LENGTH:
                validation_errors_total.labels(error_type="local_part_length").inc()
                return ValidationResult(False, "Local part exceeds maximum length")
            
            if len(domain) > cls.MAX_DOMAIN_LENGTH:
                validation_errors_total.labels(error_type="domain_length").inc()
                return ValidationResult(False, "Domain exceeds maximum length")
            
            # Check RFC 5322 compliance
            if not cls.EMAIL_REGEX.match(email):
                validation_errors_total.labels(error_type="format_invalid").inc()
                return ValidationResult(False, "Email format is invalid")
            
            # Check for common typos and suspicious patterns
            if not cls._check_common_mistakes(email):
                validation_errors_total.labels(error_type="suspicious_pattern").inc()
                return ValidationResult(False, "Email contains suspicious patterns")
            
            # Additional security checks
            if not cls._security_check(email):
                validation_errors_total.labels(error_type="security_risk").inc()
                return ValidationResult(False, "Email failed security checks")
            
            return ValidationResult(True)
            
        except Exception as e:
            logger.error(f"Email validation error: {str(e)}")
            validation_errors_total.labels(error_type="validation_error").inc()
            return ValidationResult(False, f"Validation error: {str(e)}")
    
    @classmethod
    def _check_common_mistakes(cls, email: str) -> bool:
        """Check for common typos and mistakes."""
        # List of common typos
        typos = [
            r'\.{2,}',           # Multiple dots
            r'@.*@',             # Multiple @ symbols
            r'[,;]',             # Common punctuation mistakes
            r'\s',               # Whitespace
            r'\.@',              # Dot before @
            r'@\.',             # Dot after @
        ]
        
        return not any(re.search(pattern, email) for pattern in typos)
    
    @classmethod
    def _security_check(cls, email: str) -> bool:
        """Perform security-related checks."""
        # Security checks
        security_risks = [
            r'<script',          # XSS attempt
            r'--',               # SQL injection attempt
            r';',                # Command injection attempt
            r'\x00',             # Null byte
            r'%00',             # URL encoded null byte
        ]
        
        return not any(re.search(pattern, email, re.IGNORECASE) for pattern in security_risks)