# Serverless Deployment Guide - AWS App Runner

## 🎯 Overview

Deploy Healthcare Agentic System as a serverless application that:
- ✅ Scales to zero when not in use (pay only for requests)
- ✅ Auto-scales based on traffic
- ✅ No server management required
- ✅ Similar to GCP Cloud Run

## 🚀 AWS App Runner (Recommended - Like Cloud Run)

AWS App Runner is the closest equivalent to GCP Cloud Run in AWS.

### Features
- **Pay per request**: Only charged when handling requests
- **Auto-scaling**: 0 to 1000+ instances automatically
- **No infrastructure**: Fully managed
- **Container-based**: Uses your Docker image
- **Cost-effective**: ~$5-20/month for low traffic

### Quick Deploy

```bash
# 1. Build and push Docker image to ECR
aws ecr create-repository --repository-name healthcare-system

# Get login
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com

# Build and push
docker build -t healthcare-system .
docker tag healthcare-system:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/healthcare-system:latest
docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/healthcare-system:latest

# 2. Create App Runner service
aws apprunner create-service --cli-input-json file://deployment/apprunner-config.json
```

### Cost Comparison

| Service | Idle Cost | Active Cost | Best For |
|---------|-----------|-------------|----------|
| App Runner | $0 | $0.007/vCPU-hour + $0.0008/GB-hour | Serverless, auto-scale |
| Lambda | $0 | $0.20/1M requests | API only |
| Fargate | ~$30/month | $0.04/vCPU-hour | Always-on |
| EC2 | ~$30/month | Fixed | Traditional |

**App Runner Example**: 
- 1000 requests/day
- 2 vCPU, 4GB RAM
- Average 30 seconds per request
- **Cost**: ~$5-10/month

## 📦 Option 1: AWS App Runner (Recommended)

### Step 1: Prepare Application

Your application is already containerized with the `Dockerfile`.

### Step 2: Create App Runner Service

```bash
# Using AWS CLI
aws apprunner create-service \
  --service-name healthcare-system \
  --source-configuration '{
    "ImageRepository": {
      "ImageIdentifier": "YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/healthcare-system:latest",
      "ImageRepositoryType": "ECR",
      "ImageConfiguration": {
        "Port": "8000",
        "RuntimeEnvironmentVariables": {
          "AWS_REGION": "us-east-1",
          "NOVA_MODEL_ID": "us.amazon.nova-lite-v1:0"
        }
      }
    },
    "AutoDeploymentsEnabled": true
  }' \
  --instance-configuration '{
    "Cpu": "1 vCPU",
    "Memory": "2 GB"
  }' \
  --health-check-configuration '{
    "Protocol": "HTTP",
    "Path": "/dashboard",
    "Interval": 10,
    "Timeout": 5,
    "HealthyThreshold": 1,
    "UnhealthyThreshold": 5
  }'
```

### Step 3: Access Your Application

```bash
# Get service URL
aws apprunner describe-service --service-arn YOUR_SERVICE_ARN --query 'Service.ServiceUrl'
```

Your application will be available at: `https://xxxxx.us-east-1.awsapprunner.com`

## 🔥 Option 2: AWS Lambda + API Gateway (Pure Serverless)

For API-only deployment (without Streamlit dashboard).

### Architecture
```
API Gateway → Lambda Function → Amazon Bedrock
```

### Step 1: Create Lambda Handler

See `deployment/lambda_handler.py`

### Step 2: Package and Deploy

```bash
# Install dependencies
pip install -r requirements.txt -t package/

# Copy application code
cp -r agents services config data package/

# Create deployment package
cd package
zip -r ../lambda-deployment.zip .
cd ..
zip -g lambda-deployment.zip deployment/lambda_handler.py

# Create Lambda function
aws lambda create-function \
  --function-name healthcare-api \
  --runtime python3.11 \
  --role arn:aws:iam::YOUR_ACCOUNT:role/lambda-execution-role \
  --handler lambda_handler.lambda_handler \
  --zip-file fileb://lambda-deployment.zip \
  --timeout 300 \
  --memory-size 1024 \
  --environment Variables="{AWS_REGION=us-east-1,NOVA_MODEL_ID=us.amazon.nova-lite-v1:0}"
```

