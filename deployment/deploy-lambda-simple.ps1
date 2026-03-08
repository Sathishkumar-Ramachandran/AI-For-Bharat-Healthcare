# Simple Lambda deployment for Healthcare System

Write-Host "Deploying Lambda backend..." -ForegroundColor Cyan

$REGION = "us-east-1"
$FUNCTION_NAME = "healthcare-backend"

# Step 1: Create deployment package
Write-Host "Creating deployment package..." -ForegroundColor Yellow

if (Test-Path "lambda-package.zip") { Remove-Item "lambda-package.zip" }
$tempDir = "lambda-temp"
if (Test-Path $tempDir) { Remove-Item -Recurse -Force $tempDir }
New-Item -ItemType Directory -Path $tempDir | Out-Null

Copy-Item -Path "deployment/lambda_functions.py" -Destination "$tempDir/lambda_function.py"
Copy-Item -Path "services" -Destination "$tempDir/services" -Recurse
Copy-Item -Path "agents" -Destination "$tempDir/agents" -Recurse

Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install boto3 -t $tempDir --quiet

Compress-Archive -Path "$tempDir/*" -DestinationPath "lambda-package.zip"
Remove-Item -Recurse -Force $tempDir

Write-Host "✓ Package created" -ForegroundColor Green

# Step 2: Get account ID
$accountId = aws sts get-caller-identity --query Account --output text
Write-Host "✓ Account ID: $accountId" -ForegroundColor Green

# Step 3: Create/Update Lambda
Write-Host "Deploying Lambda function..." -ForegroundColor Yellow

$roleArn = "arn:aws:iam::${accountId}:role/healthcare-lambda-role"

aws lambda create-function --function-name $FUNCTION_NAME --runtime python3.11 --role $roleArn --handler lambda_function.lambda_handler --zip-file fileb://lambda-package.zip --timeout 30 --memory-size 512 --region $REGION 2>$null

if ($LASTEXITCODE -ne 0) {
    Write-Host "Updating existing function..." -ForegroundColor Yellow
    aws lambda update-function-code --function-name $FUNCTION_NAME --zip-file fileb://lambda-package.zip --region $REGION
}

Write-Host "✓ Lambda deployed" -ForegroundColor Green

# Step 4: Create Function URL
Write-Host "Creating Function URL..." -ForegroundColor Yellow

$functionUrl = aws lambda create-function-url-config --function-name $FUNCTION_NAME --auth-type NONE --cors "AllowOrigins=*,AllowMethods=*,AllowHeaders=*" --region $REGION --query 'FunctionUrl' --output text 2>$null

if ([string]::IsNullOrEmpty($functionUrl)) {
    $functionUrl = aws lambda get-function-url-config --function-name $FUNCTION_NAME --region $REGION --query 'FunctionUrl' --output text
}

# Add permission for public access
aws lambda add-permission --function-name $FUNCTION_NAME --statement-id FunctionURLAllowPublicAccess --action lambda:InvokeFunctionUrl --principal "*" --function-url-auth-type NONE --region $REGION 2>$null

Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host "Lambda Deployed Successfully!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Function URL: $functionUrl" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next: Update dashboard.html with this URL" -ForegroundColor Yellow
Write-Host ""

# Cleanup
Remove-Item "lambda-package.zip" -ErrorAction SilentlyContinue
