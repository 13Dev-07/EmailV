#!/bin/bash
# Run pre-deployment tasks
echo "Running pre-deployment tasks..."

# Verify environment variables
if [ -z "$AWS_REGION" ] || [ -z "$ECS_CLUSTER" ] || [ -z "$ECS_SERVICE" ]; then
    echo "Required environment variables are not set"
    exit 1
fi

# Run database migrations if needed
echo "Running database migrations..."
python manage.py migrate --noinput

exit 0