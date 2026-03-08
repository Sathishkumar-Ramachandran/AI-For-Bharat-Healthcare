"""Test patient tracking data flow."""
from services.mcp_server import mcp_server

print("=" * 60)
print("PATIENT DATA TRACKING TEST")
print("=" * 60)

# Get all patient records
records = mcp_server.get_patient_records()

print(f"\n✓ Total records in database: {len(records)}")

if records:
    print("\nRecent consultations:")
    for idx, record in enumerate(records[:5], 1):
        print(f"\n{idx}. Patient ID: {record['patient_id']}")
        print(f"   Diagnosis: {record['diagnosis']}")
        print(f"   Tests: {record['tests_taken']}")
        print(f"   Medicines: {record['medicines_prescribed']}")
        print(f"   Timestamp: {record['visit_timestamp']}")
else:
    print("\n⚠️  No records found yet.")
    print("💡 Process a consultation in Treatment Flow tab to create records.")

print("\n" + "=" * 60)
print("Test complete!")
print("=" * 60)
