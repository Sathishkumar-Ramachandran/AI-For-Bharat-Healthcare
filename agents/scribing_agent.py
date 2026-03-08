"""Clinical Scribing Agent for generating clinical documentation."""
from services.bedrock_client import bedrock_client
from typing import Dict, Any
import json


class ClinicalScribingAgent:
    """Agent responsible for converting consultations into clinical notes."""
    
    def __init__(self):
        """Initialize the Clinical Scribing Agent."""
        self.role = "Clinical Documentation Specialist"
    
    def generate_clinical_notes(self, patient_name: str, transcript: str, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate structured clinical notes from consultation transcript."""
        prompt = f"""Convert this consultation into clinical notes:
Patient: {patient_name}, Age: {patient_data.get('age')}
Symptoms: {', '.join(patient_data.get('symptoms', []))}
Transcript: {transcript}

Provide: diagnosis, treatment_plan, prescription"""
        
        response = bedrock_client.invoke_nova(prompt, "You are a medical scribe.")
        
        clinical_notes = {
            "patient_name": patient_name,
            "patient_id": patient_data.get("patient_id"),
            "chief_complaint": ', '.join(patient_data.get('symptoms', [])),
            "diagnosis": "Clinical assessment based on symptoms",
            "treatment_plan": "Standard care protocol",
            "prescription": "As per clinical guidelines",
            "notes": response,
            "status": "completed"
        }
        
        return clinical_notes


clinical_scribing_agent = ClinicalScribingAgent()
