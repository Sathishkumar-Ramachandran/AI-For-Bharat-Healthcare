#!/bin/bash

# Healthcare Agentic System - AWS Deployment Script
# This script automates the deployment process to AWS

set -e

echo "========================================="
echo "Healthcare Agentic System - AWS Deployment"
echo "========================================="
echo ""

# Configuration
REGION="us-east-1"
STACK_NAME="healthcare-agentic-system"
APP_NAME="healthcare-system"

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI is not installed. Please install it first."
    exit 1
fi

echo "✓ AWS CLI found"

# Check AWS credentials
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS credentials not configured. Run 'aws configure' first."
    exit 1
fi

echo "✓ AWS credentials configured"

# Menu
echo ""
echo "Select deployment option:"
echo "1) Deploy with CloudFormation (Infrastructure)"
echo "2) Deploy with Elastic Beanstalk (Quick)"
echo "3) Deploy with Docker to ECS (Container)"
echo "4) Build and test Docker image locally"
echo "5) Exit"
echo ""
read -p "Enter your choice [1-5]: " choice

case $choice in
    1)
        echo ""
        echo "Deploying with CloudFormation..."
        read -p "Enter your EC2 Key Pair name: " KEY_NAME
        
        aws cloudformation create-stack \
            --stack-name $STACK_NAME \
            --template-body file://deployment/cloudformation-template.yaml \
            --parameters ParameterKey=KeyName,ParameterValue=$KEY_NAME \
            --capabilities CAPABILITY_IAM \
            --region $REGION
        
        echo "✓ CloudFormation stack creation initiated"
        echo "Monitor progress: aws cloudformation describe-stacks --stack-name $STACK_NAME"
        ;;
    
    2)
        echo ""
        echo "Deploying with Elastic Beanstalk..."
        
        # Check if EB CLI is installed
        if ! command -v eb &> /dev/null; then
            echo "Installing EB CLI..."
            pip install awsebcli
        fi
        
        # Initialize EB
        if [ ! -d ".elasticbeanstalk" ]; then
            eb init -p python-3.11 $APP_NAME --region $REGION
        fi
        
        # Create environment
        read -p "Enter environment name (e.g., healthcare-prod): " ENV_NAME
        eb create $ENV_NAME --instance-type t3.medium
        
        echo "✓ Elastic Beanstalk environment created"
        echo "Open application: eb open"
        ;;
    
    3)
        echo ""
        echo "Deploying with Docker to ECS..."
        
        # Get AWS account ID
        ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
        ECR_REPO="$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$APP_NAME"
        
        # Create ECR repository
        echo "Creating ECR repository..."
        aws ecr create-repository --repository-name $APP_NAME --region $REGION 2>/dev/null || echo "Repository already exists"
        
        # Login to ECR
        echo "Logging in to ECR..."
        aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ECR_REPO
        
        # Build image
        echo "Building Docker image..."
        docker build -t $APP_NAME .
        
        # Tag image
        echo "Tagging image..."
        docker tag $APP_NAME:latest $ECR_REPO:latest
        
        # Push to ECR
        echo "Pushing to ECR..."
        docker push $ECR_REPO:latest
        
        echo "✓ Docker image pushed to ECR"
        echo "Image URI: $ECR_REPO:latest"
        echo ""
        echo "Next steps:"
        echo "1. Create ECS cluster: aws ecs create-cluster --cluster-name healthcare-cluster"
        echo "2. Update deployment/ecs-task-definition.json with your account ID"
        echo "3. Register task definition: aws ecs register-task-definition --cli-input-json file://deployment/ecs-task-definition.json"
        echo "4. Create ECS service"
        ;;
    
    4)
        echo ""
        echo "Building and testing Docker image locally..."
        
        # Build image
        echo "Building Docker image..."
        docker build -t healthcare-agentic-system .
        
        # Run container
        echo "Starting container..."
        docker-compose up -d
        
        echo "✓ Container started"
        echo "Dashboard: http://localhost:8501"
        echo "API: http://localhost:8000"
        echo ""
        echo "View logs: docker-compose logs -f"
        echo "Stop: docker-compose down"
        ;;
    
    5)
        echo "Exiting..."
        exit 0
        ;;
    
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "========================================="
echo "Deployment process completed!"
echo "========================================="
