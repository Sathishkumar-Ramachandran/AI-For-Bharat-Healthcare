# Quick AWS Deployment Guide

## 🚀 Fastest Way to Deploy

### Option 1: One-Command Deployment (Elastic Beanstalk)

```bash
# Install EB CLI
pip install awsebcli

# Initialize and deploy
eb init -p python-3.11 healthcare-system --region us-east-1
eb create healthcare-prod --instance-type t3.medium

# Set environment variables
eb setenv AWS_ACCESS_KEY_ID=your_key AWS_SECRET_ACCESS_KEY=your_secret AWS_REGION=us-east-1

# Open application
eb open
```

**Time**: ~10 minutes
**Cost**: ~$50/month

### Option 2: Docker Deployment (Local Test)

```bash
# Build and run
docker-compose up -d

# Access
# Dashboard: http://localhost:8501
# API: http://localhost:8000
```

**Time**: ~5 minutes
**Cost**: Free (local)

### Option 3: Automated Script

```bash
# Make script executable
chmod +x deployment/deploy-to-aws.sh

# Run deployment script
./deployment/deploy-to-aws.sh
```

Follow the interactive prompts to choose your deployment method.

## 📋 Pre-Deployment Checklist

- [ ] AWS account created
- [ ] AWS CLI installed (`pip install awscli`)
- [ ] AWS credentials configured (`aws configure`)
- [ ] Docker installed (for container deployment)
- [ ] Domain name ready (optional)

## 🔑 Required AWS Credentials

Set these environment variables or use `aws configure`:

```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_REGION=us-east-1
```

## 🌐 Post-Deployment

After deployment, you'll get:
- **Load Balancer URL**: Access your application
- **CloudWatch Logs**: Monitor application
- **Auto Scaling**: Automatic scaling based on load

## 💰 Estimated Costs

| Deployment Type | Monthly Cost |
|----------------|--------------|
| Elastic Beanstalk (t3.medium) | $50-80 |
| ECS Fargate (2 tasks) | $100-150 |
| EC2 (t3.medium) | $40-60 |

## 🆘 Troubleshooting

### Deployment Fails
```bash
# Check logs
eb logs
# or
aws logs tail /aws/elasticbeanstalk/healthcare-prod --follow
```

### Application Not Accessible
- Check security group rules
- Verify load balancer health checks
- Check CloudWatch logs

### Database Connection Issues
- Verify RDS security group
- Check connection string
- Test from EC2 instance

## 📚 Next Steps

1. **Setup Custom Domain**: See AWS_DEPLOYMENT_GUIDE.md
2. **Enable HTTPS**: Configure SSL certificate
3. **Setup Monitoring**: CloudWatch alarms
4. **Configure Backups**: RDS automated backups
5. **Implement CI/CD**: AWS CodePipeline

## 🔗 Useful Commands

```bash
# Elastic Beanstalk
eb status                    # Check status
eb logs                      # View logs
eb ssh                       # SSH into instance
eb deploy                    # Deploy updates
eb terminate                 # Terminate environment

# Docker
docker-compose up -d         # Start
docker-compose logs -f       # View logs
docker-compose down          # Stop

# AWS CLI
aws cloudformation describe-stacks --stack-name healthcare-agentic-system
aws ecs list-clusters
aws rds describe-db-instances
```

## ✅ Success Indicators

- [ ] Application accessible via URL
- [ ] Dashboard loads correctly
- [ ] API responds to requests
- [ ] Database connected
- [ ] Amazon Nova LLM working
- [ ] Health checks passing
- [ ] Logs visible in CloudWatch

---

**Need Help?** Check the full AWS_DEPLOYMENT_GUIDE.md for detailed instructions.
