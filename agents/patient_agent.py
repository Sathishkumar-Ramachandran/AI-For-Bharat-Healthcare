"""Patient Intake Agent for collecting patient information."""
from services.bedrock_client import bedrock_client
from services.mcp_server import mcp_server
from services.fhir_service import fhir_service
from typing import Dict, Any


class PatientIntakeAgent:
    """Agent responsible for patient intake and registration."""
    
    def __init__(self):
        """Initialize the Patient Intake Agent."""
        self.role = "Patient Intake Specialist"
        self.goal = "Collect comprehensive patient information and create structured intake records"
    
    def collect_patient_info(self, name: str, age: int, symptoms: str, insurance: str) -> Dict[str, Any]:
        """Collect and structure patient intake information."""
        existing_patients = mcp_server.get_patient_data()
        patient_id = f"P{len(existing_patients) + 1:03d}"
        
        symptom_list = [s.strip() for s in symptoms.split(',')]
        
        fhir_patient = fhir_service.create_patient_resource(patient_id, name, age)
        fhir_observation = fhir_service.create_observation_resource(patient_id, symptom_list)
        
        intake_record = {
            "patient_id": patient_id,
            "name": name,
            "age": age,
            "symptoms": symptom_list,
            "insurance": insurance,
            "fhir_patient": fhir_patient,
            "fhir_observation": fhir_observation,
            "status": "registered"
        }
        
        prompt = f"Create a brief patient intake summary for {name}, age {age}, with symptoms: {', '.join(symptom_list)}"
        intake_record["intake_summary"] = bedrock_client.invoke_nova(prompt, "You are a medical intake specialist.")
        
        return intake_record


patient_intake_agent = PatientIntakeAgent()
