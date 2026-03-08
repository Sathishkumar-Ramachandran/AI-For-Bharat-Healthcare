"""
AWS Lambda functions for Healthcare Agentic System
Deploy these as separate Lambda functions behind API Gateway
"""

import json
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, '/var/task')

from services.bedrock_client import BedrockClient
from services.mcp_server import MCPServer

# Initialize services
bedrock = BedrockClient()
mcp = MCPServer()

def lambda_handler(event, context):
    """
    Main Lambda handler - routes to appropriate function
    """
    path = event.get('path', '')
    method = event.get('httpMethod', 'GET')
    
    # CORS headers
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
    }
    
    try:
        if method == 'OPTIONS':
            return {'statusCode': 200, 'headers': headers, 'body': ''}
        
        if path == '/treatment' and method == 'POST':
            return treatment_flow(event, headers)
        elif path == '/management' and method == 'GET':
            return hospital_management(event, headers)
        elif path.startswith('/patient/') and method == 'GET':
            return get_patient(event, headers)
        else:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'error': 'Not found'})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }

def treatment_flow(event, headers):
    """Handle treatment flow consultation"""
    body = json.loads(event.get('body', '{}'))
    
    patient_id = body.get('patient_id')
    patient_name = body.get('patient_name')
    symptoms = body.get('symptoms')
    
    # Run AI agents
    diagnosis_prompt = f"Patient {patient_name} presents with: {symptoms}. Provide diagnosis."
    diagnosis = bedrock.generate_text(diagnosis_prompt)
    
    tests_prompt = f"Based on diagnosis: {diagnosis}, recommend medical tests."
    tests = bedrock.generate_text(tests_prompt)
    
    prescription_prompt = f"Based on diagnosis: {diagnosis}, prescribe medications."
    prescription = bedrock.generate_text(prescription_prompt)
    
    navigation_prompt = f"Guide patient to appropriate department for: {diagnosis}"
    navigation = bedrock.generate_text(navigation_prompt)
    
    # Save to database
    mcp.save_consultation(
        patient_id=patient_id,
        patient_name=patient_name,
        symptoms=symptoms,
        diagnosis=diagnosis,
        tests=tests,
        medicines=prescription,
        navigation=navigation
    )
    
    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps({
            'diagnosis': diagnosis,
            'tests': tests,
            'prescription': prescription,
            'navigation': navigation
        })
    }

def hospital_management(event, headers):
    """Get hospital management metrics"""
    
    # Staffing prediction
    staffing_prompt = "Predict staffing needs for next week based on current trends."
    staffing = bedrock.generate_text(staffing_prompt)
    
    # Inventory check
    inventory_prompt = "Check medical supply inventory status."
    inventory = bedrock.generate_text(inventory_prompt)
    
    # Security status
    security_prompt = "Check for any security anomalies."
    security = bedrock.generate_text(security_prompt)
    
    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps({
            'staffing': staffing,
            'inventory': inventory,
            'security': security
        })
    }

def get_patient(event, headers):
    """Get patient record"""
    patient_id = event['path'].split('/')[-1]
    
    # Get from database
    record = mcp.get_patient_record(patient_id)
    
    if not record:
        return {
            'statusCode': 404,
            'headers': headers,
            'body': json.dumps({'error': 'Patient not found'})
        }
    
    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps(record)
    }
