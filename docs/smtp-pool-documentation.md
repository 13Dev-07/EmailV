# SMTP Connection Pool Documentation

## Overview

The SMTP connection pool provides efficient management of SMTP connections with the following features:
- Connection lifecycle management
- Health monitoring
- Automatic recovery
- Performance metrics
- Both synchronous and asynchronous implementations

## Components

### 1. Connection Pool

#### Synchronous Version (`SMTPConnectionPool`)
```python
pool = SMTPConnectionPool(
    max_connections=10,
    connection_timeout=30,
    max_lifetime=3600,
    cleanup_interval=300
)

with pool.get_connection("smtp.example.com") as conn:
    # Use connection
```

#### Asynchronous Version (`SMTPConnectionPoolAsync`)
```python
pool = SMTPConnectionPoolAsync(
    max_connections=10,
    connection_timeout=30
)

async with pool.get_connection("smtp.example.com") as conn:
    # Use connection
```

### 2. Health Checks

Regular health checks ensure connection validity:
```python
health_manager = HealthManager(check_interval=300)
await health_manager.start()
```

### 3. Monitoring

Comprehensive metrics collection:
```python
# Record connection error
SMTPMetrics.record_connection_error("smtp.example.com", "ConnectionTimeout")

# Update pool size
SMTPMetrics.update_pool_size("smtp.example.com", "active", 1)
```

## Configuration

Example configuration:
```python
SMTP_CONFIG = {
    "max_connections": 10,
    "connection_timeout": 30,
    "max_lifetime": 3600,
    "cleanup_interval": 300,
    "max_retries": 3,
    "health_check_interval": 300
}
```

## Metrics

Available metrics:
- Connection pool size
- Connection errors
- Connection lifetime
- Operation duration
- Health check results

## Error Handling

The pool handles various error scenarios:
- Connection failures
- Health check failures
- Pool exhaustion
- Timeout errors

## Best Practices

1. Use async implementation for high-throughput scenarios
2. Configure appropriate pool sizes based on load
3. Monitor connection metrics
4. Set up alerts for error conditions
5. Regularly review health check results

## Integration

### With Prometheus
```python
# Metrics are automatically collected
SMTP_POOL_SIZE.labels(server="smtp.example.com", state="active").set(5)
```

### With Logging
```python
logger.info("Connection pool status: %d active connections", active_count)
```

## Example Usage

```python
async def validate_email(email: str) -> bool:
    async with smtp_pool.get_connection(smtp_server) as conn:
        try:
            await conn.verify_email(email)
            return True
        except SMTPException:
            return False
```