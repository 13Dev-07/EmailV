"""
Email Validation API Endpoints
RESTful endpoints for email validation services.
"""

from fastapi import FastAPI, HTTPException, Depends, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from app.utils.validation_orchestrator import (
    validate_email,
    validate_emails_batch
)
from app.utils.rate_limiter import RateLimiter
from app.utils.authentication import verify_api_key
from app.utils.metrics import (
    API_REQUESTS,
    API_ERRORS,
    API_LATENCY,
    VALIDATION_RESULTS
)
from app.utils.logger import get_logger

logger = get_logger(__name__)
rate_limiter = RateLimiter()
app = FastAPI(
    title="Email Validation API",
    description="Enterprise-grade email validation service",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EmailRequest(BaseModel):
    """Single email validation request."""
    email: EmailStr

class BatchEmailRequest(BaseModel):
    """Batch email validation request."""
    emails: List[EmailStr]
    batch_size: Optional[int] = 50

@app.post("/validate/email")
async def validate_single_email(
    request: Request,
    email_req: EmailRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Validate a single email address.
    
    Args:
        request: FastAPI request object
        email_req: Email validation request
        api_key: API key for authentication
        
    Returns:
        Validation results
    """
    # Rate limiting check
    if not rate_limiter.check_rate_limit(api_key):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded"
        )
        
    try:
        # Track metrics
        API_REQUESTS.labels(endpoint="single", status="attempt").inc()
        
        # Perform validation
        result = validate_email(email_req.email)
        
        # Update metrics
        API_REQUESTS.labels(endpoint="single", status="success").inc()
        VALIDATION_RESULTS.labels(
            result="valid" if result["syntax_valid"] else "invalid"
        ).inc()
        
        return result
        
    except Exception as e:
        # Log error
        logger.error(f"Validation failed for {email_req.email}: {str(e)}")
        
        # Update error metrics
        API_ERRORS.labels(
            endpoint="single",
            error_type=type(e).__name__
        ).inc()
        
        raise HTTPException(
            status_code=500,
            detail=f"Validation failed: {str(e)}"
        )

@app.post("/validate/batch")
async def validate_email_batch(
    request: Request,
    batch_req: BatchEmailRequest,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(verify_api_key)
):
    """
    Validate multiple email addresses in batch.
    
    Args:
        request: FastAPI request object
        batch_req: Batch validation request
        background_tasks: FastAPI background tasks
        api_key: API key for authentication
        
    Returns:
        List of validation results
    """
    # Rate limiting check with batch multiplier
    batch_size = len(batch_req.emails)
    if not rate_limiter.check_rate_limit(api_key, multiplier=batch_size):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded"
        )
        
    try:
        # Track metrics
        API_REQUESTS.labels(endpoint="batch", status="attempt").inc()
        
        # Perform batch validation
        results = await validate_emails_batch(
            batch_req.emails,
            batch_req.batch_size
        )
        
        # Update metrics in background
        def update_metrics():
            API_REQUESTS.labels(endpoint="batch", status="success").inc()
            for result in results:
                VALIDATION_RESULTS.labels(
                    result="valid" if result["syntax_valid"] else "invalid"
                ).inc()
                
        background_tasks.add_task(update_metrics)
        
        return results
        
    except Exception as e:
        # Log error
        logger.error(f"Batch validation failed: {str(e)}")
        
        # Update error metrics
        API_ERRORS.labels(
            endpoint="batch",
            error_type=type(e).__name__
        ).inc()
        
        raise HTTPException(
            status_code=500,
            detail=f"Batch validation failed: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.get("/metrics")
async def get_metrics():
    """Get API metrics."""
    return {
        "requests": {
            "total": sum(API_REQUESTS._value.values()),
            "errors": sum(API_ERRORS._value.values())
        },
        "validations": {
            "valid": VALIDATION_RESULTS.labels(result="valid")._value,
            "invalid": VALIDATION_RESULTS.labels(result="invalid")._value
        }
    }