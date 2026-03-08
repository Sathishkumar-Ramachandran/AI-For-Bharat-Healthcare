"""Run the Streamlit dashboard."""
import subprocess
import sys
from pathlib import Path

# Initialize database first
print("Initializing database...")
from database.init_db import init_database
init_database()

print("\n🚀 Starting Healthcare Agentic System Dashboard...")
print("📍 Dashboard will open in your browser automatically")
print("🔗 URL: http://localhost:8501\n")

# Run Streamlit
subprocess.run([
    sys.executable, "-m", "streamlit", "run",
    str(Path("dashboard/dashboard.py")),
    "--server.port=8501",
    "--server.address=0.0.0.0"
])
