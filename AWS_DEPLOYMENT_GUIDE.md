# AWS Deployment Guide - Healthcare Agentic System

## 🎯 Deployment Overview

This guide covers deploying the Healthcare Agentic System to AWS using multiple deployment options.

## 📋 Prerequisites

- AWS Account with appropriate permissions
- AWS CLI installed and configured
- Docker installed (for containerized deployment)
- Domain name (optional, for custom domain)

## 🏗️ Architecture Options

### Option 1: AWS Elastic Beanstalk (Recommended for Quick Deploy)
- **Best for**: Quick deployment, managed infrastructure
- **Services**: Elastic Beanstalk, RDS, S3
- **Estimated Cost**: $50-100/month

### Option 2: AWS ECS with Fargate (Recommended for Production)
- **Best for**: Scalable, containerized deployment
- **Services**: ECS, Fargate, ALB, RDS, S3
- **Estimated Cost**: $100-200/month

### Option 3: AWS EC2 (Manual Setup)
- **Best for**: Full control, custom configuration
- **Services**: EC2, RDS, S3
- **Estimated Cost**: $50-150/month

## 🚀 Option 1: AWS Elastic Beanstalk Deployment

### Step 1: Prepare Application

1. **Install EB CLI**:
```bash
pip install awsebcli
```

2. **Initialize Elastic Beanstalk**:
```bash
eb init -p python-3.11 healthcare-agentic-system --region us-east-1
```

3. **Create Environment**:
```bash
eb create healthcare-prod --instance-type t3.medium
```

### Step 2: Configure Environment Variables

```bash
eb setenv \
  AWS_ACCESS_KEY_ID=your_key \
  AWS_SECRET_ACCESS_KEY=your_secret \
  AWS_REGION=us-east-1 \
  NOVA_MODEL_ID=us.amazon.nova-lite-v1:0
```

### Step 3: Deploy

```bash
eb deploy
```

### Step 4: Access Application

```bash
eb open
```

## 🐳 Option 2: AWS ECS with Fargate (Containerized)

### Step 1: Create Dockerfile

See `Dockerfile` in project root.

### Step 2: Build and Push to ECR

```bash
# Create ECR repository
aws ecr create-repository --repository-name healthcare-agentic-system

# Get login token
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Build image
docker build -t healthcare-agentic-system .

# Tag image
docker tag healthcare-agentic-system:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/healthcare-agentic-system:latest

# Push to ECR
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/healthcare-agentic-system:latest
```

### Step 3: Create ECS Cluster

```bash
aws ecs create-cluster --cluster-name healthcare-cluster
```

### Step 4: Create Task Definition

See `ecs-task-definition.json` in deployment folder.

```bash
aws ecs register-task-definition --cli-input-json file://deployment/ecs-task-definition.json
```

### Step 5: Create Service

```bash
aws ecs create-service \
  --cluster healthcare-cluster \
  --service-name healthcare-service \
  --task-definition healthcare-task \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

## 🖥️ Option 3: AWS EC2 Deployment

### Step 1: Launch EC2 Instance

```bash
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t3.medium \
  --key-name your-key-pair \
  --security-group-ids sg-xxx \
  --subnet-id subnet-xxx \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=healthcare-server}]'
```

### Step 2: Connect and Setup

```bash
# SSH into instance
ssh -i your-key.pem ec2-user@your-instance-ip

# Update system
sudo yum update -y

# Install Python 3.11
sudo yum install python3.11 -y

# Install git
sudo yum install git -y

# Clone repository
git clone your-repo-url
cd healthcare-agentic-system

# Install dependencies
pip3.11 install -r requirements.txt

# Setup environment variables
cp .env.example .env
nano .env  # Edit with your AWS credentials

# Initialize database
python3.11 database/init_db.py
```

### Step 3: Setup Systemd Service

Create `/etc/systemd/system/healthcare-dashboard.service`:

```ini
[Unit]
Description=Healthcare Agentic System Dashboard
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/healthcare-agentic-system
Environment="PATH=/usr/local/bin:/usr/bin:/bin"
ExecStart=/usr/bin/python3.11 run_dashboard.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Create `/etc/systemd/system/healthcare-api.service`:

```ini
[Unit]
Description=Healthcare Agentic System API
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/healthcare-agentic-system
Environment="PATH=/usr/local/bin:/usr/bin:/bin"
ExecStart=/usr/bin/python3.11 run_api.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start services:

```bash
sudo systemctl enable healthcare-dashboard
sudo systemctl enable healthcare-api
sudo systemctl start healthcare-dashboard
sudo systemctl start healthcare-api
```

## 🗄️ Database Setup (RDS)

### Create RDS PostgreSQL Instance

```bash
aws rds create-db-instance \
  --db-instance-identifier healthcare-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username admin \
  --master-user-password YourPassword123! \
  --allocated-storage 20 \
  --vpc-security-group-ids sg-xxx \
  --db-subnet-group-name your-subnet-group \
  --backup-retention-period 7 \
  --publicly-accessible
```

### Update Application to Use RDS

Update `services/mcp_server.py` to use PostgreSQL instead of SQLite.

## 🔒 Security Configuration

### 1. Security Groups

**Application Security Group**:
- Inbound: Port 8000 (API), Port 8501 (Dashboard) from ALB
- Outbound: All traffic

**Database Security Group**:
- Inbound: Port 5432 from Application SG
- Outbound: None

**Load Balancer Security Group**:
- Inbound: Port 80, 443 from 0.0.0.0/0
- Outbound: All traffic

### 2. IAM Roles

Create IAM role for EC2/ECS with policies:
- AmazonBedrockFullAccess
- AmazonS3ReadOnlyAccess (for data files)
- CloudWatchLogsFullAccess

### 3. Secrets Manager

Store sensitive data in AWS Secrets Manager:

```bash
aws secretsmanager create-secret \
  --name healthcare/credentials \
  --secret-string '{"AWS_ACCESS_KEY_ID":"xxx","AWS_SECRET_ACCESS_KEY":"xxx"}'
