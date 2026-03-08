"""
Convert Streamlit app to static HTML for Amplify hosting
This creates a static version that calls Lambda functions for backend
"""

import os

# Create static HTML version of the dashboard
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Healthcare Agentic System - Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        h1 { color: #667eea; margin-bottom: 20px; }
        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            border-bottom: 2px solid #eee;
        }
        .tab {
            padding: 15px 30px;
            cursor: pointer;
            border: none;
            background: none;
            font-size: 16px;
            color: #666;
            border-bottom: 3px solid transparent;
        }
        .tab.active {
            color: #667eea;
            border-bottom-color: #667eea;
        }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #333;
        }
        input, textarea, select {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 14px;
        }
        textarea { min-height: 100px; resize: vertical; }
        .btn {
            background: #667eea;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            margin-top: 10px;
        }
        .btn:hover { background: #5568d3; }
        .result {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
            display: none;
        }
        .result.show { display: block; }
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }
        .loading.show { display: block; }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .metric {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin: 10px 0;
            border-left: 4px solid #667eea;
        }
        .metric h3 { color: #667eea; margin-bottom: 10px; }
        .error {
            background: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 8px;
            margin-top: 10px;
            display: none;
        }
        .error.show { display: block; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏥 Healthcare Agentic System</h1>
        
        <div class="tabs">
            <button class="tab active" onclick="showTab('treatment')">Treatment Flow</button>
            <button class="tab" onclick="showTab('management')">Hospital Management</button>
            <button class="tab" onclick="showTab('tracking')">Patient Tracking</button>
        </div>

        <!-- Treatment Flow Tab -->
        <div id="treatment" class="tab-content active">
            <h2>Patient Consultation</h2>
            <form id="treatmentForm" onsubmit="handleTreatment(event)">
                <div class="form-group">
                    <label>Patient ID</label>
                    <input type="text" id="patientId" required placeholder="e.g., P001">
                </div>
                <div class="form-group">
                    <label>Patient Name</label>
                    <input type="text" id="patientName" required placeholder="Enter patient name">
                </div>
                <div class="form-group">
                    <label>Symptoms</label>
                    <textarea id="symptoms" required placeholder="Describe symptoms..."></textarea>
                </div>
                <button type="submit" class="btn">Start Consultation</button>
            </form>
            
            <div class="loading" id="treatmentLoading">
                <div class="spinner"></div>
                <p>Processing consultation...</p>
            </div>
            
            <div class="error" id="treatmentError"></div>
            
            <div class="result" id="treatmentResult"></div>
        </div>

        <!-- Hospital Management Tab -->
        <div id="management" class="tab-content">
            <h2>Hospital Operations Dashboard</h2>
            <button class="btn" onclick="loadManagement()">Refresh Metrics</button>
            
            <div class="loading" id="managementLoading">
                <div class="spinner"></div>
                <p>Loading metrics...</p>
            </div>
            
            <div class="error" id="managementError"></div>
            
            <div id="managementResult"></div>
        </div>

        <!-- Patient Tracking Tab -->
        <div id="tracking" class="tab-content">
            <h2>Patient Records</h2>
            <div class="form-group">
                <label>Search Patient ID</label>
                <input type="text" id="searchPatientId" placeholder="Enter Patient ID">
                <button class="btn" onclick="searchPatient()">Search</button>
            </div>
            
            <div class="loading" id="trackingLoading">
                <div class="spinner"></div>
                <p>Loading records...</p>
            </div>
            
            <div class="error" id="trackingError"></div>
            
            <div id="trackingResult"></div>
        </div>
    </div>

    <script>
        // API Gateway endpoint (will be configured after Lambda deployment)
        const API_ENDPOINT = 'YOUR_API_GATEWAY_URL';

        function showTab(tabName) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            event.target.classList.add('active');
            document.getElementById(tabName).classList.add('active');
        }

        async function handleTreatment(event) {
            event.preventDefault();
            
            const loading = document.getElementById('treatmentLoading');
            const result = document.getElementById('treatmentResult');
            const error = document.getElementById('treatmentError');
            
            loading.classList.add('show');
            result.classList.remove('show');
            error.classList.remove('show');
            
            const data = {
                patient_id: document.getElementById('patientId').value,
                patient_name: document.getElementById('patientName').value,
                symptoms: document.getElementById('symptoms').value
            };
            
            try {
                const response = await fetch(`${API_ENDPOINT}/treatment`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                
                if (!response.ok) throw new Error('API request failed');
                
                const resultData = await response.json();
                
                result.innerHTML = `
                    <h3>Consultation Results</h3>
                    <div class="metric">
                        <h4>Diagnosis</h4>
                        <p>${resultData.diagnosis || 'Processing...'}</p>
                    </div>
                    <div class="metric">
                        <h4>Recommended Tests</h4>
                        <p>${resultData.tests || 'None'}</p>
                    </div>
                    <div class="metric">
                        <h4>Prescription</h4>
                        <p>${resultData.prescription || 'None'}</p>
                    </div>
                    <div class="metric">
                        <h4>Navigation</h4>
                        <p>${resultData.navigation || 'N/A'}</p>
                    </div>
                `;
                result.classList.add('show');
            } catch (err) {
                error.textContent = 'Error: ' + err.message + '. Please ensure Lambda functions are deployed.';
                error.classList.add('show');
            } finally {
                loading.classList.remove('show');
            }
        }

        async function loadManagement() {
            const loading = document.getElementById('managementLoading');
            const result = document.getElementById('managementResult');
            const error = document.getElementById('managementError');
            
            loading.classList.add('show');
            result.innerHTML = '';
            error.classList.remove('show');
            
            try {
                const response = await fetch(`${API_ENDPOINT}/management`);
                if (!response.ok) throw new Error('API request failed');
                
                const data = await response.json();
                
                result.innerHTML = `
                    <div class="metric">
                        <h3>Staffing Prediction</h3>
                        <p>Recommended Staff: ${data.staffing || 'N/A'}</p>
                    </div>
                    <div class="metric">
                        <h3>Inventory Status</h3>
                        <p>${data.inventory || 'N/A'}</p>
                    </div>
                    <div class="metric">
                        <h3>Security Alerts</h3>
                        <p>${data.security || 'No alerts'}</p>
                    </div>
                `;
            } catch (err) {
                error.textContent = 'Error: ' + err.message + '. Please ensure Lambda functions are deployed.';
                error.classList.add('show');
            } finally {
                loading.classList.remove('show');
            }
        }

        async function searchPatient() {
            const patientId = document.getElementById('searchPatientId').value;
            if (!patientId) return;
            
            const loading = document.getElementById('trackingLoading');
            const result = document.getElementById('trackingResult');
            const error = document.getElementById('trackingError');
            
            loading.classList.add('show');
            result.innerHTML = '';
            error.classList.remove('show');
            
            try {
                const response = await fetch(`${API_ENDPOINT}/patient/${patientId}`);
                if (!response.ok) throw new Error('Patient not found');
                
                const data = await response.json();
                
                result.innerHTML = `
                    <div class="metric">
                        <h3>Patient: ${data.name}</h3>
                        <p><strong>ID:</strong> ${data.patient_id}</p>
                        <p><strong>Symptoms:</strong> ${data.symptoms}</p>
                        <p><strong>Diagnosis:</strong> ${data.diagnosis}</p>
                        <p><strong>Tests:</strong> ${data.tests}</p>
                        <p><strong>Medicines:</strong> ${data.medicines}</p>
                    </div>
                `;
            } catch (err) {
                error.textContent = 'Error: ' + err.message;
                error.classList.add('show');
            } finally {
                loading.classList.remove('show');
            }
        }
    </script>
</body>
</html>
"""

# Write the static HTML
with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✓ Static dashboard created: dashboard.html")
print("✓ Next: Deploy Lambda functions and update API_ENDPOINT")
