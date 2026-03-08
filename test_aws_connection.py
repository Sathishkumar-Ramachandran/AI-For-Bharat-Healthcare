"""Test AWS Bedrock connection and credentials."""
import boto3
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def test_aws_credentials():
    """Test if AWS credentials are configured."""
    print("\n" + "="*60)
    print("AWS BEDROCK CONNECTION TEST")
    print("="*60 + "\n")
    
    # Check if credentials are set
    access_key = os.getenv('AWS_ACCESS_KEY_ID')
    secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    region = os.getenv('AWS_REGION', 'us-east-1')
    
    print("Step 1: Checking credentials...")
    if not access_key or access_key == 'your_access_key_here':
        print("❌ AWS_ACCESS_KEY_ID not configured")
        print("   Please edit the .env file with your AWS credentials")
        return False
    
    if not secret_key or secret_key == 'your_secret_key_here':
        print("❌ AWS_SECRET_ACCESS_KEY not configured")
        print("   Please edit the .env file with your AWS credentials")
        return False
    
    print(f"✓ AWS_ACCESS_KEY_ID: {access_key[:8]}...")
    print(f"✓ AWS_SECRET_ACCESS_KEY: {secret_key[:8]}...")
    print(f"✓ AWS_REGION: {region}")
    
    # Test connection
    print("\nStep 2: Testing Bedrock connection...")
    try:
        client = boto3.client(
            service_name='bedrock-runtime',
            region_name=region
        )
        print("✓ Successfully connected to AWS Bedrock")
    except Exception as e:
        print(f"❌ Failed to connect to AWS Bedrock: {e}")
        return False
    
    # Test model invocation
    print("\nStep 3: Testing Amazon Nova model...")
    try:
        request_body = {
            "messages": [
                {
                    "role": "user",
                    "content": [{"text": "Say 'Hello from Amazon Nova!' if you can read this."}]
                }
            ],
            "inferenceConfig": {
                "maxTokens": 100,
                "temperature": 0.7
            }
        }
        
        response = client.invoke_model(
            modelId="us.amazon.nova-pro-v1:0",
            body=json.dumps(request_body)
        )
        
        response_body = json.loads(response['body'].read())
        llm_response = response_body['output']['message']['content'][0]['text']
        
        print("✓ Successfully invoked Amazon Nova model")
        print(f"\nLLM Response: {llm_response}")
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        print("\nYour AWS Bedrock is configured correctly!")
        print("The application will now use real LLM responses.")
        print("\nRestart the web server to apply changes:")
        print("  python -m uvicorn api.main_api:app --host 0.0.0.0 --port 8000")
        return True
        
    except Exception as e:
        print(f"❌ Failed to invoke model: {e}")
        print("\nPossible issues:")
        print("  1. Model access not enabled - Go to AWS Bedrock console")
        print("  2. Insufficient permissions - Check IAM policy")
        print("  3. Wrong region - Try us-east-1")
        print("  4. Model not available in your region")
        return False


if __name__ == "__main__":
    success = test_aws_credentials()
    
    if not success:
        print("\n" + "="*60)
        print("SETUP INSTRUCTIONS")
        print("="*60)
        print("\n1. Edit the .env file in the project root")
        print("2. Replace 'your_access_key_here' with your AWS Access Key ID")
        print("3. Replace 'your_secret_key_here' with your AWS Secret Access Key")
        print("4. Save the file and run this test again")
        print("\nFor detailed instructions, see: AWS_SETUP_GUIDE.md")
