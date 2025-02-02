# Email Validator Configuration Guide

## Overview
This document describes the available configuration options for the Email Validator service.
All settings can be configured through environment variables with the prefix `EMAIL_VALIDATOR_`.

## Core Settings

### Service Information
- `SERVICE_NAME` (default: "email-validator"): Service identifier
- `VERSION` (default: "1.0.0"): Service version
- `DEBUG` (default: false): Enable debug mode

### API Settings
- `API_WORKERS` (default: 4): Number of API worker processes
- `API_HOST` (default: "0.0.0.0"): API service host
- `API_PORT` (default: 8000): API service port
- `API_PREFIX` (default: "/api/v1"): API endpoint prefix

### DNS Settings
- `DNS_TIMEOUT` (default: 5.0): DNS query timeout in seconds
- `DNS_CACHE_TTL` (default: 300): DNS cache TTL in seconds

### SMTP Settings
- `SMTP_TIMEOUT` (default: 10.0): SMTP connection timeout
- `SMTP_MAX_CONNECTIONS` (default: 10): Maximum concurrent SMTP connections
- `SMTP_MAX_RETRIES` (default: 3): Maximum retry attempts for SMTP operations
- `SMTP_RETRY_DELAY` (default: 1.0): Delay between retries in seconds
- `VERIFY_FROM_EMAIL`: Email address to use for SMTP verification

### Redis Settings
- `REDIS_HOST` (default: "localhost"): Redis server hostname
- `REDIS_PORT` (default: 6379): Redis server port
- `REDIS_DB` (default: 0): Redis database number
- `REDIS_PASSWORD`: Redis password if required
- `REDIS_MAX_CONNECTIONS` (default: 10): Maximum Redis connections

### Cache Settings
- `DEFAULT_CACHE_TTL` (default: 3600): Default cache TTL in seconds
- `EMAIL_VALIDATION_CACHE_TTL` (default: 86400): Email validation result cache TTL

### Rate Limiting
- `RATE_LIMIT_ENABLED` (default: true): Enable rate limiting
- `DEFAULT_RATE_LIMIT` (default: 100): Default requests per window
- `DEFAULT_RATE_WINDOW` (default: 60): Rate limit window in seconds

### Logging
- `LOG_LEVEL` (default: "INFO"): Logging level
- `LOG_FORMAT`: Log message format

### Metrics
- `METRICS_ENABLED` (default: true): Enable Prometheus metrics
- `METRICS_PORT` (default: 9090): Metrics endpoint port

## Examples

### Basic Configuration
```bash
export EMAIL_VALIDATOR_API_PORT=8080
export EMAIL_VALIDATOR_LOG_LEVEL=DEBUG
export EMAIL_VALIDATOR_REDIS_HOST=redis.example.com
```

### Production Configuration
```bash
export EMAIL_VALIDATOR_DEBUG=false
export EMAIL_VALIDATOR_API_WORKERS=8
export EMAIL_VALIDATOR_RATE_LIMIT_ENABLED=true
export EMAIL_VALIDATOR_DEFAULT_RATE_LIMIT=1000
export EMAIL_VALIDATOR_SMTP_MAX_CONNECTIONS=20
```