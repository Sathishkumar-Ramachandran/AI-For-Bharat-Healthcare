"""FHIR-based healthcare data simulation service."""
from datetime import datetime
from typing import Dict, Any, List


class FHIRService:
    """Service for handling FHIR-compliant healthcare data structures."""
    
    @staticmethod
    def create_patient_resource(patient_id: str, name: str, age: int, gender: str = "unknown") -> Dict[str, Any]:
        """Create a FHIR Patient resource."""
        return {
            "resourceType": "Patient",
            "id": patient_id,
            "name": [{"use": "official", "text": name}],
            "gender": gender,
            "birthDate": str(datetime.now().year - age) + "-01-01"
        }
    
    @staticmethod
    def create_observation_resource(patient_id: str, symptoms: List[str]) -> Dict[str, Any]:
        """Create a FHIR Observation resource for symptoms."""
        return {
            "resourceType": "Observation",
            "status": "final",
            "subject": {"reference": f"Patient/{patient_id}"},
            "effectiveDateTime": datetime.now().isoformat(),
            "valueString": ", ".join(symptoms)
        }


fhir_service = FHIRService()
