"""Main entry point for the Healthcare Agentic Workflow Automation System."""
import sys
from agents.orchestrator_agent import workflow_orchestrator


def main():
    """Execute the healthcare workflow simulation."""
    print("""
    ╔════════════════════════════════════════════════════════════════════╗
    ║   AGENTIC HEALTHCARE WORKFLOW AUTOMATION SYSTEM                    ║
    ║   Powered by Amazon Nova + CrewAI + MCP                            ║
    ╚════════════════════════════════════════════════════════════════════╝
    """)
    
    # Sample patient scenario
    patient_scenario = {
        "patient_name": "Sarah Johnson",
        "age": 42,
        "symptoms": "fever, persistent cough, fatigue",
        "insurance": "BlueCross",
        "consultation_transcript": """
        Doctor: Good morning Sarah, what brings you in today?
        Patient: I've been having a fever and persistent cough for about 4 days.
        Doctor: Any other symptoms?
        Patient: Yes, feeling very fatigued and have some body aches.
        Doctor: Based on your symptoms, it appears you have a respiratory infection.
        Doctor: I'll prescribe Amoxicillin 500mg three times daily for 7 days.
        """
    }
    
    try:
        results = workflow_orchestrator.execute_patient_workflow(
            patient_name=patient_scenario["patient_name"],
            age=patient_scenario["age"],
            symptoms=patient_scenario["symptoms"],
            insurance=patient_scenario["insurance"],
            consultation_transcript=patient_scenario["consultation_transcript"]
        )
        
        print(f"\n✓ Healthcare workflow completed successfully!")
        print(f"Total steps executed: {results['total_steps']}")
        
        return 0
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
