# Quick Start Guide - Healthcare Agentic System

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure AWS (Optional)
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your AWS credentials
# (System works in fallback mode without AWS)
```

### Step 3: Run the System

Choose one of three interfaces:

#### Option A: Streamlit Dashboard (Recommended) 🌟
```bash
python run_dashboard.py
```
**Access**: http://localhost:8501

**Features**:
- 3-tab interface
- Voice-driven consultation
- Hospital management
- Patient data tracking

#### Option B: FastAPI Web Interface
```bash
python run_api.py
```
**Access**: http://localhost:8000

**Features**:
- Beautiful web UI
- REST API
- Real-time workflow execution
- API documentation at /docs

#### Option C: CLI Interface
```bash
python main.py
```
**Features**:
- Command-line interface
- Quick testing
- Direct agent interaction

## 📋 What Each Interface Does

### Streamlit Dashboard (Port 8501)

**Tab 1: Treatment Flow**
- Enter doctor and patient conversation
- AI extracts symptoms
- Generates diagnosis
- Recommends tests
- Creates prescription
- Checks pharmacy availability
- Provides hospital navigation

**Tab 2: Hospital Management**
- Security monitoring (score, alerts)
- Staffing predictions (nurses needed)
- Insurance status
- Inventory management (low stock alerts)
- Pharmacy status (medicine availability)

**Tab 3: Patient Data Tracking**
- View patient medical records
- See visit history
- Get hospital navigation
- Find departments

### FastAPI Web Interface (Port 8000)

- Submit patient information via form
- Execute complete workflow
- View structured results
- See system status dashboard
- Access API documentation

### CLI Interface

- Run complete patient workflow
- See step-by-step execution
- Test individual agents
- Quick verification

## 🎯 Try These Examples

### Example 1: Patient Consultation (Streamlit)
1. Open http://localhost:8501
2. Go to "Treatment Flow" tab
3. Enter:
   - Doctor: "What is your problem?"
   - Patient: "I have had fever for three days"
   - Age: 35
4. Click "Process Consultation"
5. View results with diagnosis, tests, and medicines

### Example 2: Check Hospital Status (Streamlit)
1. Go to "Hospital Management" tab
2. Click "Refresh Dashboard"
3. View:
   - Security score
   - Staffing requirements
   - Inventory alerts
   - Pharmacy status

### Example 3: View Patient Records (Streamlit)
1. Go to "Patient Data Tracking" tab
2. Enter Patient ID: P001
3. Click "View My Records"
4. See complete medical history

### Example 4: API Workflow (FastAPI)
1. Open http://localhost:8000
2. Fill patient form:
   - Name: John Doe
   - Age: 45
   - Symptoms: fever, headache, fatigue
   - Insurance: BlueCross
3. Click "Execute Workflow"
4. View 6-step results

### Example 5: CLI Test
```bash
python main.py
```
Watch the complete workflow execute with all 7 steps.

## 🧪 Test the System

Run the integration test:
```bash
python test_complete_system.py
```

This verifies:
- All 12 agents working
- All 4 services operational
- Database connected
- Data files present
- AWS connection (if configured)

## 📊 System Components

### 12 AI Agents
1. Patient Intake Agent
2. Clinical Scribing Agent
3. Diagnosis Agent
4. Test Recommendation Agent
5. Prescription Agent
6. Pharmacy Agent
7. Navigation Agent
8. Insurance Authorization Agent
9. Staffing Prediction Agent
10. Supply Chain Agent
11. Cybersecurity Monitoring Agent
12. Workflow Orchestrator

### 4 Services
1. Amazon Bedrock Client (Nova LLM)
2. MCP Server (Data Access)
3. FHIR Service (Healthcare Standards)
4. Speech-to-Text Service

### 3 Task Orchestrators
1. Treatment Flow Orchestrator
2. Hospital Management Orchestrator
3. Patient Tracking Orchestrator

## 🗄️ Data Files

- `data/patients.csv` - 5 sample patients
- `data/inventory.csv` - 8 medical items
- `data/staffing_history.csv` - 7 days history
- `data/insurance_rules.json` - 3 providers
- `data/pharmacy_inventory.csv` - 15 medicines
- `database/patient_records.db` - SQLite database

## 🔧 Troubleshooting

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

### Database error
```bash
python database/init_db.py
```

### Import errors
```bash
pip install -r requirements.txt
```

### AWS connection issues
- System works in fallback mode without AWS
- Check .env file for credentials
- Verify AWS region is us-east-1

## 📚 Documentation

- **SYSTEM_GUIDE.md** - Complete user guide
- **IMPLEMENTATION_SUMMARY.md** - Technical details
- **AWS_SETUP_GUIDE.md** - AWS configuration
- **README.md** - Project overview

## 🎓 Learning Path

1. **Start Simple**: Run CLI interface (`python main.py`)
2. **Try Web UI**: Run FastAPI (`python run_api.py`)
3. **Explore Dashboard**: Run Streamlit (`python run_dashboard.py`)
4. **Read Code**: Check agent implementations
5. **Customize**: Modify for your needs

## 💡 Tips

- Use Streamlit dashboard for demos
- Use FastAPI for API integration
- Use CLI for quick testing
- Check logs for debugging
- Review sample data for examples
- Test with different symptoms
- Explore all three tabs in dashboard

## 🎯 Common Tasks

### Add a new patient
Use Treatment Flow tab in Streamlit dashboard

### Check pharmacy stock
Go to Hospital Management tab → Pharmacy Status

### Find a department
Go to Patient Data Tracking tab → Department Finder

### View patient history
Enter patient ID in Patient Data Tracking tab

### Monitor security
Check Hospital Management tab → Security Monitoring

### Predict staffing
View Hospital Management tab → Staffing Predictions

## ✅ Verification Checklist

- [ ] Dependencies installed
- [ ] Database initialized
- [ ] Can run CLI interface
- [ ] Can access Streamlit dashboard
- [ ] Can access FastAPI interface
- [ ] Integration test passes
- [ ] Sample workflow executes
- [ ] All tabs in dashboard work

## 🚀 You're Ready!

The system is fully operational. Choose your preferred interface and start exploring the healthcare agentic workflow automation platform.

**Recommended**: Start with the Streamlit dashboard for the best experience.

```bash
python run_dashboard.py
```

Then open: http://localhost:8501

---

**Need Help?** Check SYSTEM_GUIDE.md for detailed documentation.
