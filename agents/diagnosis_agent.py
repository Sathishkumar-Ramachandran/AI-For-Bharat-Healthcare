"""Diagnosis Agent for medical diagnosis prediction."""
from services.bedrock_client import bedrock_client
from typing import Dict, Any, List


class DiagnosisAgent:
    """Agent responsible for analyzing symptoms and predicting diagnosis."""
    
    def __init__(self):
        """Initialize the Diagnosis Agent."""
        self.role = "Medical Diagnostician"
    
    def analyze_symptoms(self, symptoms: List[str], patient_history: str = "") -> Dict[str, Any]:
        """
        Analyze symptoms and predict probable diagnosis.
        
        Args:
            symptoms: List of patient symptoms
            patient_history: Optional patient medical history
            
        Returns:
            Diagnosis prediction with confidence and recommendations
        """
        symptoms_text = ', '.join(symptoms)
        
        prompt = f"""As a medical diagnostician, analyze these symptoms and provide a diagnosis:

Symptoms: {symptoms_text}
{f'Patient History: {patient_history}' if patient_history else ''}

Provide:
1. Most probable diagnosis
2. Differential diagnoses (2-3 alternatives)
3. Confidence level (High/Medium/Low)
4. Reasoning for the diagnosis
5. Red flags or warning signs to watch for

Be thorough but concise."""
        
        llm_response = bedrock_client.invoke_nova(
            prompt=prompt,
            system_prompt="You are an experienced medical diagnostician. Provide evidence-based diagnostic reasoning."
        )
        
        # Extract structured information
        diagnosis_data = self._parse_diagnosis(llm_response, symptoms)
        
        return {
            "primary_diagnosis": diagnosis_data['primary'],
            "differential_diagnoses": diagnosis_data['differential'],
            "confidence": diagnosis_data['confidence'],
            "reasoning": llm_response,
            "symptoms_analyzed": symptoms,
            "red_flags": diagnosis_data['red_flags'],
            "status": "completed"
        }
    
    def _parse_diagnosis(self, llm_response: str, symptoms: List[str]) -> Dict[str, Any]:
        """Parse LLM response to extract structured diagnosis data."""
        # Simplified parsing - in production use more sophisticated NLP
        response_lower = llm_response.lower()
        
        # Determine confidence
        if 'high confidence' in response_lower or 'highly likely' in response_lower:
            confidence = 'High'
        elif 'low confidence' in response_lower or 'uncertain' in response_lower:
            confidence = 'Low'
        else:
            confidence = 'Medium'
        
        # Extract primary diagnosis (simplified)
        primary = "Pending detailed analysis"
        if 'viral infection' in response_lower or 'virus' in response_lower:
            primary = "Viral Infection"
        elif 'bacterial infection' in response_lower or 'bacteria' in response_lower:
            primary = "Bacterial Infection"
        elif 'respiratory' in response_lower:
            primary = "Respiratory Condition"
        
        return {
            "primary": primary,
            "differential": ["Alternative diagnosis 1", "Alternative diagnosis 2"],
            "confidence": confidence,
            "red_flags": ["Severe symptoms", "Persistent fever"]
        }


diagnosis_agent = DiagnosisAgent()
