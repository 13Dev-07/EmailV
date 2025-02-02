# Production Deployment Guide

## Prerequisites
- AWS CLI configured with appropriate permissions
- kubectl installed and configured
- Helm 3.x installed
- Docker installed and logged into ECR

## Pre-deployment Steps
1. Create required AWS resources:
```bash
# Create ECR repository
aws ecr create-repository --repository-name email-validator

# Create EKS cluster (if not exists)
eksctl create cluster -f k8s/cluster.yaml
```

2. Configure secrets:
```bash
# Create production secrets
cp k8s/secrets-template.yml k8s/secrets-production.yml
# Edit secrets-production.yml with actual values
```

3. Configure DNS and SSL:
```bash
# Install cert-manager
helm repo add jetstack https://charts.jetstack.io
helm install cert-manager jetstack/cert-manager --namespace cert-manager --create-namespace --version v1.7.1 --set installCRDs=true
```

## Deployment Steps
1. Build and push Docker image:
```bash
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
docker build -t email-validator .
docker tag email-validator:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/email-validator:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/email-validator:latest
```

2. Deploy application:
```bash
# Deploy application
./scripts/deploy.sh production

# Verify deployment
kubectl get pods
kubectl get services
kubectl get ingress
```

3. Set up monitoring:
```bash
# Initialize monitoring
./scripts/initialize_monitoring.sh

# Access Grafana
kubectl port-forward service/prometheus-grafana 3000:80 -n monitoring
```

## Post-deployment Verification
1. Verify API endpoints:
```bash
curl -X GET https://api.emailvalidator.com/health
curl -X GET https://api.emailvalidator.com/metrics
```

2. Check monitoring:
- Access Grafana dashboard at http://localhost:3000
- Verify metrics are being collected
- Check alerting rules

3. Verify autoscaling:
```bash
kubectl get hpa
```

## Backup and Maintenance
1. Database backups:
```bash
# Automated daily backups
./scripts/backup.sh
```

2. Log management:
```bash
# View application logs
kubectl logs -l app=email-validator
```

3. Resource scaling:
```bash
# Scale deployment
kubectl scale deployment email-validator --replicas=5
```

## Emergency Procedures
1. Rollback deployment:
```bash
kubectl rollout undo deployment/email-validator
```

2. Database restore:
```bash
./scripts/restore.sh <backup-date>
```

## Monitoring and Alerts
- Configure alert receivers in alertmanager-config
- Set up PagerDuty/Slack integration
- Review and adjust alert thresholds

## Security Considerations
- Regularly rotate API keys and secrets
- Monitor security logs
- Keep dependencies updated
- Run regular security scans

## Troubleshooting
Common issues and solutions:
1. Pod startup issues:
   ```bash
   kubectl describe pod <pod-name>
   kubectl logs <pod-name>
   ```

2. Connection issues:
   ```bash
   kubectl get endpoints
   kubectl describe service email-validator
   ```

3. Performance issues:
   - Check Grafana dashboards
   - Review resource utilization
   - Check connection pool metrics