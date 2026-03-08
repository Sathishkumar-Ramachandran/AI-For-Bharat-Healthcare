"""Configuration settings for the healthcare agentic system."""
import os
from dotenv import load_dotenv

load_dotenv()

# AWS Bedrock Configuration
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# Amazon Nova Model Configuration
NOVA_MODEL_ID = "us.amazon.nova-pro-v1:0"
MAX_TOKENS = 2048
TEMPERATURE = 0.7

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./healthcare.db")

# MCP Configuration
MCP_SERVER_HOST = "localhost"
MCP_SERVER_PORT = 8001

# API Configuration
API_HOST = "0.0.0.0"
API_PORT = 8000

# Vector Database
CHROMA_PERSIST_DIR = "./data/chroma_db"

# Healthcare Standards
FHIR_VERSION = "R4"
