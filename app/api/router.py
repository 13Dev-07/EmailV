"""API router and endpoint implementations."""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Optional, List
import asyncio
import logging
from datetime import datetime

from app.api.models import (
    ValidationRequest,
    ValidationResponse,
    ValidationError,
    ValidationDetails,
    HealthCheckResponse
)
from app.validators import RFC5322EmailValidator
from app.dns_resolver import DNSResolver
from app.smtp_validator import SMTPValidator
from app.monitoring.prometheus_metrics import MetricsCollector, track_time
from app.caching.redis_client import RedisClient, RedisCacheManager

logger = logging.getLogger(__name__)
router = APIRouter()
metrics = MetricsCollector()

async def get_validators():
    """Get validator instances."""
    dns_resolver = DNSResolver()
    smtp_validator = SMTPValidator(dns_resolver=dns_resolver)
    return RFC5322EmailValidator(), dns_resolver, smtp_validator

@router.post("/validate", response_model=ValidationResponse)
@track_time(metrics.EMAIL_VALIDATION_DURATION.labels(validation_type="full"))
async def validate_email(
    request: ValidationRequest,
    background_tasks: BackgroundTasks,
    validators: tuple = Depends(get_validators)
) -> ValidationResponse:
    """
    Validate email address with specified checks.
    
    Args:
        request: Validation request parameters
        background_tasks: FastAPI background tasks
        validators: Tuple of validator instances
    
    Returns:
        ValidationResponse with results
        
    Raises:
        HTTPException: If validation fails
    """
    syntax_validator, dns_resolver, smtp_validator = validators
    validation_type = "syntax"
    
    try:
        # Start with syntax validation
        syntax_result = syntax_validator.validate_email(request.email)
        if not syntax_result.is_valid:
            return ValidationResponse(
                email=request.email,
                is_valid=False,
                validation_type=validation_type,
                error_message=syntax_result.error_message
            )
            
        details = ValidationDetails(**syntax_result.details)
        
        # Perform MX validation if requested
        if request.check_mx:
            validation_type = "mx"
            mx_records = await dns_resolver.resolve_mx(details.domain)
            
            if not mx_records:
                return ValidationResponse(
                    email=request.email,
                    is_valid=False,
                    validation_type=validation_type,
                    error_message="No MX records found for domain",
                    details=details
                )
                
            details.mx_records = [
                {
                    "host": record.value,
                    "priority": record.priority or 0
                }
                for record in mx_records
            ]
        
        # Perform SMTP validation if requested
        if request.check_smtp:
            validation_type = "smtp"
            smtp_result = await smtp_validator.verify_email(
                request.email,
                sender=request.smtp_from
            )
            
            if not smtp_result.is_valid:
                return ValidationResponse(
                    email=request.email,
                    is_valid=False,
                    validation_type=validation_type,
                    error_message=smtp_result.error_message,
                    details=details
                )
                
            details.smtp_check = {
                "mx_used": smtp_result.mx_used,
                "response": smtp_result.smtp_response
            }
        
        # Schedule cleanup in background
        background_tasks.add_task(smtp_validator.close)
        
        return ValidationResponse(
            email=request.email,
            is_valid=True,
            validation_type=validation_type,
            details=details
        )
        
    except Exception as e:
        logger.error(f"Validation error for {request.email}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=ValidationError(
                error="Internal validation error",
                error_code="INTERNAL_ERROR",
                details={"message": str(e)}
            ).dict()
        )

@router.get("/health")
async def health_check() -> HealthCheckResponse:
    """Check service health status."""
    try:
        # Basic component checks
        redis = RedisClient()
        await redis.get_async_pool()
        redis_status = "healthy"
    except Exception as e:
        redis_status = f"unhealthy: {str(e)}"
    
    try:
        resolver = DNSResolver()
        await resolver.resolve_mx("gmail.com")
        dns_status = "healthy"
    except Exception as e:
        dns_status = f"unhealthy: {str(e)}"
        
    return HealthCheckResponse(
        status="healthy",
        version="1.0.0",
        components={
            "redis": redis_status,
            "dns": dns_status
        }
    )

@router.get("/metrics")
async def get_metrics():
    """Get prometheus metrics."""
    from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
    
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )