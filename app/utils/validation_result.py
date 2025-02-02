"""
Module for handling email validation results.
"""
from dataclasses import dataclass
from typing import Optional, List, Dict

@dataclass
class ValidationResult:
    """
    Represents the result of an email validation operation.
    """
    is_valid: bool
    email: str
    syntax_valid: bool
    mx_found: bool
    smtp_check: bool
    disposable: bool = False
    role_account: bool = False
    free_provider: bool = False
    errors: List[str] = None
    warnings: List[str] = None
    details: Dict[str, any] = None
    
    def __init__(self, email: str):
        self.email = email
        self.is_valid = False
        self.syntax_valid = False
        self.mx_found = False
        self.smtp_check = False
        self.errors = []
        self.warnings = []
        self.details = {}
    
    def add_error(self, error: str) -> None:
        """Add an error message to the validation result."""
        if self.errors is None:
            self.errors = []
        self.errors.append(error)
        self.is_valid = False

    def add_warning(self, warning: str) -> None:
        """Add a warning message to the validation result."""
        if self.warnings is None:
            self.warnings = []
        self.warnings.append(warning)

    def add_detail(self, key: str, value: any) -> None:
        """Add a detail to the validation result."""
        self.details[key] = value

    def to_dict(self) -> Dict[str, any]:
        """Convert the validation result to a dictionary."""
        return {
            "is_valid": self.is_valid,
            "email": self.email,
            "syntax_valid": self.syntax_valid,
            "mx_found": self.mx_found,
            "smtp_check": self.smtp_check,
            "disposable": self.disposable,
            "role_account": self.role_account,
            "free_provider": self.free_provider,
            "errors": self.errors,
            "warnings": self.warnings,
            "details": self.details
        }