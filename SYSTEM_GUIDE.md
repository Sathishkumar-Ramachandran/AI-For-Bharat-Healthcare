# Healthcare Agentic System - Complete Guide

## 🎯 System Overview

This is a comprehensive healthcare automation platform with 12 AI agents, 3-tab dashboard, and complete hospital management capabilities.

## 🚀 Quick Start Guide

### Option 1: Streamlit Dashboard (Recommended)
```bash
python run_dashboard.py
```
Access at: http://localhost:8501

### Option 2: FastAPI Web Interface
```bash
python run_api.py
```
Access at: http://localhost:8000

### Option 3: CLI Interface
```bash
python main.py
```

## 📋 Dashboard Features

### Tab 1: Treatment Flow
**Purpose**: Voice-driven doctor-patient consultation

**Features**:
- Doctor voice input simulation
- Patient voice input simulation
- AI-powered symptom extraction
- Automated diagnosis
- Test recommendations
- Prescription generation
- Pharmacy availability check
- Hospital navigation

**Workflow**:
1. Enter doctor's question (e.g., "What is your problem?")
2. Enter patient's response (e.g., "I have had fever for three days")
3. Enter patient age
4. Click "Process Consultation"
5. View structured results with symptoms, diagnosis, tests, and medicines

### Tab 2: Hospital Management
**Purpose**: Real-time hospital operations monitoring

**Displays**:
- **Security Monitoring**: Score, anomalies, HIPAA compliance
- **Staffing Predictions**: Current patients, required nurses, ratios
- **Insurance Status**: Verification capabilities
- **Inventory Management**: Stock levels, reorder alerts
- **Pharmacy Status**: Medicine availability, low stock items

**Features**:
- Real-time metrics
- Alert notifications
- Status indicators
- Detailed breakdowns

### Tab 3: Patient Data Tracking
**Purpose**: Patient medical records and navigation

**Features**:
- Patient record lookup by ID
- Medical history display
- Test results tracking
- Prescription history
- Hospital navigation guidance
- Department finder

**Workflow**:
1. Enter patient ID (e.g., P001)
2. Click "View My Records"
3. See complete visit history
4. Get navigation instructions

## 🤖 AI Agents

### Treatment Flow Agents
1. **Scribing Agent**: Extracts symptoms from conversation
2. **Diagnosis Agent**: Analyzes symptoms and predicts diagnosis
3. **Test Recommendation Agent**: Recommends appropriate tests
4. **Prescription Agent**: Generates prescriptions
5. **Pharmacy Agent**: Checks medicine availability
6. **Navigation Agent**: Provides hospital directions

### Hospital Management Agents
7. **Security Agent**: Monitors threats and compliance
8. **Staffing Agent**: Predicts nurse requirements
9. **Insurance Agent**: Verifies coverage
10. **Inventory Agent**: Tracks medical supplies
11. **Patient Agent**: Manages patient intake
12. **Orchestrator Agent**: Coordinates workflows

## 📊 Data Flow

```
User Input (Voice/Text)
    ↓
Speech-to-Text Service
    ↓
Scribing Agent (Extract Symptoms)
    ↓
Diagnosis Agent (Analyze)
    ↓
Test Recommendation Agent
    ↓
Prescription Agent
    ↓
Pharmacy Agent (Check Availability)
    ↓
Navigation Agent (Provide Directions)
    ↓
Database (Save Records)
    ↓
Display Results
```

## 🗄️ Database Schema

### patient_intake Table
- id (PRIMARY KEY)
- patient_id
- symptoms
- diagnosis
- recommended_tests
- prescription
- consultation_timestamp

### patient_records Table
- id (PRIMARY KEY)
- patient_id
- visit_reason
- diagnosis
- tests_taken
- medicines_prescribed
- doctor_notes
- navigation_instructions
- visit_timestamp

## 🏥 Hospital Map

| Department | Floor | Block | Room |
|-----------|-------|-------|------|
| Laboratory | 2 | A | 201 |
| Radiology | 3 | B | 301 |
| Pharmacy | 1 | B | 105 |
| Cardiology | 4 | A | 401 |
| Emergency | 1 | A | 101 |
| Reception | 1 | A | 100 |
| ICU | 5 | A | 501 |

