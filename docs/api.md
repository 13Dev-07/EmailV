# Email Validator API Documentation

## Overview
The Email Validator service provides a robust HTTP API for validating email addresses through various methods including syntax checking, DNS verification, and SMTP validation.

## Base URL
```
https://api.emailvalidator.com/v1
```

## Authentication
All API requests require an API key to be included in the HTTP headers:
```
Authorization: Bearer your-api-key-here
```

## Endpoints

### Validate Email
Validates an email address using all available methods.

**Endpoint:** `POST /validate`

**Request Body:**
```json
{
    "email": "test@example.com",
    "options": {
        "verify_smtp": true,
        "check_dns": true,
        "use_cache": true
    }
}
```

**Parameters:**
- `email` (required): The email address to validate
- `options` (optional):
  - `verify_smtp` (default: true): Perform SMTP verification
  - `check_dns` (default: true): Verify DNS records
  - `use_cache` (default: true): Use cached results if available

**Response (200 OK):**
```json
{
    "is_valid": true,
    "validation_time": 0.523,
    "details": {
        "syntax_valid": true,
        "has_mx_record": true,
        "smtp_check": {
            "is_valid": true,
            "smtp_response": "OK",
            "mx_used": "mx1.example.com"
        },
        "cached": false
    }
}
```

**Error Response (400 Bad Request):**
```json
{
    "error": "Invalid email format",
    "code": "INVALID_FORMAT",
    "details": "Email must be a valid format"
}
```

### Batch Validation
Validate multiple email addresses in a single request.

**Endpoint:** `POST /validate/batch`

**Request Body:**
```json
{
    "emails": [
        "test1@example.com",
        "test2@example.com"
    ],
    "options": {
        "verify_smtp": true,
        "check_dns": true,
        "use_cache": true
    }
}
```

**Response (200 OK):**
```json
{
    "results": [
        {
            "email": "test1@example.com",
            "is_valid": true,
            "checks": {
                "syntax": true,
                "dns": true,
                "smtp": true
            },
            "metadata": {
                "domain": "example.com",
                "has_mx_record": true,
                "timestamp": "2023-01-01T12:00:00Z"
            }
        },
        {
            "email": "test2@example.com",
            "is_valid": true,
            "checks": {
                "syntax": true,
                "dns": true,
                "smtp": true
            },
            "metadata": {
                "domain": "example.com",
                "has_mx_record": true,
                "timestamp": "2023-01-01T12:00:00Z"
            }
        }
    ],
    "summary": {
        "total": 2,
        "valid": 2,
        "invalid": 0,
        "processing_time": "0.245s"
    }
}
```

**Error Responses:**
- `400 Bad Request`: Invalid request format or malformed email addresses
  ```json
  {
    "error": "Invalid request format",
    "details": "The request body must contain an 'emails' array"
  }
  ```
- `401 Unauthorized`: Missing or invalid API key
  ```json
  {
    "error": "Unauthorized",
    "details": "Invalid or expired API key"
  }
  ```
- `429 Too Many Requests`: Rate limit exceeded
  ```json
  {
    "error": "Rate limit exceeded",
    "details": "Please try again in 60 seconds",
    "retry_after": 60
  }
  ```
- `500 Internal Server Error`: Server-side error
  ```json
  {
    "error": "Internal server error",
    "request_id": "req_abc123"
  }
  ```

**Example Request:**
```bash
curl -X POST https://api.emailvalidator.com/v1/validate/batch \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "emails": ["user@example.com", "contact@company.com"],
    "options": {
        "verify_smtp": true,
        "check_dns": true,
        "use_cache": true
    }
}'
```
```json
{
    "results": [
        {
            "email": "test1@example.com",
            "is_valid": true,
            "details": {
                "syntax_valid": true,
                "has_mx_record": true,
                "smtp_check": {
                    "is_valid": true,
                    "smtp_response": "OK"
                }
            }
        },
        {
            "email": "test2@example.com",
            "is_valid": false,
            "details": {
                "syntax_valid": true,
                "has_mx_record": false,
                "error": "No MX records found"
            }
        }
    ],
    "validation_time": 1.245
}
```

### Health Check
Get the current service status.

**Endpoint:** `GET /health`

**Response (200 OK):**
```json
{
    "status": "healthy",
    "version": "1.0.0",
    "uptime": 3600
}
```

## Rate Limiting
- Free tier: 100 requests per minute
- Pro tier: 1000 requests per minute
- Enterprise tier: Custom limits

Rate limit information is included in response headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
```

## Error Codes
- `INVALID_FORMAT`: Email format is invalid
- `DNS_ERROR`: Unable to verify DNS records
- `SMTP_ERROR`: SMTP verification failed
- `RATE_LIMITED`: Too many requests
- `INVALID_AUTH`: Invalid or missing API key
- `SERVER_ERROR`: Internal server error

## Best Practices
1. Always implement retry logic with exponential backoff
2. Use batch validation for multiple emails
3. Enable caching for better performance
4. Handle rate limits gracefully
5. Check response headers for rate limit status

## Examples
See [USAGE.md](./USAGE.md) for detailed code examples in various programming languages.