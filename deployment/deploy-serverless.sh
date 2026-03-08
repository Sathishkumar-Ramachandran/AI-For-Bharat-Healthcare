#!/bin/bash

# Healthcare Agentic System - Serverless Deployment to AWS App Runner
# Similar to GCP Cloud Run - Pay per request, auto-scale to zero

set -e

echo "========================================="
echo "Serverless Deployment to AWS App Runner"
echo "========================================="
echo ""

# Configuration
REGION="us-east-1"
SERVICE_NAME="healthcare-system"
REPO_NAME="healthcare-system"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check AWS CLI
if ! command -v aws &> /dev/null; then
    echo -e "${RED}❌ AWS CLI not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ AWS CLI found${NC}"

# Get AWS Account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
echo -e "${GREEN}✓ AWS Account: $ACCOUNT_ID${NC}"

# ECR Repository URL
ECR_REPO="$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO_NAME"

echo ""
echo "Step 1: Creating ECR Repository..."
aws ecr create-repository --repository-name $REPO_NAME --region $REGION 2>/dev/null || echo "Repository already exists"
echo -e "${GREEN}✓ ECR Repository ready${NC}"

echo ""
echo "Step 2: Building Docker Image..."
docker build -t $REPO_NAME .
echo -e "${GREEN}✓ Docker image built${NC}"

echo ""
echo "Step 3: Logging into ECR..."
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ECR_REPO
echo -e "${GREEN}✓ Logged into ECR${NC}"

echo ""
echo "Step 4: Tagging and Pushing Image..."
docker tag $REPO_NAME:latest $ECR_REPO:latest
docker push $ECR_REPO:latest
echo -e "${GREEN}✓ Image pushed to ECR${NC}"

echo ""
echo "Step 5: Creating IAM Role for App Runner..."

# Create trust policy
cat > /tmp/apprunner-trust-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {"Service": "build.apprunner.amazonaws.com"},
    "Action": "sts:AssumeRole"
  }]
}
EOF

# Create role
aws iam create-role \
  --role-name AppRunnerECRAccessRole \
  --assume-role-policy-document file:///tmp/apprunner-trust-policy.json \
  2>/dev/null || echo "Role already exists"

# Attach policy
aws iam attach-role-policy \
  --role-name AppRunnerECRAccessRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSAppRunnerServicePolicyForECRAccess \
  2>/dev/null || echo "Policy already attached"

echo -e "${GREEN}✓ IAM Role configured${NC}"

echo ""
echo "Step 6: Creating App Runner Service..."

# Update config with account ID
sed "s/YOUR_ACCOUNT_ID/$ACCOUNT_ID/g" deployment/apprunner-config.json > /tmp/apprunner-config.json

# Create service
SERVICE_ARN=$(aws apprunner create-service \
  --service-name $SERVICE_NAME \
  --source-configuration file:///tmp/apprunner-config.json \
  --instance-configuration '{
    "Cpu": "1 vCPU",
    "Memory": "2 GB",
    "InstanceRoleArn": "arn:aws:iam::'$ACCOUNT_ID':role/AppRunnerECRAccessRole"
  }' \
  --health-check-configuration '{
    "Protocol": "HTTP",
    "Path": "/dashboard",
    "Interval": 10,
    "Timeout": 5,
    "HealthyThreshold": 1,
    "UnhealthyThreshold": 5
  }' \
  --region $REGION \
  --query 'Service.ServiceArn' \
  --output text 2>/dev/null || echo "Service already exists")

if [ -z "$SERVICE_ARN" ]; then
    # Get existing service ARN
    SERVICE_ARN=$(aws apprunner list-services --region $REGION --query "ServiceSummaryList[?ServiceName=='$SERVICE_NAME'].ServiceArn" --output text)
    
    if [ ! -z "$SERVICE_ARN" ]; then
        echo -e "${YELLOW}Service exists, updating...${NC}"
        aws apprunner update-service \
          --service-arn $SERVICE_ARN \
          --source-configuration file:///tmp/apprunner-config.json \
          --region $REGION
    fi
fi

echo -e "${GREEN}✓ App Runner service created/updated${NC}"

echo ""
echo "Step 7: Waiting for service to be ready..."
echo "This may take 3-5 minutes..."

# Wait for service to be running
for i in {1..60}; do
    STATUS=$(aws apprunner describe-service --service-arn $SERVICE_ARN --region $REGION --query 'Service.Status' --output text)
    if [ "$STATUS" == "RUNNING" ]; then
        break
    fi
    echo -n "."
    sleep 5
done

echo ""

if [ "$STATUS" == "RUNNING" ]; then
    echo -e "${GREEN}✓ Service is running!${NC}"
    
    # Get service URL
    SERVICE_URL=$(aws apprunner describe-service --service-arn $SERVICE_ARN --region $REGION --query 'Service.ServiceUrl' --output text)
    
    echo ""
    echo "========================================="
    echo -e "${GREEN}🎉 Deployment Successful!${NC}"
    echo "========================================="
    echo ""
    echo -e "${YELLOW}Service URL:${NC} https://$SERVICE_URL"
    echo -e "${YELLOW}Service ARN:${NC} $SERVICE_ARN"
    echo ""
    echo "Features:"
    echo "  ✓ Auto-scales from 0 to 1000+ instances"
    echo "  ✓ Pay only for requests"
    echo "  ✓ Fully managed (no servers)"
    echo "  ✓ Automatic HTTPS"
    echo ""
    echo "Estimated Cost: \$5-20/month for low traffic"
    echo ""
    echo "Access your application:"
    echo "  Dashboard: https://$SERVICE_URL"
    echo "  API: https://$SERVICE_URL/dashboard"
    echo ""
    echo "Monitor service:"
    echo "  aws apprunner describe-service --service-arn $SERVICE_ARN"
    echo ""
    echo "View logs:"
    echo "  aws logs tail /aws/apprunner/$SERVICE_NAME/application --follow"
    echo ""
    echo "========================================="
else
    echo -e "${RED}❌ Service deployment failed${NC}"
    echo "Check logs: aws apprunner list-operations --service-arn $SERVICE_ARN"
    exit 1
fi

# Cleanup temp files
rm -f /tmp/apprunner-trust-policy.json /tmp/apprunner-config.json

echo ""
echo "Deployment complete! 🚀"
