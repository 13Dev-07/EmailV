#!/bin/bash
# Validate the service is working correctly
echo "Validating service..."

# Check health endpoint
HEALTH_CHECK=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)
if [ $HEALTH_CHECK -ne 200 ]; then
    echo "Health check failed"
    exit 1
fi

# Check metrics endpoint
METRICS_CHECK=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/metrics)
if [ $METRICS_CHECK -ne 200 ]; then
    echo "Metrics check failed"
    exit 1
fi

echo "Service validation successful"
exit 0