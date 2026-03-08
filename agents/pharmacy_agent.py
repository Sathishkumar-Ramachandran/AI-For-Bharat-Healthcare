"""Pharmacy Agent for medicine recommendations and inventory."""
from services.bedrock_client import bedrock_client
from services.mcp_server import mcp_server
from typing import Dict, Any, List


class PharmacyAgent:
    """Agent responsible for pharmacy operations and medicine recommendations."""
    
    def __init__(self):
        """Initialize the Pharmacy Agent."""
        self.role = "Hospital Pharmacist"
    
    def recommend_medicines(self, diagnosis: str, symptoms: List[str]) -> Dict[str, Any]:
        """
        Recommend medicines based on diagnosis and symptoms.
        
        Args:
            diagnosis: Patient diagnosis
            symptoms: List of symptoms
            
        Returns:
            Medicine recommendations with availability
        """
        prompt = f"""As a hospital pharmacist, recommend appropriate medicines for:
        
Diagnosis: {diagnosis}
Symptoms: {', '.join(symptoms)}

Provide a list of medicines with:
1. Medicine name
2. Dosage
3. Frequency
4. Duration
5. Instructions

Format as a structured list."""
        
        llm_response = bedrock_client.invoke_nova(
            prompt=prompt,
            system_prompt="You are an experienced hospital pharmacist. Provide safe, evidence-based medicine recommendations."
        )
        
        # Get pharmacy inventory
        pharmacy_inventory = mcp_server.get_pharmacy_inventory()
        
        # Parse recommendations and check availability
        medicines = self._parse_medicine_recommendations(llm_response, pharmacy_inventory)
        
        return {
            "recommendations": medicines,
            "llm_analysis": llm_response,
            "total_medicines": len(medicines),
            "status": "completed"
        }
    
    def check_medicine_availability(self, medicine_name: str) -> Dict[str, Any]:
        """Check if medicine is available in pharmacy."""
        inventory = mcp_server.get_pharmacy_inventory()
        
        for item in inventory:
            if medicine_name.lower() in item['medicine_name'].lower():
                return {
                    "medicine_name": item['medicine_name'],
                    "stock_status": "available" if item['stock'] > 0 else "out_of_stock",
                    "current_stock": item['stock'],
                    "substitute_available": item.get('substitute', 'N/A')
                }
        
        return {
            "medicine_name": medicine_name,
            "stock_status": "not_found",
            "current_stock": 0,
            "substitute_available": "Check with pharmacist"
        }
    
    def get_pharmacy_status(self) -> Dict[str, Any]:
        """Get overall pharmacy inventory status."""
        inventory = mcp_server.get_pharmacy_inventory()
        
        low_stock = []
        out_of_stock = []
        adequate_stock = []
        
        for item in inventory:
            if item['stock'] == 0:
                out_of_stock.append(item['medicine_name'])
            elif item['stock'] < item['reorder_level']:
                low_stock.append({
                    "medicine": item['medicine_name'],
                    "current_stock": item['stock'],
                    "reorder_level": item['reorder_level']
                })
            else:
                adequate_stock.append(item['medicine_name'])
        
        return {
            "total_medicines": len(inventory),
            "low_stock_count": len(low_stock),
            "out_of_stock_count": len(out_of_stock),
            "low_stock_items": low_stock,
            "out_of_stock_items": out_of_stock,
            "status": "critical" if len(out_of_stock) > 0 else "warning" if len(low_stock) > 0 else "adequate"
        }
    
    def _parse_medicine_recommendations(self, llm_response: str, inventory: List[Dict]) -> List[Dict[str, Any]]:
        """Parse LLM response and match with inventory."""
        # Simple parsing - in production, use more sophisticated NLP
        medicines = []
        
        # Extract medicine names from response (simplified)
        common_medicines = ['Paracetamol', 'Ibuprofen', 'Amoxicillin', 'Azithromycin', 
                          'Omeprazole', 'Cetirizine', 'Metformin', 'Aspirin']
        
        for med in common_medicines:
            if med.lower() in llm_response.lower():
                availability = self.check_medicine_availability(med)
                medicines.append({
                    "medicine_name": med,
                    "stock_status": availability['stock_status'],
                    "current_stock": availability['current_stock'],
                    "substitute": availability.get('substitute_available', 'N/A')
                })
        
        return medicines


pharmacy_agent = PharmacyAgent()
