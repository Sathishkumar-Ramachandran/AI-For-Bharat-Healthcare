"""Run the FastAPI web server."""
import subprocess
import sys
from pathlib import Path

# Initialize database first
print("Initializing database...")
from database.init_db import init_database
init_database()

print("\n🚀 Starting Healthcare Agentic System API Server...")
print("📍 Open your browser to: http://localhost:8000")
print("📖 API Documentation: http://localhost:8000/docs\n")

# Run FastAPI with uvicorn
subprocess.run([
    sys.executable, "-m", "uvicorn",
    "api.main_api:app",
    "--host", "0.0.0.0",
    "--port", "8000",
    "--reload"
])
