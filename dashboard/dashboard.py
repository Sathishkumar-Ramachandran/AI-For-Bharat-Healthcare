"""Streamlit Dashboard for Healthcare Agentic System."""
import streamlit as st
import pandas as pd
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from agents.scribing_agent import clinical_scribing_agent
from agents.diagnosis_agent import diagnosis_agent
from agents.test_recommendation_agent import test_recommendation_agent
from agents.prescription_agent import prescription_agent
from agents.pharmacy_agent import pharmacy_agent
from agents.navigation_agent import navigation_agent
from agents.security_agent import cybersecurity_monitoring_agent
from agents.staffing_agent import staffing_prediction_agent
from agents.insurance_agent import insurance_authorization_agent
from agents.inventory_agent import supply_chain_agent
from services.speech_to_text import speech_to_text_service
from services.mcp_server import mcp_server


# Page configuration
st.set_page_config(
    page_title="Healthcare Agentic System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 10px 20px;
        background-color: white;
        border-radius: 10px;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🏥 Healthcare Agentic System")
st.markdown("**Powered by Amazon Nova + Multi-Agent AI**")

# Create tabs
tab1, tab2, tab3 = st.tabs(["🩺 Treatment Flow", "🏥 Hospital Management", "📊 Patient Data Tracking"])


# TAB 1: Treatment Flow
with tab1:
    st.header("Treatment Flow - Voice-Driven Consultation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Voice Input")
        doctor_input = st.text_area(
            "Doctor Voice Input",
            placeholder="What is your problem?",
            help="Simulated voice input - speak as doctor"
        )
        
        patient_input = st.text_area(
            "Patient Voice Input",
            placeholder="I have had fever for three days",
            help="Simulated voice input - speak as patient"
        )
        
        patient_age = st.number_input("Patient Age", min_value=0, max_value=120, value=35)
        
        if st.button("🎤 Process Consultation", type="primary"):
            if doctor_input and patient_input:
                with st.spinner("Processing consultation..."):
                    # Step 1: Transcribe conversation
                    transcript = speech_to_text_service.transcribe_conversation(
                        doctor_audio=doctor_input,
                        patient_audio=patient_input
                    )
                    
                    # Step 2: Extract symptoms using scribing agent
                    # Create patient data for scribing
                    patient_data = {
                        'age': patient_age,
                        'symptoms': [patient_input],  # Will be extracted by diagnosis agent
                        'patient_id': f"P{hash(patient_input) % 10000:04d}"
                    }
                    
                    scribing_result = clinical_scribing_agent.generate_clinical_notes(
                        patient_name="Patient",
                        transcript=transcript['conversation'],
                        patient_data=patient_data
                    )
                    
                    # Step 3: Diagnose - extract symptoms from patient input
                    # Simple symptom extraction from patient input
                    symptoms = [s.strip() for s in patient_input.lower().replace(',', ' ').split() if len(s.strip()) > 3][:5]
                    if not symptoms:
                        symptoms = ['general complaint']
                    
                    diagnosis_result = diagnosis_agent.analyze_symptoms(symptoms)
                    
                    # Step 4: Recommend tests
                    test_result = test_recommendation_agent.recommend_tests(
                        symptoms,
                        diagnosis_result['primary_diagnosis']
                    )
                    
                    # Step 5: Generate prescription
                    prescription_result = prescription_agent.generate_prescription(
                        diagnosis_result['primary_diagnosis'],
                        symptoms,
                        patient_age
                    )
                    
                    # Step 6: Get navigation instructions
                    test_names = [t['test_name'] for t in test_result['recommended_tests']]
                    nav_result = navigation_agent.get_navigation_instructions(
                        tests=test_names,
                        pharmacy_needed=True
                    )
                    
                    # Generate patient ID
                    patient_id = patient_data['patient_id']
                    
                    # Store in session state
                    st.session_state['treatment_data'] = {
                        'patient_id': patient_id,
                        'symptoms': symptoms,
                        'diagnosis': diagnosis_result,
                        'tests': test_result,
                        'prescription': prescription_result,
                        'scribing': scribing_result,
                        'navigation': nav_result
                    }
                    
                    # Save to database
                    mcp_server.save_patient_record({
                        'patient_id': patient_id,
                        'visit_reason': ', '.join(symptoms),
                        'diagnosis': diagnosis_result['primary_diagnosis'],
                        'tests_taken': ', '.join(test_names),
                        'medicines_prescribed': ', '.join([p['medicine'] for p in prescription_result['prescription_items']]),
                        'doctor_notes': scribing_result.get('notes', 'Clinical assessment completed'),
                        'navigation_instructions': '; '.join(nav_result['step_by_step_directions'])
                    })
                    
                    st.success(f"✅ Consultation processed successfully! Patient ID: {patient_id}")
            else:
                st.error("Please provide both doctor and patient inputs")
    
    with col2:
        st.subheader("Treatment Results")
        
        if 'treatment_data' in st.session_state:
            data = st.session_state['treatment_data']
            
            # Display results in structured format
            st.markdown("### 📋 Clinical Summary")
            
            results_df = pd.DataFrame([{
                'Symptoms': ', '.join(data['symptoms']),
                'Diagnosis': data['diagnosis']['primary_diagnosis'],
                'Confidence': data['diagnosis']['confidence'],
                'Recommended Tests': ', '.join([t['test_name'] for t in data['tests']['recommended_tests']]),
                'Medicines': ', '.join([p['medicine'] for p in data['prescription']['prescription_items']])
            }])
            
            st.dataframe(results_df, use_container_width=True)
            
            # Detailed sections
            with st.expander("🔬 Test Details"):
                tests_df = pd.DataFrame(data['tests']['recommended_tests'])
                st.dataframe(tests_df, use_container_width=True)
            
            with st.expander("💊 Prescription Details"):
                prescription_df = pd.DataFrame(data['prescription']['prescription_items'])
                st.dataframe(prescription_df, use_container_width=True)
            
            with st.expander("🧠 AI Reasoning"):
                st.text_area("Diagnosis Reasoning", data['diagnosis']['reasoning'], height=200)
        else:
            st.info("Process a consultation to see results here")


# TAB 2: Hospital Management
with tab2:
    st.header("Hospital Management Dashboard")
    
    if st.button("🔄 Refresh Dashboard"):
        st.rerun()
    
    # Security Agent
    st.subheader("🔒 Security Monitoring")
    security_data = cybersecurity_monitoring_agent.monitor_system_activity()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Security Score", f"{security_data['security_score']}/100")
    col2.metric("Anomalies", security_data['anomalies_detected'])
    col3.metric("HIPAA Compliant", "✓ Yes" if security_data['hipaa_compliant'] else "✗ No")
    
    # Check for anomalies instead of alerts
    if security_data.get('anomalies') and len(security_data['anomalies']) > 0:
        st.warning("⚠️ Security Anomalies Detected:")
        for anomaly in security_data['anomalies']:
            st.write(f"- {anomaly.get('type', 'Unknown')}: {anomaly.get('user', 'N/A')} (Severity: {anomaly.get('severity', 'N/A')})")
    
    st.divider()
    
    # Staffing Agent
    st.subheader("👥 Staffing Predictions")
    staffing_data = staffing_prediction_agent.predict_staffing_needs()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Current Patients", staffing_data['current_patient_count'])
    col2.metric("Required Nurses", staffing_data['predicted_nurse_count'])
    col3.metric("Nurse-to-Patient Ratio", staffing_data['nurse_to_patient_ratio'])
    
    st.divider()
    
    # Insurance Agent
    st.subheader("💳 Insurance Status")
    st.info("Insurance verification available during patient workflow")
    
    st.divider()
    
    # Inventory Agent
    st.subheader("📦 Medical Inventory")
    inventory_data = supply_chain_agent.check_inventory_status()
    
    col1, col2 = st.columns(2)
    col1.metric("Items Checked", inventory_data['total_items_checked'])
    col2.metric("Items Needing Reorder", inventory_data['items_needing_reorder'])
    
    if inventory_data['alerts']:
        st.warning("⚠️ Inventory Alerts:")
        for alert in inventory_data['alerts']:
            st.write(f"- {alert}")
    
    st.divider()
    
    # Pharmacy Agent
    st.subheader("💊 Pharmacy Status")
    pharmacy_data = pharmacy_agent.get_pharmacy_status()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Medicines", pharmacy_data['total_medicines'])
    col2.metric("Low Stock", pharmacy_data['low_stock_count'])
    col3.metric("Out of Stock", pharmacy_data['out_of_stock_count'])
    
    if pharmacy_data['low_stock_items']:
        with st.expander("📉 Low Stock Items"):
            low_stock_df = pd.DataFrame(pharmacy_data['low_stock_items'])
            st.dataframe(low_stock_df, use_container_width=True)


# TAB 3: Patient Data Tracking
with tab3:
    st.header("Patient Data Tracking - Mobile View")
    
    # Show hint about recent patient ID if available
    if 'treatment_data' in st.session_state and st.session_state['treatment_data'].get('patient_id'):
        recent_patient_id = st.session_state['treatment_data']['patient_id']
        st.info(f"💡 Most recent consultation: Patient ID **{recent_patient_id}**")
    
    patient_id = st.text_input("Enter Patient ID", placeholder="P001 or use recent ID above")
    
    # Quick access button for recent patient
    col1, col2 = st.columns([1, 3])
    with col1:
        view_button = st.button("🔍 View Records", type="primary")
    with col2:
        if 'treatment_data' in st.session_state and st.session_state['treatment_data'].get('patient_id'):
            if st.button("📋 View Recent Patient"):
                patient_id = st.session_state['treatment_data']['patient_id']
                view_button = True
    
    if view_button and patient_id:
        with st.spinner("Retrieving patient records..."):
            # Get patient records
            records = mcp_server.get_patient_records(patient_id)
            
            if records:
                st.success(f"✅ Found {len(records)} record(s) for Patient ID: {patient_id}")
                st.markdown("---")
                
                for idx, record in enumerate(records, 1):
                    with st.expander(f"📋 Visit #{idx} - {record.get('visit_timestamp', 'N/A')}", expanded=(idx==1)):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("### 🏥 Visit Information")
                            st.write("**Reason for Visit:**", record.get('visit_reason', 'N/A'))
                            st.write("**Diagnosis:**", record.get('diagnosis', 'N/A'))
                            st.write("**Tests Performed:**", record.get('tests_taken', 'N/A'))
                        
                        with col2:
                            st.markdown("### 💊 Treatment")
                            st.write("**Medicines Prescribed:**", record.get('medicines_prescribed', 'N/A'))
                            st.write("**Doctor Notes:**", record.get('doctor_notes', 'N/A')[:200] + "..." if len(record.get('doctor_notes', '')) > 200 else record.get('doctor_notes', 'N/A'))
                        
                        # Navigation instructions
                        if record.get('navigation_instructions'):
                            st.markdown("### 🗺️ Hospital Navigation")
                            st.info(record['navigation_instructions'])
                
                # Show current treatment data if available
                if 'treatment_data' in st.session_state and st.session_state['treatment_data'].get('patient_id') == patient_id:
                    st.markdown("---")
                    st.markdown("### 📊 Current Session Details")
                    data = st.session_state['treatment_data']
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Symptoms Analyzed", len(data['symptoms']))
                    col2.metric("Tests Recommended", len(data['tests']['recommended_tests']))
                    col3.metric("Medicines Prescribed", len(data['prescription']['prescription_items']))
            else:
                st.warning(f"⚠️ No records found for Patient ID: {patient_id}")
                st.info("💡 **Tip:** Process a consultation in the **Treatment Flow** tab to create patient records.")
                
                # Show how to create records
                with st.expander("ℹ️ How to create patient records"):
                    st.markdown("""
                    1. Go to the **Treatment Flow** tab
                    2. Enter doctor and patient conversation
                    3. Click **Process Consultation**
                    4. A Patient ID will be generated
                    5. Return here to view the saved records
                    """)
    
    st.divider()
    
    # Department Finder
    st.subheader("🏥 Find Department")
    department = st.selectbox(
        "Select Department",
        ["Laboratory", "Radiology", "Pharmacy", "Cardiology", "Emergency", "Reception", "ICU"]
    )
    
    if st.button("📍 Get Location"):
        dept_info = navigation_agent.get_department_info(department)
        if 'error' not in dept_info:
            st.success(f"**{department}** - {dept_info['full_address']}")
        else:
            st.error(dept_info['error'])


# Sidebar
with st.sidebar:
    st.header("System Information")
    st.write("**Status:** 🟢 Online")
    st.write("**Model:** Amazon Nova")
    st.write("**Version:** 2.0.0")
    
    st.divider()
    
    st.subheader("Quick Stats")
    patients = mcp_server.get_patient_data()
    st.metric("Total Patients", len(patients))
    
    inventory = mcp_server.get_inventory_data()
    st.metric("Inventory Items", len(inventory))
    
    pharmacy_inv = mcp_server.get_pharmacy_inventory()
    st.metric("Pharmacy Items", len(pharmacy_inv))
    
    st.divider()
    
    # Recent patient records from database
    st.subheader("📋 Recent Consultations")
    recent_records = mcp_server.get_patient_records()
    if recent_records:
        st.write(f"**Total Records:** {len(recent_records)}")
        for record in recent_records[:5]:  # Show last 5
            patient_id = record.get('patient_id', 'Unknown')
            timestamp = record.get('visit_timestamp', 'N/A')
            if timestamp != 'N/A':
                # Format timestamp
                try:
                    from datetime import datetime
                    dt = datetime.fromisoformat(timestamp)
                    timestamp = dt.strftime("%m/%d %H:%M")
                except:
                    pass
            st.caption(f"🔹 {patient_id} - {timestamp}")
    else:
        st.info("No consultations yet")
