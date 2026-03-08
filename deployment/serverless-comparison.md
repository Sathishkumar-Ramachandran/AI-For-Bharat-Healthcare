# Serverless Options Comparison

## AWS Serverless Services vs GCP Cloud Run

| Feature | AWS App Runner | AWS Lambda | GCP Cloud Run |
|---------|---------------|------------|---------------|
| **Pricing Model** | Pay per request | Pay per invocation | Pay per request |
| **Scales to Zero** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Container Support** | ✅ Yes | ⚠️ Limited | ✅ Yes |
| **Max Timeout** | No limit | 15 minutes | 60 minutes |
| **Cold Start** | 2-5 seconds | 1-3 seconds | 2-4 seconds |
| **Ease of Use** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Best For** | Web apps | APIs, Functions | Web apps |

## Recommendation: AWS App Runner

**Why App Runner is like Cloud Run:**
- ✅ Container-based deployment
- ✅ Automatic HTTPS
- ✅ Auto-scaling (0 to 1000+)
- ✅ Pay per request
- ✅ No infrastructure management
- ✅ Simple deployment

## Cost Comparison (1000 requests/day)

### AWS App Runner
```
Compute: 2 hours/day × 30 days × $0.007/vCPU-hour = $4.20
Memory: 2 hours/day × 30 days × 2GB × $0.0008/GB-hour = $0.96
Requests: 30,000 × $0.001/1000 = $0.03
Total: ~$5.19/month
```

### AWS Lambda
```
Requests: 30,000 × $0.0000002 = $0.006
Compute: 30,000 × 5s × $0.0000166667 = $2.50
Total: ~$2.51/month
```

### GCP Cloud Run
```
Requests: 30,000 × $0.40/1M = $0.012
CPU: 2 hours/day × 30 days × 1 vCPU × $0.00002400/vCPU-second = $5.18
Memory: 2 hours/day × 30 days × 2GB × $0.00000250/GB-second = $1.08
Total: ~$6.28/month
```

### Traditional EC2
```
t3.medium: $30.37/month (always running)
```

**Savings: 80-90% with serverless!**

## Feature Matrix

| Feature | App Runner | Lambda | Cloud Run |
|---------|-----------|--------|-----------|
| Streamlit Support | ✅ | ❌ | ✅ |
| FastAPI Support | ✅ | ✅ | ✅ |
| WebSocket | ✅ | ❌ | ✅ |
| Custom Domain | ✅ | ✅ | ✅ |
| Auto HTTPS | ✅ | ✅ | ✅ |
| VPC Support | ✅ | ✅ | ✅ |
| CI/CD Integration | ✅ | ✅ | ✅ |

## Deployment Time

| Service | Initial Deploy | Update Deploy |
|---------|---------------|---------------|
| App Runner | 5-10 min | 3-5 min |
| Lambda | 2-5 min | 1-2 min |
| Cloud Run | 3-7 min | 2-4 min |

## When to Use Each

### Use App Runner When:
- ✅ You want Cloud Run-like experience in AWS
- ✅ You have a containerized web application
- ✅ You need both dashboard and API
- ✅ You want simple deployment
- ✅ You need WebSocket support

### Use Lambda When:
- ✅ You only need API endpoints
- ✅ You want lowest cost
- ✅ You have short-running functions
- ✅ You need event-driven architecture
- ✅ You don't need Streamlit dashboard

### Use Fargate When:
- ✅ You need more control
- ✅ You have complex networking
- ✅ You need persistent connections
- ✅ You want ECS ecosystem

## Migration from Cloud Run to App Runner

Very similar! Main differences:

| Cloud Run | App Runner |
|-----------|-----------|
| `gcloud run deploy` | `aws apprunner create-service` |
| Cloud Build | ECR + Docker |
| IAM | IAM |
| Cloud Logging | CloudWatch |
| Cloud Monitoring | CloudWatch |

## Quick Start Commands

### App Runner (Recommended)
```bash
./deployment/deploy-serverless.sh
```

### Lambda
```bash
./deployment/deploy-lambda.sh
```

### Cloud Run (for comparison)
```bash
gcloud run deploy healthcare-system \
  --image gcr.io/PROJECT/healthcare-system \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## Conclusion

**For Healthcare Agentic System:**
- ✅ **Best Choice**: AWS App Runner
- ✅ **Most Similar to Cloud Run**: App Runner
- ✅ **Lowest Cost**: Lambda (API only)
- ✅ **Best Performance**: App Runner or Fargate

**Recommendation**: Use AWS App Runner for the closest Cloud Run experience with full application support (Dashboard + API).