### Step 3: Create API Gateway

```bash
# Create REST API
aws apigateway create-rest-api --name healthcare-api

# Create resource and method
# Link to Lambda function
# Deploy API
```

## 🌐 Option 3: AWS Fargate with Auto-Scaling to Zero

Fargate can scale down to 0 tasks when not in use.

### Configuration

```yaml
# deployment/fargate-serverless.yaml
AutoScalingConfiguration:
  MinCapacity: 0  # Scale to zero
  MaxCapacity: 10
  TargetTrackingScaling:
    TargetValue: 70
    ScaleInCooldown: 300
    ScaleOutCooldown: 60
```

## 📊 Detailed Cost Analysis

### App Runner (Recommended)
```
Provisioned instances: 1 vCPU, 2 GB RAM
Active time: 2 hours/day (low traffic)

Compute: 2 hours × 30 days × $0.007/vCPU-hour = $4.20
Memory: 2 hours × 30 days × 2 GB × $0.0008/GB-hour = $0.96
Requests: 1000/day × 30 × $0.001/1000 = $0.03

Total: ~$5.19/month
```

### Lambda
```
Requests: 30,000/month
Duration: 5 seconds average
Memory: 1024 MB

Compute: 30,000 × 5s × $0.0000166667 = $2.50
Requests: 30,000 × $0.0000002 = $0.006

Total: ~$2.51/month
```

### Comparison with Always-On
```
EC2 t3.medium: ~$30/month (always running)
Fargate (always-on): ~$40/month
App Runner (serverless): ~$5/month (low traffic)
Lambda: ~$2.50/month (API only)
```

**Savings**: 80-90% for low to medium traffic!

## 🔧 Complete App Runner Setup

### 1. Create IAM Role

```bash
# Create role for App Runner
aws iam create-role \
  --role-name AppRunnerECRAccessRole \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "build.apprunner.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }'

# Attach ECR access policy
aws iam attach-role-policy \
  --role-name AppRunnerECRAccessRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSAppRunnerServicePolicyForECRAccess
```

### 2. Create Service with Auto-Scaling

```bash
aws apprunner create-service \
  --service-name healthcare-system \
  --source-configuration file://deployment/apprunner-config.json \
  --instance-configuration '{
    "Cpu": "1 vCPU",
    "Memory": "2 GB",
    "InstanceRoleArn": "arn:aws:iam::YOUR_ACCOUNT:role/AppRunnerInstanceRole"
  }' \
  --auto-scaling-configuration-arn arn:aws:apprunner:us-east-1:YOUR_ACCOUNT:autoscalingconfiguration/DefaultConfiguration/1/00000000000000000000000000000001
```

### 3. Configure Custom Domain (Optional)

```bash
# Associate custom domain
aws apprunner associate-custom-domain \
  --service-arn YOUR_SERVICE_ARN \
  --domain-name healthcare.yourdomain.com
```

## 🔒 Security Configuration

### Environment Variables (Secrets)

```bash
# Store secrets in AWS Secrets Manager
aws secretsmanager create-secret \
  --name healthcare/app-secrets \
  --secret-string '{
    "AWS_ACCESS_KEY_ID": "xxx",
    "AWS_SECRET_ACCESS_KEY": "xxx"
  }'

# Reference in App Runner
"RuntimeEnvironmentSecrets": {
  "AWS_ACCESS_KEY_ID": "arn:aws:secretsmanager:us-east-1:ACCOUNT:secret:healthcare/app-secrets:AWS_ACCESS_KEY_ID::",
  "AWS_SECRET_ACCESS_KEY": "arn:aws:secretsmanager:us-east-1:ACCOUNT:secret:healthcare/app-secrets:AWS_SECRET_ACCESS_KEY::"
}
```