## 💊 Pharmacy Inventory

The system tracks 15 medicines including:
- Paracetamol, Ibuprofen (Analgesics)
- Amoxicillin, Azithromycin (Antibiotics)
- Omeprazole (Antacid)
- Cetirizine (Antihistamine)
- Metformin (Antidiabetic)
- And more...

Each medicine has:
- Stock level
- Reorder threshold
- Substitute medicine
- Manufacturer

## 🔐 Security Features

- HIPAA compliance monitoring
- Anomaly detection
- Security scoring (0-100)
- Access log analysis
- Threat detection
- Alert system

## 📈 Staffing Predictions

Uses historical data to predict:
- Required nurse count
- Nurse-to-patient ratio
- Department-wise requirements
- Shift recommendations

## 💳 Insurance Verification

Supports multiple providers:
- BlueCross
- Aetna
- Medicare

Calculates:
- Coverage percentage
- Patient responsibility
- Authorization status

## 🧪 Test Recommendations

Common tests mapped to departments:
- CBC, Blood Culture → Laboratory
- X-Ray, CT Scan → Radiology
- ECG, Echo → Cardiology

## 🗺️ Navigation System

Provides:
- Step-by-step directions
- Department locations
- Estimated time
- Priority ordering

## 🔧 Configuration

### AWS Credentials (.env)
```env
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1
NOVA_MODEL_ID=us.amazon.nova-lite-v1:0
```

### System Settings (config/settings.py)
- AWS region
- Model ID
- Max tokens
- Temperature

## 📝 Sample Usage

### Example 1: Patient Consultation
```
Doctor Input: "What is your problem?"
Patient Input: "I have had fever for three days"
Patient Age: 35

Results:
- Symptoms: fever
- Diagnosis: Viral Infection
- Tests: CBC, Blood Culture
- Medicine: Paracetamol 500mg twice daily
- Navigation: Laboratory - Floor 2, Block A, Room 201
```

### Example 2: Check Patient Records
```
Patient ID: P001

Results:
- Visit Date: 2024-03-01
- Reason: Fever and headache
- Diagnosis: Viral Infection
- Tests: CBC, Blood Culture
- Medicines: Paracetamol
- Navigation: Laboratory directions
```

## 🚨 Troubleshooting

### Dashboard won't start
```bash
pip install streamlit
python run_dashboard.py
```

### API server error
```bash
pip install fastapi uvicorn
python run_api.py
```

### Database not found
```bash
python database/init_db.py
```

### AWS connection issues
- Check .env file
- Verify credentials
- System works in fallback mode

## 📚 Additional Resources

- README.md - Project overview
- AWS_SETUP_GUIDE.md - AWS configuration
- PROJECT_STATUS.md - Implementation status
- CHECKLIST.md - Development checklist

## 🎓 Learning Path

1. Start with CLI interface (main.py)
2. Try FastAPI web interface
3. Explore Streamlit dashboard
4. Review agent implementations
5. Understand data flow
6. Customize for your needs

## 🔄 Workflow Orchestration

### Treatment Flow
```python
from tasks.treatment_flow_tasks import treatment_flow_orchestrator

result = treatment_flow_orchestrator.execute_treatment_flow(
    doctor_input="What is your problem?",
    patient_input="I have fever",
    patient_age=35
)
```

### Hospital Management
```python
from tasks.hospital_management_tasks import hospital_management_orchestrator

status = hospital_management_orchestrator.get_hospital_status()
```

### Patient Tracking
```python
from tasks.patient_tracking_tasks import patient_tracking_orchestrator

history = patient_tracking_orchestrator.get_patient_history("P001")
```

## 🎯 Best Practices

1. **Always initialize database first**
2. **Use Streamlit dashboard for demos**
3. **Check pharmacy inventory regularly**
4. **Monitor security alerts**
5. **Review staffing predictions daily**
6. **Keep patient records updated**
7. **Test navigation instructions**

## 📞 Support

For issues:
1. Check this guide
2. Review error messages
3. Check logs
4. Verify configuration
5. Test with sample data

---

**System Version**: 2.0.0
**Last Updated**: 2024
**Status**: Fully Operational
