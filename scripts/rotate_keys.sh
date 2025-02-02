#!/bin/bash
set -e

# Generate new API key
NEW_API_KEY=$(openssl rand -base64 32)

# Update secret in AWS Secrets Manager
aws secretsmanager update-secret \
    --secret-id email-validator/api-key \
    --secret-string "$NEW_API_KEY"

# Update Kubernetes secret
kubectl create secret generic email-validator-secrets \
    --from-literal=api-key="$NEW_API_KEY" \
    --dry-run=client -o yaml | \
    kubectl apply -f -

# Restart pods to pick up new secret
kubectl rollout restart deployment email-validator

echo "API key rotated successfully!"