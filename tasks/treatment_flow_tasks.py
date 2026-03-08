"""Task orchestration for Treatment Flow."""
from typing import Dict, Any, List


class TreatmentFlowOrchestrator:
    """Orchestrate treatment flow tasks across agents."""
    
    def __init__(self):
        """Initialize treatment flow orchestrator."""
        self.workflow_steps = [
            "transcribe_conversation",
            "extract_symptoms",
            "diagnose_condition",
            "recommend_tests",
            "generate_prescription",
            "check_pharmacy",
            "provide_navigation"
        ]
    
    def execute_treatment_flow(
        self,
        doctor_input: str,
        patient_input: str,
        patient_age: int = None
    ) -> Dict[str, Any]:
        """
        Execute complete treatment flow.
        
        Args:
            doctor_input: Doctor's voice/text input
            patient_input: Patient's voice/text input
            patient_age: Patient age
            
        Returns:
            Complete treatment flow results
        """
        from services.speech_to_text import speech_to_text_service
        from agents.scribing_agent import clinical_scribing_agent
        from agents.diagnosis_agent import diagnosis_agent
        from agents.test_recommendation_agent import test_recommendation_agent
        from agents.prescription_agent import prescription_agent
        from agents.pharmacy_agent import pharmacy_agent
        from agents.navigation_agent import navigation_agent
        from services.mcp_server import mcp_server
        
        results = {}
        
        # Step 1: Transcribe conversation
        transcript = speech_to_text_service.transcribe_conversation(
            doctor_audio=doctor_input,
            patient_audio=patient_input
        )
        results['transcript'] = transcript
        
        # Step 2: Extract symptoms
        scribing_result = clinical_scribing_agent.generate_clinical_notes(
            transcript['conversation']
        )
        results['clinical_notes'] = scribing_result
        symptoms = scribing_result['symptoms']
        
        # Step 3: Diagnose
        diagnosis_result = diagnosis_agent.analyze_symptoms(symptoms)
        results['diagnosis'] = diagnosis_result
        
        # Step 4: Recommend tests
        test_result = test_recommendation_agent.recommend_tests(
            symptoms,
            diagnosis_result['primary_diagnosis']
        )
        results['tests'] = test_result
        
        # Step 5: Generate prescription
        prescription_result = prescription_agent.generate_prescription(
            diagnosis_result['primary_diagnosis'],
            symptoms,
            patient_age
        )
        results['prescription'] = prescription_result
        
        # Step 6: Check pharmacy availability
        pharmacy_status = pharmacy_agent.get_pharmacy_status()
        results['pharmacy_status'] = pharmacy_status
        
        # Step 7: Provide navigation
        test_names = [t['test_name'] for t in test_result['recommended_tests']]
        navigation_result = navigation_agent.get_navigation_instructions(
            tests=test_names,
            pharmacy_needed=True
        )
        results['navigation'] = navigation_result
        
        # Save to database
        patient_id = f"P{hash(patient_input) % 10000:04d}"
        mcp_server.save_patient_intake({
            'patient_id': patient_id,
            'symptoms': ', '.join(symptoms),
            'diagnosis': diagnosis_result['primary_diagnosis'],
            'recommended_tests': ', '.join(test_names),
            'prescription': ', '.join([p['medicine'] for p in prescription_result['prescription_items']])
        })
        
        mcp_server.save_patient_record({
            'patient_id': patient_id,
            'visit_reason': ', '.join(symptoms),
            'diagnosis': diagnosis_result['primary_diagnosis'],
            'tests_taken': ', '.join(test_names),
            'medicines_prescribed': ', '.join([p['medicine'] for p in prescription_result['prescription_items']]),
            'doctor_notes': scribing_result['treatment_plan'],
            'navigation_instructions': '; '.join(navigation_result['step_by_step_directions'])
        })
        
        results['patient_id'] = patient_id
        results['status'] = 'completed'
        
        return results


treatment_flow_orchestrator = TreatmentFlowOrchestrator()
