"""Insurance Authorization Agent for checking coverage and approvals."""
from services.bedrock_client import bedrock_client
from services.mcp_server import mcp_server
from typing import Dict, Any


class InsuranceAuthorizationAgent:
    """Agent responsible for insurance eligibility and authorization checks."""
    
    def __init__(self):
        """Initialize the Insurance Authorization Agent."""
        self.role = "Insurance Authorization Specialist"
    
    def check_authorization(self, patient_data: Dict[str, Any], clinical_notes: Dict[str, Any], procedure_codes: list = None) -> Dict[str, Any]:
        """Check insurance authorization for patient treatment."""
        insurance_provider = patient_data.get("insurance", "Unknown")
        diagnosis = clinical_notes.get("diagnosis", "Unknown")
        
        insurance_rules = mcp_server.get_insurance_rules()
        provider_info = insurance_rules.get("providers", {}).get(insurance_provider, {})
        
        if not provider_info:
            return {"status": "denied", "reason": "Insurance provider not recognized", "coverage": 0}
        
        if procedure_codes is None:
            procedure_codes = ["consultation"]
        
        total_cost = sum(insurance_rules.get("procedure_codes", {}).get(code, 0) for code in procedure_codes)
        coverage_rate = provider_info.get("coverage", 0)
        copay = provider_info.get("copay", 0)
        
        covered_amount = total_cost * coverage_rate
        patient_responsibility = total_cost - covered_amount + copay
        
        status = "approved" if coverage_rate >= 0.7 else "pending"
        
        return {
            "status": status,
            "insurance_provider": insurance_provider,
            "coverage_rate": coverage_rate,
            "total_cost": total_cost,
            "covered_amount": covered_amount,
            "patient_responsibility": patient_responsibility,
            "copay": copay,
            "procedure_codes": procedure_codes
        }


insurance_authorization_agent = InsuranceAuthorizationAgent()