## 📈 Auto-Scaling Configuration

### App Runner Auto-Scaling

```json
{
  "AutoScalingConfigurationName": "healthcare-autoscaling",
  "MaxConcurrency": 100,
  "MinSize": 1,
  "MaxSize": 10
}
```

- **MinSize**: Minimum instances (set to 1, scales to 0 when idle)
- **MaxSize**: Maximum instances
- **MaxConcurrency**: Requests per instance

## 🔄 CI/CD Pipeline

### Automated Deployment

```yaml
# .github/workflows/deploy-apprunner.yml
name: Deploy to App Runner

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v1
      
      - name: Build and push image
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          ECR_REPOSITORY: healthcare-system
          IMAGE_TAG: ${{ github.sha }}
        run: |
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
      
      - name: Deploy to App Runner
        run: |
          aws apprunner update-service \
            --service-arn ${{ secrets.APPRUNNER_SERVICE_ARN }} \
            --source-configuration ImageRepository={ImageIdentifier=$ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG}
```

## 🎯 Best Practices

### 1. Cold Start Optimization

```python
# Optimize imports
import sys
sys.path.insert(0, '/opt/python')

# Pre-load models
from services.bedrock_client import bedrock_client
bedrock_client.invoke_nova("warmup", "warmup")  # Warm up connection
```

### 2. Connection Pooling

```python
# Reuse connections
import boto3
from functools import lru_cache

@lru_cache(maxsize=1)
def get_bedrock_client():
    return boto3.client('bedrock-runtime', region_name='us-east-1')
```

### 3. Caching

```python
# Cache frequently accessed data
from functools import lru_cache

@lru_cache(maxsize=100)
def get_pharmacy_inventory():
    return mcp_server.get_pharmacy_inventory()
```

## 📊 Monitoring

### CloudWatch Metrics

```bash
# View App Runner metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/AppRunner \
  --metric-name RequestCount \
  --dimensions Name=ServiceName,Value=healthcare-system \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-02T00:00:00Z \
  --period 3600 \
  --statistics Sum
```

### Key Metrics
- Request count
- Response time
- Error rate
- Active instances
- CPU/Memory utilization

## 🆘 Troubleshooting

### Service Won't Start
```bash
# Check service logs
aws apprunner list-operations --service-arn YOUR_SERVICE_ARN

# View logs in CloudWatch
aws logs tail /aws/apprunner/healthcare-system/application --follow
```

### High Cold Start Time
- Optimize Docker image size
- Use lighter base image
- Pre-load critical dependencies
- Consider keeping 1 instance warm

### Database Connection Issues
- Use connection pooling
- Implement retry logic
- Consider Aurora Serverless for database

## ✅ Deployment Checklist

- [ ] Docker image built and tested
- [ ] ECR repository created
- [ ] Image pushed to ECR
- [ ] IAM roles configured
- [ ] App Runner service created
- [ ] Environment variables set
- [ ] Health checks configured
- [ ] Custom domain configured (optional)
- [ ] Monitoring enabled
- [ ] Auto-scaling tested

## 🎉 Success Criteria

- ✅ Service accessible via URL
- ✅ Scales to zero when idle
- ✅ Auto-scales with traffic
- ✅ Response time < 3 seconds
- ✅ Cost < $20/month for low traffic
- ✅ 99.9% uptime

---

## 🚀 Quick Start Command

```bash
# One-command deployment
./deployment/deploy-serverless.sh
```

This will:
1. Build Docker image
2. Push to ECR
3. Create App Runner service
4. Configure auto-scaling
5. Output service URL

**Estimated Time**: 10 minutes
**Estimated Cost**: $5-20/month
**Scaling**: 0 to 1000+ instances automatically

---

**Version**: 1.0.0
**Status**: Production Ready
**Best For**: Cost-effective, serverless deployment
