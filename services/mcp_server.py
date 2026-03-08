"""Model Context Protocol (MCP) data access layer."""
import json
import pandas as pd
from typing import Dict, Any, List, Optional
from pathlib import Path


class MCPServer:
    """MCP-style data access layer for healthcare resources."""
    
    def __init__(self, data_dir: str = "./data"):
        """Initialize MCP server with data directory."""
        self.data_dir = Path(data_dir)
        self._ensure_data_dir()
    
    def _ensure_data_dir(self):
        """Ensure data directory exists."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def get_patient_data(self, patient_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve patient data from MCP resource."""
        try:
            df = pd.read_csv(self.data_dir / "patients.csv")
            if patient_id:
                df = df[df['patient_id'] == patient_id]
            return df.to_dict('records')
        except FileNotFoundError:
            return []
    
    def get_insurance_rules(self) -> Dict[str, Any]:
        """Retrieve insurance authorization rules."""
        try:
            with open(self.data_dir / "insurance_rules.json", 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"providers": {}}
    
    def get_inventory_data(self) -> List[Dict[str, Any]]:
        """Retrieve medical inventory data."""
        try:
            df = pd.read_csv(self.data_dir / "inventory.csv")
            return df.to_dict('records')
        except FileNotFoundError:
            return []
    
    def get_staffing_history(self) -> List[Dict[str, Any]]:
        """Retrieve historical staffing data."""
        try:
            df = pd.read_csv(self.data_dir / "staffing_history.csv")
            return df.to_dict('records')
        except FileNotFoundError:
            return []
    
    def get_pharmacy_inventory(self) -> List[Dict[str, Any]]:
        """Retrieve pharmacy inventory data."""
        try:
            df = pd.read_csv(self.data_dir / "pharmacy_inventory.csv")
            return df.to_dict('records')
        except FileNotFoundError:
            return []
    
    def get_patient_records(self, patient_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve patient medical records."""
        try:
            import sqlite3
            db_path = Path("database/patient_records.db")
            
            if not db_path.exists():
                return []
            
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if patient_id:
                cursor.execute("SELECT * FROM patient_records WHERE patient_id = ?", (patient_id,))
            else:
                cursor.execute("SELECT * FROM patient_records ORDER BY visit_timestamp DESC LIMIT 100")
            
            records = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            return records
        except Exception as e:
            print(f"Error retrieving patient records: {e}")
            return []
    
    def save_patient_intake(self, intake_data: Dict[str, Any]) -> bool:
        """Save patient intake data to database."""
        try:
            import sqlite3
            from datetime import datetime
            
            db_path = Path("database/patient_records.db")
            db_path.parent.mkdir(parents=True, exist_ok=True)
            
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Create table if not exists
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS patient_intake (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id TEXT NOT NULL,
                    symptoms TEXT,
                    diagnosis TEXT,
                    recommended_tests TEXT,
                    prescription TEXT,
                    consultation_timestamp TEXT
                )
            """)
            
            cursor.execute("""
                INSERT INTO patient_intake 
                (patient_id, symptoms, diagnosis, recommended_tests, prescription, consultation_timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                intake_data.get('patient_id'),
                intake_data.get('symptoms'),
                intake_data.get('diagnosis'),
                intake_data.get('recommended_tests'),
                intake_data.get('prescription'),
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error saving patient intake: {e}")
            return False
    
    def save_patient_record(self, record_data: Dict[str, Any]) -> bool:
        """Save complete patient record to database."""
        try:
            import sqlite3
            from datetime import datetime
            
            db_path = Path("database/patient_records.db")
            db_path.parent.mkdir(parents=True, exist_ok=True)
            
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Create table if not exists
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS patient_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id TEXT NOT NULL,
                    visit_reason TEXT,
                    diagnosis TEXT,
                    tests_taken TEXT,
                    medicines_prescribed TEXT,
                    doctor_notes TEXT,
                    navigation_instructions TEXT,
                    visit_timestamp TEXT
                )
            """)
            
            cursor.execute("""
                INSERT INTO patient_records 
                (patient_id, visit_reason, diagnosis, tests_taken, medicines_prescribed, 
                 doctor_notes, navigation_instructions, visit_timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                record_data.get('patient_id'),
                record_data.get('visit_reason'),
                record_data.get('diagnosis'),
                record_data.get('tests_taken'),
                record_data.get('medicines_prescribed'),
                record_data.get('doctor_notes'),
                record_data.get('navigation_instructions'),
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error saving patient record: {e}")
            return False


mcp_server = MCPServer()
