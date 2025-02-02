# Production Deployment Runbook

## 1. Prerequisites
- AWS account with appropriate IAM permissions
- Docker installed on deployment machine
- Access to production configuration values
- SSL certificates for domain

## 2. Infrastructure Setup

### 2.1 Network Configuration
1. Create VPC with appropriate subnets
```bash
aws ec2 create-vpc --cidr-block 10.0.0.0/16
aws ec2 create-subnet --vpc-id vpc-xxx --cidr-block 10.0.1.0/24
aws ec2 create-subnet --vpc-id vpc-xxx --cidr-block 10.0.2.0/24
```

2. Configure security groups
```bash
aws ec2 create-security-group \
    --group-name email-validator-sg \
    --description "Security group for Email Validator service"
```

### 2.2 Database Setup
1. Create Redis cluster
```bash
aws elasticache create-cache-cluster \
    --cache-cluster-id email-validator-cache \
    --engine redis \
    --cache-node-type cache.t3.micro \
    --num-cache-nodes 1
```

2. Configure Redis replication group for high availability
```bash
aws elasticache create-replication-group \
    --replication-group-id email-validator-cache-ha \
    --replication-group-description "HA group for Email Validator" \
    --automatic-failover-enabled
```

## 3. Application Deployment

### 3.1 Container Registry Setup
1. Create ECR repository
```bash
aws ecr create-repository --repository-name email-validator
```

2. Build and push Docker image
```bash
docker build -t email-validator .
docker tag email-validator:latest ${ECR_REPO_URI}:latest
docker push ${ECR_REPO_URI}:latest
```

### 3.2 ECS Service Deployment
1. Create ECS cluster
```bash
aws ecs create-cluster --cluster-name email-validator-cluster
```

2. Create task definition
```bash
aws ecs register-task-definition \
    --family email-validator \
    --container-definitions file://task-definition.json
```

3. Create ECS service
```bash
aws ecs create-service \
    --cluster email-validator-cluster \
    --service-name email-validator-service \
    --task-definition email-validator:1 \
    --desired-count 2
```

## 4. Monitoring Setup

### 4.1 CloudWatch Configuration
1. Create log groups
```bash
aws logs create-log-group --log-group-name /ecs/email-validator
```

2. Set up metrics and alarms
```bash
aws cloudwatch put-metric-alarm \
    --alarm-name api-latency-high \
    --metric-name Latency \
    --namespace AWS/ECS \
    --threshold 1.0 \
    --period 300
```

### 4.2 Dashboard Setup
1. Create CloudWatch dashboard
```bash
aws cloudwatch put-dashboard \
    --dashboard-name email-validator \
    --dashboard-body file://dashboard.json
```

## 5. SSL/TLS Configuration

### 5.1 Certificate Setup
1. Request ACM certificate
```bash
aws acm request-certificate \
    --domain-name api.emailvalidator.com \
    --validation-method DNS
```

2. Create Application Load Balancer
```bash
aws elbv2 create-load-balancer \
    --name email-validator-alb \
    --subnets subnet-xxx subnet-yyy \
    --security-groups sg-xxx
```

## 6. Backup and Recovery

### 6.1 Backup Configuration
1. Configure Redis backup
```bash
aws elasticache modify-cache-cluster \
    --cache-cluster-id email-validator-cache \
    --snapshot-retention-limit 7
```

2. Set up automated snapshots
```bash
aws elasticache create-snapshot \
    --cache-cluster-id email-validator-cache \
    --snapshot-name manual-backup-1
```

### 6.2 Recovery Procedures
1. Restore from backup
```bash
aws elasticache restore-cache-cluster \
    --cache-cluster-id email-validator-cache-restored \
    --snapshot-name backup-2023-01-01
```

## 7. Scaling Configuration

### 7.1 Auto Scaling Setup
1. Create Auto Scaling group
```bash
aws application-autoscaling register-scalable-target \
    --service-namespace ecs \
    --scalable-dimension ecs:service:DesiredCount \
    --resource-id service/email-validator-cluster/email-validator-service \
    --min-capacity 2 \
    --max-capacity 10
```

2. Configure scaling policies
```bash
aws application-autoscaling put-scaling-policy \
    --policy-name cpu-tracking \
    --policy-type TargetTrackingScaling \
    --resource-id service/email-validator-cluster/email-validator-service \
    --service-namespace ecs \
    --scalable-dimension ecs:service:DesiredCount \
    --target-tracking-scaling-policy-configuration file://scaling-policy.json
```

## 8. Troubleshooting Guide

### 8.1 Common Issues
1. High API Latency
   - Check Redis connection pool
   - Verify auto-scaling is working
   - Monitor CPU/Memory usage

2. Increased Error Rates
   - Check application logs
   - Verify DNS resolution
   - Check rate limiter configuration

### 8.2 Recovery Steps
1. Service Degradation
   ```bash
   # Restart ECS tasks
   aws ecs update-service \
       --cluster email-validator-cluster \
       --service email-validator-service \
       --force-new-deployment
   ```

2. Cache Issues
   ```bash
   # Flush Redis cache
   aws elasticache modify-cache-cluster \
       --cache-cluster-id email-validator-cache \
       --apply-immediately
   ```

## 9. Release Process

### 9.1 Deployment Steps
1. Tag release
```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

2. Build and push new image
```bash
docker build -t email-validator:v1.0.0 .
docker push ${ECR_REPO_URI}:v1.0.0
```

3. Update ECS service
```bash
aws ecs update-service \
    --cluster email-validator-cluster \
    --service email-validator-service \
    --task-definition email-validator:latest
```

### 9.2 Rollback Procedure
1. Revert to previous version
```bash
aws ecs update-service \
    --cluster email-validator-cluster \
    --service email-validator-service \
    --task-definition email-validator:previous
```