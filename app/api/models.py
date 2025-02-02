"""API request and response models."""

from typing import Optional, List, Dict
from pydantic import BaseModel, EmailStr, Field

class ValidationRequest(BaseModel):
    """Email validation request model."""
    email: str = Field(..., description="Email address to validate")
    check_mx: bool = Field(True, description="Whether to perform MX record validation")
    check_smtp: bool = Field(False, description="Whether to perform SMTP verification")
    smtp_from: Optional[str] = Field(None, description="Email to use as SMTP FROM address")

class ValidationDetails(BaseModel):
    """Detailed validation results."""
    local_part: str = Field(..., description="Local part of email address")
    domain: str = Field(..., description="Domain part of email address")
    normalized_email: str = Field(..., description="Normalized form of email address")
    mx_records: Optional[List[Dict[str, str]]] = Field(None, description="MX records if checked")
    smtp_check: Optional[Dict[str, str]] = Field(None, description="SMTP check results if performed")

class ValidationResponse(BaseModel):
    """Email validation response model."""
    email: str = Field(..., description="Original email address")
    is_valid: bool = Field(..., description="Whether email is valid")
    validation_type: str = Field(..., description="Type of validation performed")
    error_message: Optional[str] = Field(None, description="Error message if validation failed")
    details: Optional[ValidationDetails] = Field(None, description="Detailed validation results")

class ValidationError(BaseModel):
    """API error response model."""
    error: str = Field(..., description="Error message")
    error_code: str = Field(..., description="Error code")
    details: Optional[Dict] = Field(None, description="Additional error details")

class HealthCheckResponse(BaseModel):
    """Health check response model."""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="Service version")
    components: Dict[str, str] = Field(..., description="Component statuses")