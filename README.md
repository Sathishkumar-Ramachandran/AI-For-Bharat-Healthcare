# Agentic Healthcare Workflow Automation System

A multi-agent healthcare automation platform using **Amazon Nova** (via Bedrock), **CrewAI**, and **Model Context Protocol (MCP)**.

## 🎯 Overview

This system demonstrates automation of healthcare workflows including:
- Patient intake and registration
- Clinical documentation generation
- Insurance authorization
- Staffing prediction
- Inventory management
- Cybersecurity monitoring

## 🤖 AI Agents

1. **Patient Intake Agent** - Registers patients and creates FHIR records
2. **Clinical Scribing Agent** - Converts consultations to clinical notes
3. **Insurance Authorization Agent** - Processes insurance approvals
4. **Staffing Prediction Agent** - Predicts nurse requirements
5. **Supply Chain Agent** - Monitors medical inventory
6. **Cybersecurity Monitoring Agent** - Detects security threats
7. **Workflow Orchestrator Agent** - Coordinates all agents

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Configure AWS credentials (optional - has fallback mode)
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_REGION=us-east-1

# Run the system
python main.py
```

### What You'll See

The system will execute a complete patient workflow:
1. Patient registration
2. Clinical note generation
3. Insurance authorization
4. Staffing predictions
5. Inventory monitoring
6. Security assessment

## 📊 Sample Output

```
STEP 1: Patient Intake
✓ Patient registered: P006
  Symptoms: fever, persistent cough, fatigue

STEP 2: Clinical Documentation
✓ Clinical notes generated
  Diagnosis: Respiratory infection

STEP 3: Insurance Authorization
✓ Authorization: APPROVED
  Coverage: 80%

STEP 4: Staffing Prediction
✓ Predicted nurses needed: 13

STEP 5: Inventory Check
✓ Status: CRITICAL
  Items needing reorder: 2

STEP 6: Security Monitoring
✓ Security Score: 100/100
  HIPAA Compliant: Yes
```

## 📁 Project Structure

```
healthcare_agentic_system/
├── agents/          # 7 AI agents
├── services/        # Bedrock, MCP, FHIR services
├── data/            # Sample datasets
├── config/          # Configuration
└── main.py          # Main workflow
```

## 🔧 Technologies

- **Python 3.9+**
- **CrewAI** - Multi-agent orchestration
- **Amazon Nova** - LLM via Bedrock
- **MCP** - Model Context Protocol
- **FHIR R4** - Healthcare standards
- **pandas** - Data processing

## 📝 Requirements

```
crewai==0.28.8
boto3==1.34.51
pandas==2.2.0
python-dotenv==1.0.1
```

## 🎓 Features

✅ Multi-agent AI orchestration
✅ Amazon Nova LLM integration
✅ FHIR-compliant healthcare data
✅ Model Context Protocol (MCP)
✅ Clinical documentation automation
✅ Insurance authorization automation
✅ Predictive staffing analytics
✅ Inventory management
✅ Security monitoring
✅ HIPAA compliance checks

## 🔒 Security & Compliance

- HIPAA compliance monitoring
- Security threat detection
- Access log analysis
- Anomaly detection
- Patient data protection

## 📚 Documentation

- Sample data included in `data/` directory
- Configuration in `config/settings.py`
- All agents in `agents/` directory
- Services in `services/` directory

## 🆘 Troubleshooting

**Issue**: AWS credentials error
**Solution**: System works in fallback mode without AWS

**Issue**: Module not found
**Solution**: Run `pip install -r requirements.txt`

## 📄 License

MIT License (or as specified)

## 🤝 Contributing

Contributions welcome! This is a prototype system for demonstration purposes.

---

**Version**: 1.0.0
**Status**: Production-Ready Prototype
