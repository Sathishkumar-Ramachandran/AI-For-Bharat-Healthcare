"""Initialize patient records database."""
import sqlite3
from pathlib import Path


def init_database():
    """Create database and tables."""
    db_path = Path(__file__).parent / "patient_records.db"
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create patient_intake table
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
    
    # Create patient_records table
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
    
    # Insert sample data
    cursor.execute("""
        INSERT INTO patient_records 
        (patient_id, visit_reason, diagnosis, tests_taken, medicines_prescribed, 
         doctor_notes, navigation_instructions, visit_timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        'P001',
        'Fever and headache',
        'Viral Infection',
        'CBC, Blood Culture',
        'Paracetamol 500mg twice daily',
        'Rest and hydration recommended',
        'Laboratory - Floor 2, Block A, Room 201',
        '2024-03-01T10:30:00'
    ))
    
    conn.commit()
    conn.close()
    
    print(f"✓ Database initialized at {db_path}")


if __name__ == "__main__":
    init_database()
