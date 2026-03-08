"""Navigation Agent for hospital campus guidance."""
from typing import Dict, Any, List


class NavigationAgent:
    """Agent responsible for hospital navigation guidance."""
    
    def __init__(self):
        """Initialize the Navigation Agent."""
        self.role = "Hospital Navigator"
        
        # Hospital layout mapping
        self.hospital_map = {
            "Laboratory": {"floor": 2, "block": "A", "room": "201"},
            "Radiology": {"floor": 3, "block": "B", "room": "301"},
            "Pharmacy": {"floor": 1, "block": "B", "room": "105"},
            "Cardiology": {"floor": 4, "block": "A", "room": "401"},
            "Emergency": {"floor": 1, "block": "A", "room": "101"},
            "Reception": {"floor": 1, "block": "A", "room": "100"},
            "ICU": {"floor": 5, "block": "A", "room": "501"},
        }
    
    def get_navigation_instructions(self, tests: List[str] = None, pharmacy_needed: bool = False) -> Dict[str, Any]:
        """
        Generate navigation instructions based on required services.
        
        Args:
            tests: List of tests to be performed
            pharmacy_needed: Whether pharmacy visit is needed
            
        Returns:
            Navigation instructions with locations
        """
        destinations = []
        
        # Add test locations
        if tests:
            for test in tests:
                location = self._get_test_location(test)
                if location:
                    destinations.append(location)
        
        # Add pharmacy if needed
        if pharmacy_needed:
            destinations.append({
                "destination": "Pharmacy",
                "location": self.hospital_map["Pharmacy"],
                "purpose": "Collect prescribed medicines",
                "priority": "After tests"
            })
        
        # Generate step-by-step directions
        directions = self._generate_directions(destinations)
        
        return {
            "destinations": destinations,
            "step_by_step_directions": directions,
            "total_stops": len(destinations),
            "estimated_time": len(destinations) * 10,  # 10 mins per stop
            "status": "ready"
        }
    
    def _get_test_location(self, test_name: str) -> Dict[str, Any]:
        """Get location for a specific test."""
        test_lower = test_name.lower()
        
        if 'lab' in test_lower or 'blood' in test_lower or 'cbc' in test_lower or 'urine' in test_lower:
            dept = "Laboratory"
        elif 'x-ray' in test_lower or 'ct' in test_lower or 'mri' in test_lower or 'radiology' in test_lower:
            dept = "Radiology"
        elif 'ecg' in test_lower or 'echo' in test_lower or 'cardiac' in test_lower:
            dept = "Cardiology"
        else:
            dept = "Laboratory"  # Default
        
        location = self.hospital_map.get(dept, self.hospital_map["Laboratory"])
        
        return {
            "destination": dept,
            "location": location,
            "purpose": f"Perform {test_name}",
            "priority": "Required"
        }
    
    def _generate_directions(self, destinations: List[Dict]) -> List[str]:
        """Generate step-by-step directions."""
        directions = []
        
        for i, dest in enumerate(destinations, 1):
            loc = dest['location']
            directions.append(
                f"Step {i}: Go to {dest['destination']} - "
                f"Floor {loc['floor']}, Block {loc['block']}, Room {loc['room']}"
            )
        
        return directions
    
    def get_department_info(self, department: str) -> Dict[str, Any]:
        """Get detailed information about a department."""
        location = self.hospital_map.get(department)
        
        if not location:
            return {"error": "Department not found"}
        
        return {
            "department": department,
            "floor": location['floor'],
            "block": location['block'],
            "room": location['room'],
            "full_address": f"Floor {location['floor']}, Block {location['block']}, Room {location['room']}"
        }


navigation_agent = NavigationAgent()
