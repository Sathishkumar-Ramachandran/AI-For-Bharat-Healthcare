# AWS Bedrock Setup Guide

## Step 1: Get AWS Credentials

### Option A: If you already have an AWS account

1. **Log in to AWS Console**: https://console.aws.amazon.com
2. **Go to IAM (Identity and Access Management)**
3. **Create a new user or use existing user**
4. **Create Access Keys:**
   - Click on your user
   - Go to "Security credentials" tab
   - Click "Create access key"
   - Choose "Application running outside AWS"
   - Download the credentials (you'll get Access Key ID and Secret Access Key)

### Option B: If you don't have an AWS account

1. **Sign up for AWS**: https://aws.amazon.com
2. **Complete the registration** (requires credit card)
3. **Follow Option A above** to create access keys

## Step 2: Enable Amazon Bedrock

1. **Go to Amazon Bedrock Console**: https://console.aws.amazon.com/bedrock
2. **Select your region** (us-east-1 recommended)
3. **Request Model Access:**
   - Click "Model access" in the left sidebar
   - Click "Manage model access"
   - Find "Amazon Nova Pro" and enable it
   - Submit the request (usually instant approval)

## Step 3: Configure Your Application

### Method 1: Edit .env file (Recommended)

Open the `.env` file in your project and replace the placeholder values:

```env
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_REGION=us-east-1
```

### Method 2: Set Environment Variables

**Windows (PowerShell):**
```powershell
$env:AWS_ACCESS_KEY_ID="your_access_key"
$env:AWS_SECRET_ACCESS_KEY="your_secret_key"
$env:AWS_REGION="us-east-1"
```

**Windows (Command Prompt):**
```cmd
set AWS_ACCESS_KEY_ID=your_access_key
set AWS_SECRET_ACCESS_KEY=your_secret_key
set AWS_REGION=us-east-1
```

**Mac/Linux:**
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_REGION=us-east-1
```

## Step 4: Verify Configuration

Run this test script to verify your AWS credentials:

```bash
python -c "import boto3; client = boto3.client('bedrock-runtime', region_name='us-east-1'); print('✓ AWS credentials configured correctly!')"
```

## Step 5: Restart the Application

After configuring credentials, restart the web server:

```bash
# Stop the current server (Ctrl+C)
# Then restart:
python -m uvicorn api.main_api:app --host 0.0.0.0 --port 8000
```

## Troubleshooting

### Error: "Unable to locate credentials"
- Make sure you've set the credentials correctly
- Check that .env file is in the project root directory
- Verify no typos in the credentials

### Error: "Access Denied"
- Ensure your IAM user has Bedrock permissions
- Add this policy to your IAM user:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": "*"
        }
    ]
}
```

### Error: "Model not found"
- Make sure you've requested access to Amazon Nova Pro
- Check that you're using the correct region (us-east-1)
- Wait a few minutes after requesting model access

## Cost Information

**Amazon Nova Pro Pricing (as of 2024):**
- Input: ~$0.80 per 1M tokens
- Output: ~$3.20 per 1M tokens

**Estimated costs for this application:**
- Each workflow execution: ~$0.01-0.05
- 100 patient workflows: ~$1-5

**Free Tier:**
- AWS Free Tier includes some Bedrock usage
- Check current free tier limits: https://aws.amazon.com/bedrock/pricing/

## Security Best Practices

1. **Never commit credentials to Git**
   - The .env file is already in .gitignore
   - Never share your access keys publicly

2. **Use IAM roles in production**
   - For production deployments, use IAM roles instead of access keys
   - Rotate access keys regularly

3. **Limit permissions**
   - Only grant Bedrock permissions, not full AWS access
   - Use least-privilege principle

## Alternative: Use AWS CLI Configuration

If you have AWS CLI installed:

```bash
aws configure
```

This will store credentials in `~/.aws/credentials` and the application will automatically use them.

## Need Help?

- AWS Bedrock Documentation: https://docs.aws.amazon.com/bedrock/
- AWS Support: https://console.aws.amazon.com/support/
- Check the application logs for specific error messages

---

**Once configured, your application will use real Amazon Nova LLM responses for:**
- Patient intake summaries
- Clinical note generation
- Insurance authorization decisions
- Staffing recommendations
- Inventory procurement advice
- Security assessments
