"""Staffing Prediction Agent for hospital resource planning."""
from services.mcp_server import mcp_server
from typing import Dict, Any
import pandas as pd


class StaffingPredictionAgent:
    """Agent responsible for predicting hospital staffing needs."""
    
    def __init__(self):
        """Initialize the Staffing Prediction Agent."""
        self.role = "Hospital Staffing Coordinator"
    
    def predict_staffing_needs(self, current_patient_count: int = None) -> Dict[str, Any]:
        """Predict staffing requirements based on historical data."""
        staffing_history = mcp_server.get_staffing_history()
        
        if not staffing_history:
            return {"status": "insufficient_data", "recommendation": "Unable to predict"}
        
        df = pd.DataFrame(staffing_history)
        avg_patient_count = df['patient_count'].mean()
        avg_nurse_count = df['nurse_count'].mean()
        nurse_to_patient_ratio = avg_nurse_count / avg_patient_count if avg_patient_count > 0 else 0.25
        
        if current_patient_count is None:
            current_patient_count = int(avg_patient_count)
        
        predicted_nurses = int(current_patient_count * nurse_to_patient_ratio)
        
        return {
            "current_patient_count": current_patient_count,
            "predicted_nurse_count": predicted_nurses,
            "nurse_to_patient_ratio": f"1:{(1/nurse_to_patient_ratio):.1f}",
            "historical_avg_patients": round(avg_patient_count, 1),
            "historical_avg_nurses": round(avg_nurse_count, 1),
            "status": "adequate" if predicted_nurses <= avg_nurse_count * 1.2 else "additional_staff_needed"
        }


staffing_prediction_agent = StaffingPredictionAgent()
