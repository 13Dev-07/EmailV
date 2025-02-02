# Kubernetes Deployment Configuration

This directory contains Kubernetes configurations for deploying the email validation service.

## Structure

```
k8s/
├── base/             # Base configurations
│   ├── deployment.yaml
│   ├── service.yaml
│   └── configmap.yaml
├── staging/         # Staging environment overlays
│   └── kustomization.yaml
└── production/      # Production environment overlays
    └── kustomization.yaml
```

## Deployment

### Staging

```bash
# Deploy to staging
kubectl apply -k k8s/staging/

# Check deployment status
kubectl -n staging get pods
kubectl -n staging describe deployment staging-email-validator
```

### Production

```bash
# Deploy to production
kubectl apply -k k8s/production/

# Check deployment status
kubectl -n production get pods
kubectl -n production describe deployment prod-email-validator
```

## Monitoring

Access metrics:
```bash
# Port-forward Prometheus service
kubectl port-forward -n monitoring svc/prometheus 9090:9090

# Check application metrics
curl http://localhost:8000/metrics
```

## Scaling

The service can be scaled horizontally:
```bash
# Scale replicas
kubectl -n production scale deployment/prod-email-validator --replicas=7
```

## Configuration

Update ConfigMap values:
```bash
kubectl -n production create configmap email-validator-config \
  --from-file=k8s/base/configmap.yaml \
  -o yaml --dry-run=client | kubectl apply -f -
```