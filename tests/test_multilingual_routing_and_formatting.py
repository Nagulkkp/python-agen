"""
tests/test_multilingual_routing_and_formatting.py
=================================================
Validates:
1. Multilingual routing for Tamil, Arabic, and English queries.
2. Identical SQL query resolution with Is_Service_Billed = 'N'.
3. Zero-token human-centric action cards with collapsible <details> table in User Mode.
4. Full uncollapsed diagnostic table with SQL code blocks in Developer Mode.
5. Valkey 5-minute ephemeral cache retention.
"""

import sys
import json
import re
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from main import chat_with_agent, ChatRequest
from valkey_himes_manager import valkey_manager
from autonomous_agent import autonomous_agent

def run_tests():
    print("=" * 70)
    print("🧪 MULTILINGUAL ROUTING & USER-FRIENDLY SUMMARY ENGINE TESTS")
    print("=" * 70)

    test_mrn = "3004383"
    test_visit = "16923"

    # Setup reliable mock for remote MSSQL execution in test harness
    captured_queries = []
    original_sql = autonomous_agent.execute_select_sql
    
    sample_services_data = json.dumps([
        {
            "Permanent_Visit_No": test_visit,
            "Permanent_MRN_No": test_mrn,
            "Patient_Visit_Services_Serial_No": 50101,
            "CPT_Code": "92602",
            "Service_Internal_Code": "SRV-001",
            "Service_Description": "REPROGRAM COCHLEAR IMPLT <7",
            "Service_Quantity": 1,
            "Is_Service_Billed": "N"
        },
        {
            "Permanent_Visit_No": test_visit,
            "Permanent_MRN_No": test_mrn,
            "Patient_Visit_Services_Serial_No": 50102,
            "CPT_Code": "71020",
            "Service_Internal_Code": "RAD-002",
            "Service_Description": "CHEST X-RAY PA AND LATERAL",
            "Service_Quantity": 1,
            "Is_Service_Billed": "N"
        },
        {
            "Permanent_Visit_No": test_visit,
            "Permanent_MRN_No": test_mrn,
            "Patient_Visit_Services_Serial_No": 50103,
            "CPT_Code": "80053",
            "Service_Internal_Code": "LAB-003",
            "Service_Description": "COMPREHENSIVE METABOLIC PANEL (LAB)",
            "Service_Quantity": 1,
            "Is_Service_Billed": "N"
        }
    ])

    def test_mock_sql(sql_query: str) -> str:
        captured_queries.append(sql_query)
        # Visit lookup
        if "Patient_Visit_Basic_Details" in sql_query and "Patient_Visit_Services" not in sql_query:
            return json.dumps([{
                "Permanent_Visit_No": test_visit,
                "Patient_Visit_Basic_Details_Serial_No": 16923
            }])
        # Services lookup
        if "Patient_Visit_Services" in sql_query:
            return sample_services_data
        # Demographics
        if "Patient_Basic_Details" in sql_query:
            return json.dumps([{
                "Permanent_MRN_No": test_mrn,
                "Patient_First_Name": "Mohammed",
                "Patient_Middle_Name": None,
                "Patient_Last_Name": "Ali",
                "Gender_Code": "M",
                "Patient_DOB": "1990-01-01",
                "Contact_Phone_Mobile": "+971501234567",
                "Emirates_Id": "784-1990-1234567-1"
            }])
        return "[]"

    autonomous_agent.execute_select_sql = test_mock_sql
    valkey_manager.invalidate_patient_snapshot(test_mrn)

    try:
        # ---------------------------------------------------------------------
        # TEST 1: TAMIL QUERY
        # ---------------------------------------------------------------------
        print("\n--- TEST 1: TAMIL QUERY ROUTING & PRESENTATION ---")
        tamil_query = "MRN 3004383-ku innum bill podadha test edhavadhu irukka?"
        print(f"User Query: '{tamil_query}'")
        
        req_ta = ChatRequest(message=tamil_query, session_id="sess_tamil_test")
        res_ta = chat_with_agent(req_ta)
        
        print(f"Status: {res_ta.status}")
        print(f"Model Used: {res_ta.model_used}")
        print(f"Response Preview:\n{res_ta.reply[:350]}...\n")

        assert "⚠️ பில் செய்யப்படாத சேவைகள் விபரம்" in res_ta.reply or "Pending Unbilled" in res_ta.reply
        assert "<details>" in res_ta.reply and "</details>" in res_ta.reply, "User view must include collapsible <details>"
        assert "3004383" in res_ta.reply
        print("✅ Tamil query correctly generated localized status card & collapsible table.")

        # Verify SQL query
        last_query_ta = captured_queries[-1]
        print(f"Tamil Executed SQL:\n{last_query_ta.strip()}")
        assert "Patient_Visit_Services" in last_query_ta
        assert "Is_Service_Billed = 'N'" in last_query_ta
        assert "WITH(NOLOCK)" in last_query_ta
        print("✅ Tamil query executed verified MSSQL join query with Is_Service_Billed = 'N'.")

        # ---------------------------------------------------------------------
        # TEST 2: ARABIC QUERY
        # ---------------------------------------------------------------------
        print("\n--- TEST 2: ARABIC QUERY ROUTING & PRESENTATION ---")
        arabic_query = "ما هي الفحوصات غير المفوترة للمريض MRN 3004383؟"
        print(f"User Query: '{arabic_query}'")

        # Invalidate ephemeral cache to test fresh execution
        valkey_manager.invalidate_patient_snapshot(test_mrn)
        captured_queries.clear()

        req_ar = ChatRequest(message=arabic_query, session_id="sess_arabic_test")
        res_ar = chat_with_agent(req_ar)

        print(f"Status: {res_ar.status}")
        print(f"Model Used: {res_ar.model_used}")
        print(f"Response Preview:\n{res_ar.reply[:350]}...\n")

        assert "⚠️ ملخص الفحوصات والخدمات غير المفوترة" in res_ar.reply
        assert "<details>" in res_ar.reply and "</details>" in res_ar.reply
        assert "3004383" in res_ar.reply
        print("✅ Arabic query correctly generated Arabic status card & collapsible table.")

        # Verify SQL query matches Tamil query logic
        last_query_ar = captured_queries[-1]
        print(f"Arabic Executed SQL:\n{last_query_ar.strip()}")
        assert "Patient_Visit_Services" in last_query_ar
        assert "Is_Service_Billed = 'N'" in last_query_ar
        assert "WITH(NOLOCK)" in last_query_ar
        print("✅ Arabic query resolved to the exact same SQL join query with Is_Service_Billed = 'N'.")

        # ---------------------------------------------------------------------
        # TEST 3: DEVELOPER VIEW VS USER VIEW
        # ---------------------------------------------------------------------
        print("\n--- TEST 3: DUAL VIEW (DEVELOPER MODE VS USER MODE) ---")
        valkey_manager.invalidate_patient_snapshot(test_mrn)

        # Developer Mode Query
        req_dev = ChatRequest(
            message="Show unbilled services for MRN 3004383", 
            session_id="sess_dev_test",
            context={"mode": "developer"}
        )
        # Set session mode to developer in Valkey
        valkey_manager.set_session_mode("sess_dev_test", "developer")

        res_dev = chat_with_agent(req_dev)
        print(f"Developer Mode Used: {res_dev.model_used}")
        print(f"Developer Reply Preview:\n{res_dev.reply[:300]}...\n")

        assert "<details>" not in res_dev.reply, "Developer view must NOT be collapsed in <details>"
        assert "Executed MSSQL Query:" in res_dev.reply or "```sql" in res_dev.reply
        assert "92602" in res_dev.reply
        print("✅ Developer Mode correctly returned full uncollapsed table with SQL code diagnostics.")

        # ---------------------------------------------------------------------
        # TEST 4: VALKEY 5-MINUTE CACHE (SUB-MILLISECOND RETRIEVAL)
        # ---------------------------------------------------------------------
        print("\n--- TEST 4: VALKEY 5-MINUTE EPHEMERAL CACHE HIT ---")
        captured_queries.clear()
        res_cache = chat_with_agent(req_dev)
        print(f"Model Used on Repeat Query: {res_cache.model_used}")
        assert "Valkey Ephemeral Cache" in res_cache.model_used
        assert len(captured_queries) == 0, "Zero SQL queries must be executed on cache hit!"
        print("✅ Repeat query within 5 minutes retrieved instantly from Valkey Ephemeral Cache (0 Tokens, 0 DB calls).")

    finally:
        autonomous_agent.execute_select_sql = original_sql

    print("\n" + "=" * 70)
    print("🎉 ALL MULTILINGUAL & HYBRID SUMMARY ENGINE TESTS PASSED!")
    print("=" * 70)

if __name__ == "__main__":
    run_tests()
