"""
Email validation module implementing RFC 5322 compliant validation.

This module provides comprehensive email address validation functionality
following RFC 5322 standards with support for:
- Basic email syntax validation
- Internationalized email addresses (IDNA)
- Separate local and domain part validation
- Special character handling
"""

import re
from typing import Tuple, Optional, List
import idna
import unicodedata
from dataclasses import dataclass
from enum import Enum

class IDNAError(Exception):
    """Raised when IDNA conversion fails."""
    pass

class EmailPartType(Enum):
    """Types of email address parts."""
    LOCAL = "local"
    DOMAIN = "domain"

@dataclass
class ValidationResult:
    """Stores the result of email validation."""
    is_valid: bool
    error_message: Optional[str] = None
    details: Optional[dict] = None

class RFC5322EmailValidator:
    """
    Validates email addresses according to RFC 5322 specifications.
    
    This implementation follows the RFC 5322 standard for email address validation,
    including support for international characters and special cases.
    """
    
    # RFC 5322 compliant regex pattern for email validation
    EMAIL_REGEX = re.compile(r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])""", re.IGNORECASE)
    
    def __init__(self):
        """Initialize the validator."""
        pass

    def validate_email(self, email: str) -> ValidationResult:
        """
        Validate an email address according to RFC 5322.

        Args:
            email: The email address to validate.

        Returns:
            ValidationResult: Contains validation status and any error messages.
        """
        if not email or not isinstance(email, str):
            return ValidationResult(
                is_valid=False,
                error_message="Email address must be a non-empty string"
            )

        # Basic format validation
        if not self.EMAIL_REGEX.match(email):
            return ValidationResult(
                is_valid=False,
                error_message="Email address does not match RFC 5322 format"
            )

        # Split email into local and domain parts
        try:
            local_part, domain = self._split_email(email)
        except ValueError as e:
            return ValidationResult(
                is_valid=False,
                error_message=str(e)
            )

        # Validate local part
        local_part_validation = self._validate_local_part(local_part)
        if not local_part_validation.is_valid:
            return local_part_validation

        # Validate domain part
        domain_validation = self._validate_domain_part(domain)
        if not domain_validation.is_valid:
            return domain_validation

        return ValidationResult(
            is_valid=True,
            details={
                "local_part": local_part,
                "domain": domain,
                "normalized_email": f"{local_part}@{domain}"
            }
        )

    def _split_email(self, email: str) -> Tuple[str, str]:
        """
        Split email into local and domain parts.

        Args:
            email: The email address to split.

        Returns:
            Tuple containing local part and domain.

        Raises:
            ValueError: If email cannot be split properly.
        """
        try:
            local_part, domain = email.rsplit('@', 1)
            if not local_part or not domain:
                raise ValueError("Email must have non-empty local and domain parts")
            return local_part, domain
        except ValueError:
            raise ValueError("Invalid email format: must contain exactly one '@' character")

    def _validate_local_part(self, local_part: str) -> ValidationResult:
        """
        Validate the local part of an email address.

        Args:
            local_part: The local part to validate.

        Returns:
            ValidationResult: Contains validation status and any error messages.
        """
        if len(local_part) > 64:
            return ValidationResult(
                is_valid=False,
                error_message="Local part exceeds maximum length of 64 characters"
            )

        # Additional local part validation rules can be added here
        return ValidationResult(is_valid=True)

    def normalize_email_part(self, part: str, part_type: EmailPartType) -> str:
        """
        Normalize email parts according to IDNA 2008 and Unicode standards.

        Args:
            part: The email part to normalize (local or domain).
            part_type: Type of the email part (LOCAL or DOMAIN).

        Returns:
            Normalized string.

        Raises:
            IDNAError: If normalization fails.
        """
        # First, apply NFKC normalization to handle compatibility characters
        normalized = unicodedata.normalize('NFKC', part)

        if part_type == EmailPartType.DOMAIN:
            try:
                # Convert domain to ASCII using IDNA 2008
                return idna.encode(normalized, uts46=True).decode('ascii')
            except idna.IDNAError as e:
                raise IDNAError(f"Invalid international domain name: {str(e)}")
        else:
            # For local part, preserve Unicode characters as per RFC 6530
            return normalized

    def _validate_domain_part(self, domain: str) -> ValidationResult:
        """
        Validate the domain part of an email address.

        Args:
            domain: The domain to validate.

        Returns:
            ValidationResult: Contains validation status and any error messages.
        """
        try:
            # Normalize and convert domain to ASCII using IDNA 2008
            domain_ascii = self.normalize_email_part(domain, EmailPartType.DOMAIN)
            
            if len(domain_ascii) > 255:
                return ValidationResult(
                    is_valid=False,
                    error_message="Domain exceeds maximum length of 255 characters"
                )

            # Check for valid domain format
            if not re.match(r'^[a-zA-Z0-9.-]+$', domain_ascii):
                return ValidationResult(
                    is_valid=False,
                    error_message="Domain contains invalid characters"
                )

            return ValidationResult(is_valid=True)
        except idna.IDNAError:
            return ValidationResult(
                is_valid=False,
                error_message="Invalid international domain name"
            )