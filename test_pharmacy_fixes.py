import json
from main import extract_entities_from_text, app
from autonomous_agent import AutonomousAgent

print("--- 1. Testing Entity Extraction ---")
ents1 = extract_entities_from_text("mrn PHAR2120 - intha mrn no ku phamacy and clinic la visit iruka?")
print("Entities from PHAR2120 query:", ents1)
assert ents1.get("mrn") == "PHAR2120", f"Expected PHAR2120, got {ents1.get('mrn')}"

ents2 = extract_entities_from_text("pharmacy module ah paaru")
print("Entities from 'pharmacy module ah paaru':", ents2)
assert ents2.get("visit_no") is None, f"Expected None for visit_no, got {ents2.get('visit_no')}"

ents3 = extract_entities_from_text("visit no 3074 details sollu")
print("Entities from 'visit no 3074':", ents3)
assert ents3.get("visit_no") == "3074", f"Expected 3074, got {ents3.get('visit_no')}"

print("\n--- 2. Testing Database Lookup for PHAR2120 ---")
agent = AutonomousAgent()
q_mrn = """
SELECT 
    p.Pharmacy_Patient_Basic_Details_Serial_No,
    p.Pharmacy_Permanent_MRN_No,
    p.Patient_First_Name,
    p.Patient_Last_Name,
    p.Contact_Phone_Mobile,
    v.Pharmacy_Permanent_Visit_No,
    v.Patient_Visit_Registered_Date_Time,
    h.Permanent_Invoice_No,
    h.Bill_Net_Value
FROM Pharmacy_Patient_Basic_Details p
LEFT JOIN Pharmacy_Patient_Visit_Basic_Details v ON v.Pharmacy_Patient_Basic_Details_Serial_No = p.Pharmacy_Patient_Basic_Details_Serial_No
LEFT JOIN Pharmacy_Patient_Bill_Header h ON h.Pharmacy_Patient_Visit_Basic_Details_Serial_No = v.Pharmacy_Patient_Visit_Basic_Details_Serial_No
WHERE p.Pharmacy_Permanent_MRN_No = 'PHAR2120'
"""
res = agent.execute_select_sql(q_mrn)
print("PHAR2120 Direct DB result:")
print(res)

print("\nALL PRE-CHECKS PASSED!")
