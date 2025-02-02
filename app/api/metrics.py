"""
API Metrics Module
Defines Prometheus metrics for API monitoring.
"""

from prometheus_client import Counter, Histogram, Gauge

# Request metrics
API_REQUESTS = Counter(
    'email_validator_api_requests_total',
    'Total API requests',
    ['endpoint', 'status']
)

API_ERRORS = Counter(
    'email_validator_api_errors_total',
    'API errors by type',
    ['endpoint', 'error_type']
)

API_LATENCY = Histogram(
    'email_validator_api_latency_seconds',
    'API endpoint latency',
    ['endpoint']
)

# Validation result metrics
VALIDATION_RESULTS = Counter(
    'email_validator_results_total',
    'Validation results',
    ['result']  # valid/invalid
)

# Authentication metrics
AUTH_FAILURES = Counter(
    'email_validator_auth_failures_total',
    'Authentication failures',
    ['reason']
)

# Rate limiting metrics
RATE_LIMIT_EXCEEDED = Counter(
    'email_validator_rate_limit_exceeded_total',
    'Rate limit exceeded count',
    ['tier']
)

# Active client metrics
ACTIVE_CLIENTS = Gauge(
    'email_validator_active_clients',
    'Number of active API clients',
    ['tier']
)