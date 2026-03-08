"""Prescription Agent for generating medicine prescriptions."""
from services.bedrock_client import bedrock_client
from agents.pharmacy_agent import pharmacy_agent
from typing import Dict, Any, List


class PrescriptionAgent:
    """Agent responsible for generating prescriptions."""
    
    def __init__(self):
        """Initialize the Prescription Agent."""
        self.role = "Prescribing Physician"
    
    def generate_prescription(self, diagnosis: str, symptoms: List[str], patient_age: int = None) -> Dict[str, Any]:
        """
        Generate prescription based on diagnosis and symptoms.
        
        Args:
            diagnosis: Patient diagnosis
            symptoms: List of symptoms
            patient_age: Patient age (optional)
            
        Returns:
            Prescription with medicines, dosage, and instructions
        """
        symptoms_text = ', '.join(symptoms)
        age_info = f"Patient Age: {patient_age}" if patient_age else ""
        
        prompt = f"""As a prescribing physician, create a prescription for:

Diagnosis: {diagnosis}
Symptoms: {symptoms_text}
{age_info}

Provide a complete prescription with:
1. Medicine name
2. Dosage (e.g., 500mg)
3. Frequency (e.g., twice daily)
4. Duration (e.g., 7 days)
5. Special instructions
6. Precautions

Be specific and safe."""
        
        llm_response = bedrock_client.invoke_nova(
            prompt=prompt,
            system_prompt="You are a licensed physician. Prescribe safe, evidence-based medications."
        )
        
        # Check pharmacy availability
        pharmacy_status = pharmacy_agent.recommend_medicines(diagnosis, symptoms)
        
        # Parse prescription
        prescription_items = self._parse_prescription(llm_response)
        
        # Add availability info
        for item in prescription_items:
            availability = pharmacy_agent.check_medicine_availability(item['medicine'])
            item['availability'] = availability['stock_status']
            item['substitute'] = availability.get('substitute_available', 'N/A')
        
        return {
            "prescription_items": prescription_items,
            "total_medicines": len(prescription_items),
            "llm_prescription": llm_response,
            "pharmacy_check": pharmacy_status,
            "status": "completed"
        }
    
    def _parse_prescription(self, llm_response: str) -> List[Dict[str, Any]]:
        """Parse LLM response to extract prescription items."""
        items = []
        
        # Common medicine patterns
        common_prescriptions = {
            'paracetamol': {'dosage': '500mg', 'frequency': 'Twice daily', 'duration': '5 days'},
            'ibuprofen': {'dosage': '400mg', 'frequency': 'Three times daily', 'duration': '3 days'},
            'amoxicillin': {'dosage': '500mg', 'frequency': 'Three times daily', 'duration': '7 days'},
            'azithromycin': {'dosage': '500mg', 'frequency': 'Once daily', 'duration': '3 days'},
        }
        
        response_lower = llm_response.lower()
        
        for medicine, details in common_prescriptions.items():
            if medicine in response_lower:
                items.append({
                    "medicine": medicine.capitalize(),
                    "dosage": details['dosage'],
                    "frequency": details['frequency'],
                    "duration": details['duration'],
                    "instructions": "Take after meals"
                })
        
        return items if items else [{
            "medicine": "Paracetamol",
            "dosage": "500mg",
            "frequency": "Twice daily",
            "duration": "5 days",
            "instructions": "Take after meals"
        }]


prescription_agent = PrescriptionAgent()
