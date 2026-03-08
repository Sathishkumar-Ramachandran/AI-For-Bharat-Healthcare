"""Workflow Orchestrator Agent for coordinating all healthcare agents."""
from typing import Dict, Any
from agents.patient_agent import patient_intake_agent
from agents.scribing_agent import clinical_scribing_agent
from agents.insurance_agent import insurance_authorization_agent
from agents.staffing_agent import staffing_prediction_agent
from agents.inventory_agent import supply_chain_agent
from agents.security_agent import cybersecurity_monitoring_agent


class WorkflowOrchestratorAgent:
    """Orchestrator agent that coordinates the entire healthcare workflow."""
    
    def __init__(self):
        """Initialize the Workflow Orchestrator Agent."""
        self.role = "Healthcare Workflow Coordinator"
    
    def execute_patient_workflow(self, patient_name: str, age: int, symptoms: str, insurance: str, consultation_transcript: str = None) -> Dict[str, Any]:
        """Execute complete patient workflow from intake to billing."""
        workflow_results = {"workflow_status": "in_progress", "steps_completed": []}
        
        print("\n" + "="*80)
        print("HEALTHCARE WORKFLOW AUTOMATION - STARTING")
        print("="*80 + "\n")
        
        # Step 1: Patient Intake
        print("STEP 1: Patient Intake")
        print("-" * 40)
        try:
            intake_result = patient_intake_agent.collect_patient_info(name=patient_name, age=age, symptoms=symptoms, insurance=insurance)
            workflow_results["patient_intake"] = intake_result
            workflow_results["steps_completed"].append("patient_intake")
            print(f"✓ Patient registered: {intake_result['patient_id']}")
        except Exception as e:
            workflow_results["patient_intake"] = {"error": str(e)}
            print(f"✗ Error: {e}")
        
        # Step 2: Clinical Documentation
        print("\nSTEP 2: Clinical Documentation")
        print("-" * 40)
        try:
            if not consultation_transcript:
                consultation_transcript = f"Doctor: What symptoms? Patient: {symptoms}"
            
            clinical_notes = clinical_scribing_agent.generate_clinical_notes(patient_name, consultation_transcript, intake_result)
            workflow_results["clinical_notes"] = clinical_notes
            workflow_results["steps_completed"].append("clinical_documentation")
            print(f"✓ Clinical notes generated")
        except Exception as e:
            workflow_results["clinical_notes"] = {"error": str(e)}
            print(f"✗ Error: {e}")
        
        # Step 3: Insurance Authorization
        print("\nSTEP 3: Insurance Authorization")
        print("-" * 40)
        try:
            auth_result = insurance_authorization_agent.check_authorization(intake_result, clinical_notes, ["consultation"])
            workflow_results["insurance_authorization"] = auth_result
            workflow_results["steps_completed"].append("insurance_authorization")
            print(f"✓ Authorization: {auth_result['status'].upper()}")
        except Exception as e:
            workflow_results["insurance_authorization"] = {"error": str(e)}
            print(f"✗ Error: {e}")
        
        # Step 4: Staffing Prediction
        print("\nSTEP 4: Staffing Prediction")
        print("-" * 40)
        try:
            staffing_result = staffing_prediction_agent.predict_staffing_needs(50)
            workflow_results["staffing_prediction"] = staffing_result
            workflow_results["steps_completed"].append("staffing_prediction")
            print(f"✓ Predicted nurses: {staffing_result['predicted_nurse_count']}")
        except Exception as e:
            workflow_results["staffing_prediction"] = {"error": str(e)}
            print(f"✗ Error: {e}")
        
        # Step 5: Inventory Check
        print("\nSTEP 5: Inventory Check")
        print("-" * 40)
        try:
            inventory_result = supply_chain_agent.check_inventory_status()
            workflow_results["inventory_status"] = inventory_result
            workflow_results["steps_completed"].append("inventory_check")
            print(f"✓ Status: {inventory_result['status'].upper()}")
        except Exception as e:
            workflow_results["inventory_status"] = {"error": str(e)}
            print(f"✗ Error: {e}")
        
        # Step 6: Security Monitoring
        print("\nSTEP 6: Security Monitoring")
        print("-" * 40)
        try:
            security_result = cybersecurity_monitoring_agent.monitor_system_activity()
            workflow_results["security_monitoring"] = security_result
            workflow_results["steps_completed"].append("security_monitoring")
            print(f"✓ Security Score: {security_result['security_score']}/100")
        except Exception as e:
            workflow_results["security_monitoring"] = {"error": str(e)}
            print(f"✗ Error: {e}")
        
        workflow_results["workflow_status"] = "completed"
        workflow_results["total_steps"] = len(workflow_results["steps_completed"])
        
        print("\n" + "="*80)
        print(f"WORKFLOW COMPLETED - {workflow_results['total_steps']} steps")
        print("="*80 + "\n")
        
        return workflow_results


workflow_orchestrator = WorkflowOrchestratorAgent()