```

## 🌐 Load Balancer Setup

### Create Application Load Balancer

```bash
aws elbv2 create-load-balancer \
  --name healthcare-alb \
  --subnets subnet-xxx subnet-yyy \
  --security-groups sg-xxx \
  --scheme internet-facing \
  --type application
```

### Create Target Groups

```bash
# Dashboard target group
aws elbv2 create-target-group \
  --name healthcare-dashboard-tg \
  --protocol HTTP \
  --port 8501 \
  --vpc-id vpc-xxx \
  --health-check-path /

# API target group
aws elbv2 create-target-group \
  --name healthcare-api-tg \
  --protocol HTTP \
  --port 8000 \
  --vpc-id vpc-xxx \
  --health-check-path /dashboard
```

### Create Listeners

```bash
# Dashboard listener
aws elbv2 create-listener \
  --load-balancer-arn arn:aws:elasticloadbalancing:... \
  --protocol HTTP \
  --port 80 \
  --default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:...

# API listener
aws elbv2 create-listener \
  --load-balancer-arn arn:aws:elasticloadbalancing:... \
  --protocol HTTP \
  --port 8000 \
  --default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:...
```

## 📊 Monitoring & Logging

### CloudWatch Logs

```bash
# Create log group
aws logs create-log-group --log-group-name /aws/healthcare-system

# Create log streams
aws logs create-log-stream \
  --log-group-name /aws/healthcare-system \
  --log-stream-name dashboard

aws logs create-log-stream \
  --log-group-name /aws/healthcare-system \
  --log-stream-name api
```

### CloudWatch Alarms

```bash
# CPU utilization alarm
aws cloudwatch put-metric-alarm \
  --alarm-name healthcare-high-cpu \
  --alarm-description "Alert when CPU exceeds 80%" \
  --metric-name CPUUtilization \
  --namespace AWS/EC2 \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2
```

## 🔄 Auto Scaling

### Create Auto Scaling Group (for EC2)

```bash
# Create launch template
aws ec2 create-launch-template \
  --launch-template-name healthcare-template \
  --version-description "Healthcare system v1" \
  --launch-template-data file://launch-template.json

# Create auto scaling group
aws autoscaling create-auto-scaling-group \
  --auto-scaling-group-name healthcare-asg \
  --launch-template LaunchTemplateName=healthcare-template \
  --min-size 2 \
  --max-size 10 \
  --desired-capacity 2 \
  --vpc-zone-identifier "subnet-xxx,subnet-yyy" \
  --target-group-arns arn:aws:elasticloadbalancing:...
```

## 🌍 Domain & SSL

### 1. Route 53 Setup

```bash
# Create hosted zone
aws route53 create-hosted-zone \
  --name healthcare.example.com \
  --caller-reference $(date +%s)

# Create A record pointing to ALB
aws route53 change-resource-record-sets \
  --hosted-zone-id Z123456 \
  --change-batch file://route53-change.json
```

### 2. SSL Certificate (ACM)

```bash
# Request certificate
aws acm request-certificate \
  --domain-name healthcare.example.com \
  --validation-method DNS \
  --subject-alternative-names *.healthcare.example.com
```

### 3. Update ALB Listener for HTTPS

```bash
aws elbv2 create-listener \
  --load-balancer-arn arn:aws:elasticloadbalancing:... \
  --protocol HTTPS \
  --port 443 \
  --certificates CertificateArn=arn:aws:acm:... \
  --default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:...
```

## 💰 Cost Optimization

### 1. Use Reserved Instances
- Save up to 72% for predictable workloads

### 2. Use Spot Instances
- Save up to 90% for non-critical workloads

### 3. Right-Size Resources
- Start with t3.small, scale as needed

### 4. Use S3 for Static Assets
- Store data files in S3 instead of EBS

### 5. Enable Auto Scaling
- Scale down during off-peak hours

## 📝 Deployment Checklist

- [ ] AWS account setup
- [ ] IAM roles and policies configured
- [ ] Security groups created
- [ ] RDS database provisioned
- [ ] Application deployed
- [ ] Load balancer configured
- [ ] Domain and SSL setup
- [ ] Monitoring and logging enabled
- [ ] Auto scaling configured
- [ ] Backup strategy implemented
- [ ] Security audit completed
- [ ] Performance testing done
- [ ] Documentation updated

## 🔧 Troubleshooting

### Application Won't Start
- Check CloudWatch logs
- Verify environment variables
- Check security group rules
- Verify IAM permissions

### Database Connection Issues
- Check RDS security group
- Verify connection string
- Check RDS status
- Test connectivity from EC2

### High Latency
- Check CloudWatch metrics
- Enable caching
- Optimize database queries
- Scale up resources

## 📚 Additional Resources

- [AWS Elastic Beanstalk Documentation](https://docs.aws.amazon.com/elasticbeanstalk/)
- [AWS ECS Documentation](https://docs.aws.amazon.com/ecs/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)

## 🆘 Support

For deployment issues:
1. Check CloudWatch logs
2. Review security group rules
3. Verify IAM permissions
4. Test locally first
5. Contact AWS Support if needed

---

**Deployment Version**: 1.0.0
**Last Updated**: 2024
**Status**: Production Ready
