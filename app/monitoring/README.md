# Monitoring Components

This directory contains monitoring components for various aspects of the application.

## Component Overview

### SMTP Health Check System
- `smtp_health_check.py`: Performs health checks on SMTP connections
- `health_check_scheduler.py`: Schedules periodic health checks
- `health_manager.py`: Manages overall health status of connections

### Metrics Collection
- `smtp_metrics.py`: SMTP-specific metrics collection
- `connection_pool_monitor.py`: Connection pool monitoring
- `enhanced_metrics.py`: Enhanced application metrics

## Integration Points

The monitoring system integrates with:
1. Prometheus for metrics collection
2. Connection pooling for health monitoring
3. Application logging for error tracking

## Usage Example

```python
from monitoring.health_manager import HealthManager
from monitoring.smtp_metrics import SMTPMetrics

# Initialize health manager
health_manager = HealthManager(check_interval=300)

# Start health checks
await health_manager.start()

# Record metrics
SMTPMetrics.record_connection_error("smtp.example.com", "ConnectionTimeout")
```

## Metrics Overview

### SMTP Connection Metrics
- Connection pool size
- Connection errors
- Connection lifetime
- Operation duration

### Health Check Metrics
- Health check duration
- Failed health checks
- Last check timestamp

## Configuration

Health check intervals and thresholds can be configured via environment variables:

```env
SMTP_HEALTH_CHECK_INTERVAL=300  # seconds
SMTP_CONNECTION_TIMEOUT=30      # seconds
SMTP_MAX_RETRIES=3
```

## Alerting

Critical metrics are configured to trigger alerts:
1. High error rate
2. Pool exhaustion
3. Failed health checks