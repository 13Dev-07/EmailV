#!/bin/bash
set -e

# Install Prometheus Operator
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack \
    --namespace monitoring \
    --create-namespace \
    --values k8s/prometheus-values.yml

# Install Grafana dashboards
kubectl apply -f k8s/grafana-dashboards/

# Wait for deployments
echo "Waiting for Prometheus and Grafana to be ready..."
kubectl -n monitoring rollout status deployment/prometheus-grafana
kubectl -n monitoring rollout status statefulset/prometheus-prometheus-kube-prometheus-prometheus

echo "Monitoring setup completed successfully!"