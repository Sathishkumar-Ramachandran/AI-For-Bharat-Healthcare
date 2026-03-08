"""
AWS Lambda Handler for Healthcare Agentic System API
For pure serverless deployment with Lambda + API Gateway
"""
import json
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from agents.diagnosis_agent import diagnosis_agent
from agents.test_recommendation_agent import test_recommendation_agent
from agents.prescription_agent import prescription_agent
from agents.pharmacy_agent import pharmacy_agent
from agents.navigation_agent import navigation_agent
from services.mcp_server import mcp_server


def lambda_handler(event, context):
    """
    AWS Lambda handler for API requests.
    
    Supports:
    - GET /health - Health check
    - POST /diagnose - Diagnosis
    - POST /tests - Test recommendations
    - POST /prescription - Prescription generation
    - GET /pharmacy - Pharmacy status
    """
    
    # Parse request
    http_method = event.get('httpMethod', 'GET')
    path = event.get('path', '/')
    body = event.get('body', '{}')
    
    try:
        body_data = json.loads(body) if body else {}
    except:
        body_data = {}
    
    # CORS headers
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    
    # Handle OPTIONS for CORS
    if http_method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }
    
    # Route requests
    try:
        if path == '/health' or path == '/':
            response = {
                'status': 'healthy',
                'service': 'Healthcare Agentic System',
                'version': '2.0.0'
            }
            status_code = 200
            
        elif path == '/diagnose' and http_method == 'POST':
            symptoms = body_data.get('symptoms', [])
            result = diagnosis_agent.analyze_symptoms(symptoms)
            response = result
            status_code = 200
            
        elif path == '/tests' and http_method == 'POST':
            symptoms = body_data.get('symptoms', [])
            diagnosis = body_data.get('diagnosis', 'Unknown')
            result = test_recommendation_agent.recommend_tests(symptoms, diagnosis)
            response = result
            status_code = 200
            
        elif path == '/prescription' and http_method == 'POST':
            diagnosis = body_data.get('diagnosis', 'Unknown')
            symptoms = body_data.get('symptoms', [])
            age = body_data.get('age', 35)
            result = prescription_agent.generate_prescription(diagnosis, symptoms, age)
            response = result
            status_code = 200
            
        elif path == '/pharmacy' and http_method == 'GET':
            result = pharmacy_agent.get_pharmacy_status()
            response = result
            status_code = 200
            
        elif path == '/navigation' and http_method == 'POST':
            tests = body_data.get('tests', [])
            pharmacy_needed = body_data.get('pharmacy_needed', False)
            result = navigation_agent.get_navigation_instructions(tests, pharmacy_needed)
            response = result
            status_code = 200
            
        elif path == '/workflow' and http_method == 'POST':
            # Complete workflow
            symptoms = body_data.get('symptoms', [])
            age = body_data.get('age', 35)
            
            # Diagnose
            diagnosis_result = diagnosis_agent.analyze_symptoms(symptoms)
            
            # Tests
            test_result = test_recommendation_agent.recommend_tests(
                symptoms, 
                diagnosis_result['primary_diagnosis']
            )
            
            # Prescription
            prescription_result = prescription_agent.generate_prescription(
                diagnosis_result['primary_diagnosis'],
                symptoms,
                age
            )
            
            # Navigation
            test_names = [t['test_name'] for t in test_result['recommended_tests']]
            nav_result = navigation_agent.get_navigation_instructions(test_names, True)
            
            response = {
                'diagnosis': diagnosis_result,
                'tests': test_result,
                'prescription': prescription_result,
                'navigation': nav_result,
                'status': 'completed'
            }
            status_code = 200
            
        else:
            response = {
                'error': 'Not Found',
                'message': f'Path {path} not found'
            }
            status_code = 404
            
    except Exception as e:
        response = {
            'error': 'Internal Server Error',
            'message': str(e)
        }
        status_code = 500
    
    return {
        'statusCode': status_code,
        'headers': headers,
        'body': json.dumps(response)
    }


# For local testing
if __name__ == '__main__':
    # Test event
    test_event = {
        'httpMethod': 'POST',
        'path': '/diagnose',
        'body': json.dumps({
            'symptoms': ['fever', 'cough', 'fatigue']
        })
    }
    
    result = lambda_handler(test_event, None)
    print(json.dumps(json.loads(result['body']), indent=2))
