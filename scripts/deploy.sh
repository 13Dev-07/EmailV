#!/bin/bash
set -e

# Configuration
ENVIRONMENT=$1
REGION="us-west-2"
CLUSTER_NAME="email-validator-${ENVIRONMENT}"

# Ensure environment is provided
if [ -z "$ENVIRONMENT" ]; then
    echo "Usage: $0 <environment>"
    exit 1
fi

# Update kubeconfig
aws eks update-kubeconfig --name $CLUSTER_NAME --region $REGION

# Apply secrets first
echo "Applying secrets..."
kubectl apply -f k8s/secrets-${ENVIRONMENT}.yml

# Apply deployments
echo "Applying Kubernetes configurations..."
kubectl apply -f k8s/deployment.yml
kubectl apply -f k8s/service.yml

# Wait for deployment to complete
echo "Waiting for deployment to complete..."
kubectl rollout status deployment/email-validator

echo "Deployment completed successfully!"