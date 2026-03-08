"""FastAPI backend for the Healthcare Agentic System."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
from agents.orchestrator_agent import workflow_orchestrator
from agents.patient_agent import patient_intake_agent
from agents.insurance_agent import insurance_authorization_agent
from agents.staffing_agent import staffing_prediction_agent
from agents.inventory_agent import supply_chain_agent
from agents.security_agent import cybersecurity_monitoring_agent
from services.mcp_server import mcp_server

app = FastAPI(
    title="Healthcare Agentic Workflow API",
    description="Multi-agent healthcare automation platform",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class WorkflowRequest(BaseModel):
    """Complete workflow request model."""
    patient_name: str
    age: int
    symptoms: str
    insurance: str
    consultation_transcript: Optional[str] = None


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the web interface."""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Healthcare Agentic System</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            
            .header {
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                margin-bottom: 30px;
                text-align: center;
            }
            
            .header h1 {
                color: #667eea;
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            
            .header p {
                color: #666;
                font-size: 1.1em;
            }
            
            .main-content {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 30px;
            }
            
            .card {
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            
            .card h2 {
                color: #667eea;
                margin-bottom: 20px;
                font-size: 1.8em;
            }
            
            .form-group {
                margin-bottom: 20px;
            }
            
            label {
                display: block;
                margin-bottom: 8px;
                color: #333;
                font-weight: 600;
            }
            
            input, select, textarea {
                width: 100%;
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 1em;
                transition: border-color 0.3s;
            }
            
            input:focus, select:focus, textarea:focus {
                outline: none;
                border-color: #667eea;
            }
            
            textarea {
                resize: vertical;
                min-height: 100px;
            }
            
            button {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 15px 30px;
                border: none;
                border-radius: 8px;
                font-size: 1.1em;
                font-weight: 600;
                cursor: pointer;
                width: 100%;
                transition: transform 0.2s;
            }
            
            button:hover {
                transform: translateY(-2px);
            }
            
            button:disabled {
                opacity: 0.6;
                cursor: not-allowed;
            }
            
            .results {
                grid-column: 1 / -1;
            }
            
            .result-section {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 15px;
                border-left: 4px solid #667eea;
            }
            
            .result-section h3 {
                color: #667eea;
                margin-bottom: 10px;
            }
            
            .result-section p {
                color: #555;
                line-height: 1.6;
            }
            
            .status-badge {
                display: inline-block;
                padding: 5px 15px;
                border-radius: 20px;
                font-size: 0.9em;
                font-weight: 600;
                margin-left: 10px;
            }
            
            .status-success {
                background: #d4edda;
                color: #155724;
            }
            
            .status-warning {
                background: #fff3cd;
                color: #856404;
            }
            
            .status-info {
                background: #d1ecf1;
                color: #0c5460;
            }
            
            .loading {
                text-align: center;
                padding: 40px;
                color: #667eea;
                font-size: 1.2em;
            }
            
            .spinner {
                border: 4px solid #f3f3f3;
                border-top: 4px solid #667eea;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 20px auto;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin-top: 20px;
            }
            
            .stat-card {
                background: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            
            .stat-value {
                font-size: 2em;
                font-weight: bold;
                color: #667eea;
            }
            
            .stat-label {
                color: #666;
                margin-top: 5px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏥 Healthcare Agentic System</h1>
                <p>Powered by Amazon Nova + CrewAI + MCP</p>
            </div>
            
            <div class="main-content">
                <div class="card">
                    <h2>Patient Workflow</h2>
                    <form id="workflowForm">
                        <div class="form-group">
                            <label for="patientName">Patient Name *</label>
                            <input type="text" id="patientName" required placeholder="John Doe">
                        </div>
                        
                        <div class="form-group">
                            <label for="age">Age *</label>
                            <input type="number" id="age" required min="0" max="120" placeholder="45">
                        </div>
                        
                        <div class="form-group">
                            <label for="symptoms">Symptoms *</label>
                            <textarea id="symptoms" required placeholder="fever, headache, fatigue"></textarea>
                        </div>
                        
                        <div class="form-group">
                            <label for="insurance">Insurance Provider *</label>
                            <select id="insurance" required>
                                <option value="">Select Insurance</option>
                                <option value="BlueCross">BlueCross</option>
                                <option value="Aetna">Aetna</option>
                                <option value="Medicare">Medicare</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label for="transcript">Consultation Transcript (Optional)</label>
                            <textarea id="transcript" placeholder="Doctor: What symptoms? Patient: Fever and cough..."></textarea>
                        </div>
                        
                        <button type="submit" id="submitBtn">Execute Workflow</button>
                    </form>
                </div>
                
                <div class="card">
                    <h2>System Status</h2>
                    <div id="systemStatus">
                        <p style="color: #666;">Click "Execute Workflow" to see results</p>
                    </div>
                </div>
                
                <div class="card results" id="resultsCard" style="display: none;">
                    <h2>Workflow Results</h2>
                    <div id="results"></div>
                </div>
            </div>
        </div>
        
        <script>
            const form = document.getElementById('workflowForm');
            const submitBtn = document.getElementById('submitBtn');
            const resultsCard = document.getElementById('resultsCard');
            const resultsDiv = document.getElementById('results');
            const systemStatus = document.getElementById('systemStatus');
            
            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                
                submitBtn.disabled = true;
                submitBtn.textContent = 'Processing...';
                resultsCard.style.display = 'block';
                resultsDiv.innerHTML = '<div class="loading"><div class="spinner"></div><p>Executing workflow...</p></div>';
                
                const data = {
                    patient_name: document.getElementById('patientName').value,
                    age: parseInt(document.getElementById('age').value),
                    symptoms: document.getElementById('symptoms').value,
                    insurance: document.getElementById('insurance').value,
                    consultation_transcript: document.getElementById('transcript').value || null
                };
                
                try {
                    const response = await fetch('/workflow', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(data)
                    });
                    
                    const result = await response.json();
                    
                    if (response.ok) {
                        displayResults(result.data);
                        updateSystemStatus(result.data);
                    } else {
                        resultsDiv.innerHTML = `<div class="result-section" style="border-left-color: #dc3545;"><h3>Error</h3><p>${result.detail}</p></div>`;
                    }
                } catch (error) {
                    resultsDiv.innerHTML = `<div class="result-section" style="border-left-color: #dc3545;"><h3>Error</h3><p>Failed to connect to server: ${error.message}</p></div>`;
                } finally {
                    submitBtn.disabled = false;
                    submitBtn.textContent = 'Execute Workflow';
                }
            });
            
            function displayResults(data) {
                let html = '';
                
                // Patient Intake
                if (data.patient_intake) {
                    const intake = data.patient_intake;
                    html += `
                        <div class="result-section">
                            <h3>✅ Step 1: Patient Intake <span class="status-badge status-success">${intake.status}</span></h3>
                            <p><strong>Patient ID:</strong> ${intake.patient_id}</p>
                            <p><strong>Name:</strong> ${intake.name}</p>
                            <p><strong>Age:</strong> ${intake.age}</p>
                            <p><strong>Symptoms:</strong> ${intake.symptoms.join(', ')}</p>
                            <p><strong>Insurance:</strong> ${intake.insurance}</p>
                        </div>
                    `;
                }
                
                // Clinical Notes
                if (data.clinical_notes) {
                    const notes = data.clinical_notes;
                    html += `
                        <div class="result-section">
                            <h3>✅ Step 2: Clinical Documentation <span class="status-badge status-success">${notes.status}</span></h3>
                            <p><strong>Chief Complaint:</strong> ${notes.chief_complaint}</p>
                            <p><strong>Diagnosis:</strong> ${notes.diagnosis}</p>
                            <p><strong>Treatment Plan:</strong> ${notes.treatment_plan}</p>
                            <p><strong>Prescription:</strong> ${notes.prescription}</p>
                        </div>
                    `;
                }
                
                // Insurance Authorization
                if (data.insurance_authorization) {
                    const auth = data.insurance_authorization;
                    const statusClass = auth.status === 'approved' ? 'status-success' : 'status-warning';
                    html += `
                        <div class="result-section">
                            <h3>✅ Step 3: Insurance Authorization <span class="status-badge ${statusClass}">${auth.status.toUpperCase()}</span></h3>
                            <p><strong>Provider:</strong> ${auth.insurance_provider}</p>
                            <p><strong>Coverage Rate:</strong> ${(auth.coverage_rate * 100).toFixed(0)}%</p>
                            <p><strong>Total Cost:</strong> $${auth.total_cost.toFixed(2)}</p>
                            <p><strong>Covered Amount:</strong> $${auth.covered_amount.toFixed(2)}</p>
                            <p><strong>Patient Responsibility:</strong> $${auth.patient_responsibility.toFixed(2)}</p>
                        </div>
                    `;
                }
                
                // Staffing Prediction
                if (data.staffing_prediction) {
                    const staffing = data.staffing_prediction;
                    html += `
                        <div class="result-section">
                            <h3>✅ Step 4: Staffing Prediction <span class="status-badge status-info">${staffing.status}</span></h3>
                            <p><strong>Current Patients:</strong> ${staffing.current_patient_count}</p>
                            <p><strong>Predicted Nurses:</strong> ${staffing.predicted_nurse_count}</p>
                            <p><strong>Nurse-to-Patient Ratio:</strong> ${staffing.nurse_to_patient_ratio}</p>
                        </div>
                    `;
                }
                
                // Inventory Status
                if (data.inventory_status) {
                    const inventory = data.inventory_status;
                    const statusClass = inventory.status === 'adequate' ? 'status-success' : 'status-warning';
                    html += `
                        <div class="result-section">
                            <h3>✅ Step 5: Inventory Check <span class="status-badge ${statusClass}">${inventory.status.toUpperCase()}</span></h3>
                            <p><strong>Items Checked:</strong> ${inventory.total_items_checked}</p>
                            <p><strong>Items Needing Reorder:</strong> ${inventory.items_needing_reorder}</p>
                            ${inventory.alerts.length > 0 ? '<p><strong>Alerts:</strong></p><ul>' + inventory.alerts.map(a => '<li>' + a + '</li>').join('') + '</ul>' : ''}
                        </div>
                    `;
                }
                
                // Security Monitoring
                if (data.security_monitoring) {
                    const security = data.security_monitoring;
                    const statusClass = security.status === 'secure' ? 'status-success' : 'status-warning';
                    html += `
                        <div class="result-section">
                            <h3>✅ Step 6: Security Monitoring <span class="status-badge ${statusClass}">${security.status.toUpperCase()}</span></h3>
                            <p><strong>Security Score:</strong> ${security.security_score}/100</p>
                            <p><strong>Anomalies Detected:</strong> ${security.anomalies_detected}</p>
                            <p><strong>HIPAA Compliant:</strong> ${security.hipaa_compliant ? 'Yes ✓' : 'No ✗'}</p>
                        </div>
                    `;
                }
                
                resultsDiv.innerHTML = html;
            }
            
            function updateSystemStatus(data) {
                const html = `
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-value">${data.total_steps}</div>
                            <div class="stat-label">Steps Completed</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">${data.security_monitoring?.security_score || 0}</div>
                            <div class="stat-label">Security Score</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">${data.insurance_authorization?.status === 'approved' ? '✓' : '⚠'}</div>
                            <div class="stat-label">Insurance Status</div>
                        </div>
                    </div>
                `;
                systemStatus.innerHTML = html;
            }
        </script>
    </body>
    </html>
    """


@app.post("/workflow")
async def run_workflow(request: WorkflowRequest):
    """Execute complete patient workflow."""
    try:
        result = workflow_orchestrator.execute_patient_workflow(
            patient_name=request.patient_name,
            age=request.age,
            symptoms=request.symptoms,
            insurance=request.insurance,
            consultation_transcript=request.consultation_transcript
        )
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/dashboard")
async def get_dashboard_status():
    """Get system dashboard status."""
    try:
        inventory = supply_chain_agent.check_inventory_status()
        staffing = staffing_prediction_agent.predict_staffing_needs()
        security = cybersecurity_monitoring_agent.monitor_system_activity()
        patients = mcp_server.get_patient_data()
        
        return {
            "status": "success",
            "data": {
                "total_patients": len(patients),
                "inventory_status": inventory["status"],
                "items_needing_reorder": inventory["items_needing_reorder"],
                "staffing_status": staffing["status"],
                "predicted_nurses": staffing["predicted_nurse_count"],
                "security_score": security["security_score"],
                "security_status": security["status"],
                "hipaa_compliant": security["hipaa_compliant"]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    print("\n🚀 Starting Healthcare Agentic System Web Server...")
    print("📍 Open your browser to: http://localhost:8000")
    print("📖 API Documentation: http://localhost:8000/docs\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
