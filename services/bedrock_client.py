"""Amazon Bedrock client for Nova model integration."""
import json
import boto3
from typing import Optional
from config.settings import AWS_REGION, NOVA_MODEL_ID, MAX_TOKENS, TEMPERATURE


class BedrockClient:
    """Client for interacting with Amazon Nova via Bedrock."""
    
    def __init__(self):
        """Initialize Bedrock runtime client."""
        try:
            self.client = boto3.client(
                service_name='bedrock-runtime',
                region_name=AWS_REGION
            )
            self.model_id = NOVA_MODEL_ID
        except Exception as e:
            print(f"Warning: Could not initialize Bedrock client: {e}")
            self.client = None
    
    def invoke_nova(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        max_tokens: int = MAX_TOKENS,
        temperature: float = TEMPERATURE
    ) -> str:
        """Invoke Amazon Nova model with a prompt."""
        if not self.client:
            print("⚠️  Using fallback mode - No AWS credentials")
            return self._fallback_response(prompt)
            
        try:
            messages = []
            
            if system_prompt:
                messages.append({
                    "role": "user",
                    "content": [{"text": system_prompt + "\n\n" + prompt}]
                })
            else:
                messages.append({
                    "role": "user",
                    "content": [{"text": prompt}]
                })
            
            request_body = {
                "messages": messages,
                "inferenceConfig": {
                    "maxTokens": max_tokens,
                    "temperature": temperature
                }
            }
            
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body)
            )
            
            response_body = json.loads(response['body'].read())
            result = response_body['output']['message']['content'][0]['text']
            print(f"✓ Amazon Nova LLM response received ({len(result)} chars)")
            return result
            
        except Exception as e:
            print(f"❌ Error invoking Bedrock Nova: {str(e)}")
            print("⚠️  Falling back to simulated response")
            return self._fallback_response(prompt)
    
    def _fallback_response(self, prompt: str) -> str:
        """Fallback response when Bedrock is unavailable."""
        return f"[Simulated Response] Processed: {prompt[:100]}..."


bedrock_client = BedrockClient()
