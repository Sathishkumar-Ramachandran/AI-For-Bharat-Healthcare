"""Task orchestration for Patient Data Tracking."""
from typing import Dict, Any, List, Optional


class PatientTrackingOrchestrator:
    """Orchestrate patient data tracking tasks."""
    
    def __init__(self):
        """Initialize patient tracking orchestrator."""
        self.tracking_areas = [
            "medical_history",
            "test_results",
            "prescriptions",
            "navigation_guidance"
        ]
    
    def get_patient_history(self, patient_id: str) -> Dict[str, Any]:
        """
        Get complete patient medical history.
        
        Args:
            patient_id: Patient identifier
            
        Returns:
            Complete patient history with all visits
        """
        from services.mcp_server import mcp_server
        from agents.navigation_agent import navigation_agent
        
        # Get patient records
        records = mcp_server.get_patient_records(patient_id)
        
        if not records:
            return {
                'patient_id': patient_id,
                'records_found': 0,
                'message': 'No records found for this patient',
                'status': 'not_found'
            }
        
        # Format records
        formatted_records = []
        for record in records:
            formatted_records.append({
                'visit_date': record.get('visit_timestamp'),
                'reason': record.get('visit_reason'),
                'diagnosis': record.get('diagnosis'),
                'tests': record.get('tests_taken'),
                'medicines': record.get('medicines_prescribed'),
                'notes': record.get('doctor_notes'),
                'navigation': record.get('navigation_instructions')
            })
        
        return {
            'patient_id': patient_id,
            'records_found': len(records),
            'records': formatted_records,
            'status': 'success'
        }
    
    def get_navigation_for_patient(
        self,
        tests: Optional[List[str]] = None,
        pharmacy_needed: bool = False
    ) -> Dict[str, Any]:
        """
        Get navigation instructions for patient.
        
        Args:
            tests: List of tests patient needs
            pharmacy_needed: Whether pharmacy visit is needed
            
        Returns:
            Navigation instructions
        """
        from agents.navigation_agent import navigation_agent
        
        navigation_result = navigation_agent.get_navigation_instructions(
            tests=tests,
            pharmacy_needed=pharmacy_needed
        )
        
        return navigation_result
    
    def get_patient_mobile_view(self, patient_id: str) -> Dict[str, Any]:
        """
        Get patient data formatted for mobile app view.
        
        Args:
            patient_id: Patient identifier
            
        Returns:
            Mobile-formatted patient data
        """
        history = self.get_patient_history(patient_id)
        
        if history['status'] == 'not_found':
            return history
        
        # Get latest record
        latest_record = history['records'][0] if history['records'] else None
        
        # Extract navigation if available
        navigation = None
        if latest_record and latest_record.get('navigation'):
            navigation = latest_record['navigation']
        
        return {
            'patient_id': patient_id,
            'latest_visit': latest_record,
            'total_visits': history['records_found'],
            'navigation_instructions': navigation,
            'all_records': history['records'],
            'status': 'success'
        }


patient_tracking_orchestrator = PatientTrackingOrchestrator()
