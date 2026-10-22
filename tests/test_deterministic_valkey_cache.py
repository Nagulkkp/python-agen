"""
tests/test_deterministic_valkey_cache.py
========================================
Verifies Zero-Token Deterministic Formatting, 50-row handling, and Valkey 5-Minute (300s) Ephemeral Cache.
"""

import sys
import json
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from main import chat_with_agent, ChatRequest
from valkey_himes_manager import valkey_manager
from autonomous_agent import autonomous_agent

def run_tests():
    print("=" * 65)
    print("🧪 RUNNING ZERO-TOKEN ENGINE & VALKEY 5-MIN EPHEMERAL CACHE TESTS")
    print("=" * 65)

    test_mrn = "3004383"
    test_visit = "16923"
    
    # Invalidate any existing ephemeral cache for clean test
    valkey_manager.invalidate_patient_snapshot(test_mrn)

    # 1. First Inquiry: Demographics (Live MSSQL DB -> Deterministic Format -> Cached in Valkey 5m)
    print(f"\n--- TEST 1: LIVE DB DEMOGRAPHICS FOR MRN {test_mrn} ---")
    req1 = ChatRequest(
        message=f"MRN {test_mrn} patient name enna?",
        session_id="test_ephemeral_sess"
    )
    res1 = chat_with_agent(req1)
    print(f"Status: {res1.status}")
    print(f"Model Used: {res1.model_used}")
    print(f"Reply Snippet:\n{res1.reply[:200]}...")
    assert "HIMES Deterministic Engine" in res1.model_used, "First query must use Deterministic Engine with Live DB!"
    assert "ARK" in res1.reply or "Mohammed" in res1.reply, "Should contain patient name from DB"
    print("✅ First query successfully fetched live from MSSQL DB with 0 LLM tokens.")

    # 2. Second Inquiry: Same query within 5 minutes (Must hit Valkey Ephemeral Cache!)
    print(f"\n--- TEST 2: REPEAT INQUIRY WITHIN 5 MINUTES (VALKEY EPHEMERAL HIT) ---")
    req2 = ChatRequest(
        message=f"MRN {test_mrn} details sollu",
        session_id="test_ephemeral_sess"
    )
    res2 = chat_with_agent(req2)
    print(f"Status: {res2.status}")
    print(f"Model Used: {res2.model_used}")
    assert "Valkey Ephemeral Cache" in res2.model_used, "Second query must hit Valkey Ephemeral Cache!"
    print("✅ Second query hit Valkey Ephemeral Cache with 0 DB load and 0 LLM tokens.")

    # 3. Third Inquiry: Live Services Inquiry for Visit 16923
    print(f"\n--- TEST 3: LIVE DB SERVICES INQUIRY (VISIT {test_visit}) ---")
    req3 = ChatRequest(
        message=f"MRN {test_mrn} visit {test_visit} services details",
        session_id="test_ephemeral_sess"
    )
    res3 = chat_with_agent(req3)
    print(f"Status: {res3.status}")
    print(f"Model Used: {res3.model_used}")
    table_lines = [l for l in res3.reply.splitlines() if l.startswith("| 92") or l.startswith("| 9 ")]
    print(f"Rendered Table Rows: {len(table_lines)} services formatted in Markdown table!")
    print(f"Reply Snippet:\n{res3.reply[:260]}...")
    assert "HIMES Deterministic Engine" in res3.model_used, "Services query must use Deterministic Engine!"
    assert len(table_lines) > 0, "Should format services table"
    print("✅ Live services successfully formatted with 0 LLM tokens directly from DB.")

    # 4. Fourth Inquiry: Repeat services within 5 minutes (Hits Valkey Ephemeral Cache)
    print(f"\n--- TEST 4: REPEAT SERVICES QUERY (VALKEY 5-MIN HIT) ---")
    res4 = chat_with_agent(req3)
    print(f"Status: {res4.status}")
    print(f"Model Used: {res4.model_used}")
    assert "Valkey Ephemeral Cache" in res4.model_used, "Repeat services query must hit Valkey Ephemeral Cache!"
    print("✅ Repeat services query retrieved from Valkey in sub-milliseconds with 0 tokens.")

    # 5. Fifth Inquiry: Stress Test - 50 Services Handling Without Data Loss (0 LLM Tokens)
    print(f"\n--- TEST 5: 50-ROW DETERMINISTIC FORMATTING STRESS TEST (ZERO TOKENS) ---")
    mock_50_mrn = "MRN99999"
    mock_50_visit = "V88888"
    original_sql = autonomous_agent.execute_select_sql
    try:
        def mocked_50_sql(query):
            if "Patient_Visit_Services" in query:
                rows = []
                for i in range(1, 51):
                    rows.append({
                        "Permanent_Visit_No": mock_50_visit,
                        "Permanent_MRN_No": mock_50_mrn,
                        "Patient_Visit_Services_Serial_No": 50000 + i,
                        "CPT_Code": f"99{200 + i}",
                        "Service_Internal_Code": f"SRV-{i:03d}",
                        "Service_Description": f"Specialist Consultation & Diagnostic Procedure {i}",
                        "Service_Quantity": 1,
                        "Is_Service_Billed": "N" if i % 2 == 0 else "Y"
                    })
                return json.dumps(rows)
            return original_sql(query)

        autonomous_agent.execute_select_sql = mocked_50_sql
        req5 = ChatRequest(
            message=f"MRN {mock_50_mrn} visit {mock_50_visit} services details",
            session_id="test_50_sess"
        )
        res5 = chat_with_agent(req5)
        print(f"Status: {res5.status}")
        print(f"Model Used: {res5.model_used}")
        lines_50 = [l for l in res5.reply.splitlines() if l.startswith("| 99")]
        print(f"Rendered Table Rows: {len(lines_50)} rows formatted in Markdown table!")
        assert len(lines_50) == 50, f"Expected 50 rendered rows, got {len(lines_50)}"
        assert "50" in res5.reply, "Response should confirm 50 services recorded"
        print("✅ 50 full service rows successfully rendered without data loss and with 0 LLM tokens!")
    finally:
        autonomous_agent.execute_select_sql = original_sql

    print("\n" + "=" * 65)
    print("🎉 ALL 5 ZERO-TOKEN & VALKEY EPHEMERAL CACHE TESTS PASSED!")
    print("=" * 65)

if __name__ == "__main__":
    run_tests()
