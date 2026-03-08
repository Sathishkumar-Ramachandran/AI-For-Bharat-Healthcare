# Serverless Deployment - Quick Start

## 🎯 AWS App Runner (Like GCP Cloud Run)

Deploy your Healthcare Agentic System as a serverless application that:
- ✅ **Scales to zero** when not in use
- ✅ **Pay per request** only
- ✅ **Auto-scales** from 0 to 1000+ instances
- ✅ **No server management** required

## 💰 Cost Comparison

| Traffic Level | Traditional EC2 | Serverless (App Runner) | Savings |
|--------------|-----------------|------------------------|---------|
| Low (1K req/day) | $30/month | $5/month | 83% |
| Medium (10K req/day) | $30/month | $15/month | 50% |
| High (100K req/day) | $100/month | $50/month | 50% |

**Key Benefit**: With low traffic, you pay almost nothing!

## 🚀 One-Command Deployment

```bash
chmod +x deployment/deploy-serverless.sh
./deployment/deploy-serverless.sh
```

**That's it!** The script will:
1. Build Docker image
2. Push to AWS ECR
3. Create App Runner service
4. Configure auto-scaling
5. Give you the URL

**Time**: 10 minutes
**Cost**: $5-20/month for typical usage

## 📋 Prerequisites

```bash
# 1. Install AWS CLI
pip install awscli

# 2. Configure credentials
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Region: us-east-1

# 3. Install Docker
# Download from: https://www.docker.com/
```

## 🎯 Manual Deployment (Step by Step)

### Step 1: Build and Push Docker Image

```bash
# Get your AWS account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Create ECR repository
aws ecr create-repository --repository-name healthcare-system

# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Build image
docker build -t healthcare-system .

# Tag and push
docker tag healthcare-system:latest $ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/healthcare-system:latest
docker push $ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/healthcare-system:latest
```

### Step 2: Create App Runner Service

```bash
# Create IAM role
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

# Attach policy
aws iam attach-role-policy \
  --role-name AppRunnerECRAccessRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSAppRunnerServicePolicyForECRAccess

# Create service (update YOUR_ACCOUNT_ID in deployment/apprunner-config.json first)
aws apprunner create-service \
  --service-name healthcare-system \
  --source-configuration file://deployment/apprunner-config.json \
  --instance-configuration '{
    "Cpu": "1 vCPU",
    "Memory": "2 GB"
  }' \
  --health-check-configuration '{
    "Protocol": "HTTP",
    "Path": "/dashboard",
    "Interval": 10
  }'
```

### Step 3: Get Your URL

```bash
# Get service URL
aws apprunner list-services --query 'ServiceSummaryList[0].ServiceUrl' --output text
```

Your app will be at: `https://xxxxx.us-east-1.awsapprunner.com`

## 🔍 Monitoring

### View Logs
```bash
aws logs tail /aws/apprunner/healthcare-system/application --follow
```

### Check Status
```bash
aws apprunner list-services
```

### View Metrics
```bash
aws cloudwatch get-metric-statistics \
  --namespace AWS/AppRunner \
  --metric-name RequestCount \
  --dimensions Name=ServiceName,Value=healthcare-system \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Sum
```

## 🔄 Update Deployment

```bash
# Build new image
docker build -t healthcare-system .
docker tag healthcare-system:latest $ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/healthcare-system:latest
docker push $ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/healthcare-system:latest

# App Runner will auto-deploy the new image!
```

## 🗑️ Delete Service

```bash
# Get service ARN
SERVICE_ARN=$(aws apprunner list-services --query 'ServiceSummaryList[0].ServiceArn' --output text)

# Delete service
aws apprunner delete-service --service-arn $SERVICE_ARN
```

## 📊 Cost Breakdown

### Example: 1000 requests/day

```
Active time: ~2 hours/day
Compute: 2 hours × 30 days × $0.007/vCPU-hour = $4.20
Memory: 2 hours × 30 days × 2GB × $0.0008/GB-hour = $0.96
Requests: 30,000 × $0.001/1000 = $0.03

Total: ~$5.19/month
```

### Example: 10,000 requests/day

```
Active time: ~8 hours/day
Compute: 8 hours × 30 days × $0.007/vCPU-hour = $16.80
Memory: 8 hours × 30 days × 2GB × $0.0008/GB-hour = $3.84
Requests: 300,000 × $0.001/1000 = $0.30

Total: ~$20.94/month
```

## ✅ Features

- ✅ **Auto-scaling**: 0 to 1000+ instances
- ✅ **Pay per request**: No idle costs
- ✅ **Automatic HTTPS**: SSL included
- ✅ **Health checks**: Automatic monitoring
- ✅ **Zero downtime**: Rolling deployments
- ✅ **Custom domains**: Bring your own domain
- ✅ **VPC support**: Private networking
- ✅ **CloudWatch**: Logs and metrics

## 🆚 Comparison with Other Options

| Feature | App Runner | Lambda | EC2 | Fargate |
|---------|-----------|--------|-----|---------|
| Scales to Zero | ✅ | ✅ | ❌ | ⚠️ |
| Container Support | ✅ | ⚠️ | ✅ | ✅ |
| Ease of Use | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| Cost (Low Traffic) | $5 | $2 | $30 | $30 |
| Setup Time | 10 min | 15 min | 30 min | 20 min |

## 🎉 Success Indicators

After deployment, verify:
- [ ] Service URL accessible
- [ ] Dashboard loads
- [ ] API responds
- [ ] Amazon Nova working
- [ ] Logs visible
- [ ] Auto-scaling enabled

## 🆘 Troubleshooting

### Service Won't Start
```bash
# Check operations
aws apprunner list-operations --service-arn YOUR_SERVICE_ARN

# View logs
aws logs tail /aws/apprunner/healthcare-system/application --follow
```

### High Costs
- Check CloudWatch metrics
- Verify auto-scaling configuration
- Consider reducing instance size

### Slow Response
- Check cold start time
- Consider keeping 1 instance warm
- Optimize Docker image size

## 📚 Additional Resources

- **Full Guide**: `deployment/SERVERLESS_DEPLOYMENT.md`
- **Comparison**: `deployment/serverless-comparison.md`
- **AWS Docs**: https://docs.aws.amazon.com/apprunner/

---

## 🚀 Ready to Deploy?

Run this command:
```bash
./deployment/deploy-serverless.sh
```

**Estimated Time**: 10 minutes
**Estimated Cost**: $5-20/month
**Difficulty**: ⭐ Easy

Your serverless Healthcare Agentic System will be live in minutes! 🎉

---

**Version**: 1.0.0
**Status**: Production Ready
**Best For**: Cost-effective, auto-scaling deployment
