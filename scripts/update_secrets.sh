#!/bin/bash
set -e

ENVIRONMENT=$1

if [ -z "$ENVIRONMENT" ]; then
    echo "Usage: $0 <environment>"
    exit 1
fi

# Source environment variables
source .env.${ENVIRONMENT}

# Create secrets file from template
envsubst < k8s/secrets-template.yml > k8s/secrets-${ENVIRONMENT}.yml

# Apply secrets
kubectl apply -f k8s/secrets-${ENVIRONMENT}.yml

echo "Secrets updated successfully!"