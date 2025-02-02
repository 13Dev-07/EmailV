"""Email part validation components."""

import re
import unicodedata
from dataclasses import dataclass
from typing import Optional, List
import idna
from enum import Enum

class EmailPartValidationError(Exception):
    """Base exception for email part validation errors."""
    pass

@dataclass
class PartValidationResult:
    """Results of validating an email part."""
    is_valid: bool
    normalized_value: Optional[str] = None
    error_message: Optional[str] = None

class LocalPartValidator:
    """Validates the local part of an email address."""

    # Maximum length for local part in bytes
    MAX_LENGTH_BYTES = 64
    
    # Characters allowed in unquoted local parts
    UNQUOTED_ALLOWED_CHARS = re.compile(
        r'^[a-zA-Z0-9!#$%&\'*+\-/=?^_`{|}~\u0080-\uFFFF]'
        r'+(?:\.[a-zA-Z0-9!#$%&\'*+\-/=?^_`{|}~\u0080-\uFFFF]+)*$'
    )
    
    # Characters allowed in quoted local parts
    QUOTED_ALLOWED_CHARS = re.compile(r'^[\x20-\x21\x23-\x5B\x5D-\x7E\u0080-\uFFFF]*$')

    @classmethod
    def validate(cls, local_part: str) -> PartValidationResult:
        """
        Validate local part of email address.
        
        Args:
            local_part: The local part to validate.
            
        Returns:
            PartValidationResult with validation status and normalized value.
        """
        if not local_part:
            return PartValidationResult(
                is_valid=False,
                error_message="Local part cannot be empty"
            )

        # Normalize Unicode characters
        normalized = unicodedata.normalize('NFKC', local_part)
        
        # Check encoded length
        if len(normalized.encode('utf-8')) > cls.MAX_LENGTH_BYTES:
            return PartValidationResult(
                is_valid=False,
                error_message=f"Local part exceeds maximum length of {cls.MAX_LENGTH_BYTES} bytes when encoded"
            )

        # Handle quoted local parts
        if normalized.startswith('"') and normalized.endswith('"'):
            if len(normalized) < 3:  # At least one character between quotes
                return PartValidationResult(
                    is_valid=False,
                    error_message="Empty quoted string in local part"
                )
            
            content = normalized[1:-1]
            if not cls.QUOTED_ALLOWED_CHARS.match(content):
                return PartValidationResult(
                    is_valid=False,
                    error_message="Invalid characters in quoted local part"
                )
        else:
            if not cls.UNQUOTED_ALLOWED_CHARS.match(normalized):
                return PartValidationResult(
                    is_valid=False,
                    error_message="Invalid characters in local part"
                )

        return PartValidationResult(
            is_valid=True,
            normalized_value=normalized
        )

class DomainValidator:
    """Validates the domain part of an email address."""

    # Maximum length for domain name
    MAX_LENGTH = 255
    
    # Maximum length for a domain label (part between dots)
    MAX_LABEL_LENGTH = 63
    
    # Valid characters in domain labels (after IDNA encoding)
    LABEL_CHARS = re.compile(r'^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?$')

    @classmethod
    def validate(cls, domain: str) -> PartValidationResult:
        """
        Validate domain part of email address.
        
        Args:
            domain: The domain to validate.
            
        Returns:
            PartValidationResult with validation status and normalized value.
        """
        if not domain:
            return PartValidationResult(
                is_valid=False,
                error_message="Domain cannot be empty"
            )

        try:
            # Convert to IDNA ASCII form
            normalized = idna.encode(domain, uts46=True).decode('ascii')
            
            if len(normalized) > cls.MAX_LENGTH:
                return PartValidationResult(
                    is_valid=False,
                    error_message=f"Domain exceeds maximum length of {cls.MAX_LENGTH} characters"
                )

            # Split into labels and validate each
            labels = normalized.split('.')
            
            if len(labels) < 2:
                return PartValidationResult(
                    is_valid=False,
                    error_message="Domain must have at least two parts"
                )

            for label in labels:
                if not label:
                    return PartValidationResult(
                        is_valid=False,
                        error_message="Empty label in domain name"
                    )
                    
                if len(label) > cls.MAX_LABEL_LENGTH:
                    return PartValidationResult(
                        is_valid=False,
                        error_message=f"Domain label exceeds maximum length of {cls.MAX_LABEL_LENGTH} characters"
                    )
                    
                if not cls.LABEL_CHARS.match(label):
                    return PartValidationResult(
                        is_valid=False,
                        error_message="Invalid characters in domain label"
                    )

            return PartValidationResult(
                is_valid=True,
                normalized_value=normalized
            )
            
        except idna.IDNAError as e:
            return PartValidationResult(
                is_valid=False,
                error_message=f"Invalid international domain name: {str(e)}"
            )