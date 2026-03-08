"""Test Recommendation Agent for medical test suggestions."""
from services.bedrock_client import bedrock_client
from typing import Dict, Any, List


class TestRecommendationAgent:
    """Agent responsible for recommending medical tests."""
    
    def __init__(self):
        """Initialize the Test Recommendation Agent."""
        self.role = "Medical Test Coordinator"
    
    def recommend_tests(self, symptoms: List[str], diagnosis: str) -> Dict[str, Any]:
        """
        Recommend medical tests based on symptoms and diagnosis.
        
        Args:
            symptoms: List of patient symptoms
            diagnosis: Probable diagnosis
            
        Returns:
            Recommended tests with priority and location
        """
        symptoms_text = ', '.join(symptoms)
        
        prompt = f"""As a medical test coordinator, recommend appropriate diagnostic tests for:

Symptoms: {symptoms_text}
Probable Diagnosis: {diagnosis}

Provide a list of recommended tests with:
1. Test name
2. Priority (Urgent/Routine)
3. Purpose/Reason
4. Department/Location

Be specific and practical."""
        
        llm_response = bedrock_client.invoke_nova(
            prompt=prompt,
            system_prompt="You are a medical test coordinator. Recommend evidence-based diagnostic tests."
        )
        
        # Parse and structure test recommendations
        tests = self._parse_test_recommendations(llm_response, symptoms, diagnosis)
        
        return {
            "recommended_tests": tests,
            "total_tests": len(tests),
            "llm_analysis": llm_response,
            "status": "completed"
        }
    
    def _parse_test_recommendations(self, llm_response: str, symptoms: List[str], diagnosis: str) -> List[Dict[str, Any]]:
        """Parse LLM response to extract structured test data."""
        tests = []
        response_lower = llm_response.lower()
        
        # Common test mappings
        test_database = {
            'cbc': {'name': 'Complete Blood Count (CBC)', 'department': 'Laboratory', 'priority': 'Routine'},
            'blood culture': {'name': 'Blood Culture', 'department': 'Laboratory', 'priority': 'Urgent'},
            'x-ray': {'name': 'Chest X-Ray', 'department': 'Radiology', 'priority': 'Routine'},
            'ct scan': {'name': 'CT Scan', 'department': 'Radiology', 'priority': 'Urgent'},
            'urine': {'name': 'Urine Analysis', 'department': 'Laboratory', 'priority': 'Routine'},
            'ecg': {'name': 'ECG', 'department': 'Cardiology', 'priority': 'Urgent'},
        }
        
        # Check which tests are mentioned
        for test_key, test_info in test_database.items():
            if test_key in response_lower:
                tests.append({
                    "test_name": test_info['name'],
                    "department": test_info['department'],
                    "priority": test_info['priority'],
                    "reason": f"Based on {diagnosis}"
                })
        
        # If no tests found, add default based on symptoms
        if not tests:
            if any(s in ['fever', 'infection'] for s in symptoms):
                tests.append({
                    "test_name": "Complete Blood Count (CBC)",
                    "department": "Laboratory",
                    "priority": "Routine",
                    "reason": "Standard test for infection"
                })
        
        return tests


test_recommendation_agent = TestRecommendationAgent()
