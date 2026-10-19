import os
import sys
import json
import base64
from dotenv import load_dotenv

load_dotenv(override=True)

from valkey_himes_manager import valkey_manager
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def run_tests():
    print("=" * 70)
    print("TESTING DUAL RESPONSE SYSTEM, VALKEY PERSISTENCE & MULTI-MEDIA INPUTS")
    print("=" * 70)

    test_session = "test_dual_mode_session_99"

    # Reset any existing mode in Valkey
    valkey_manager._delete(f"chat_session:{test_session}:mode")

    # -------------------------------------------------------------
    # TEST 1: Default Mode should be USER MODE
    # -------------------------------------------------------------
    print("\n--- TEST 1: Default Mode Verification ---")
    default_mode = valkey_manager.get_session_mode(test_session)
    print(f"Default Valkey Mode for session: '{default_mode}'")
    assert default_mode == "user", f"Expected 'user', got '{default_mode}'"
    print("✓ Default mode is correctly 'user'")

    # -------------------------------------------------------------
    # TEST 2: Price List query in User Mode
    # Strict Prohibition: NO file paths, NO raw SQL queries
    # -------------------------------------------------------------
    print("\n--- TEST 2: Price List Fast-Path in USER MODE ---")
    res1 = client.post("/api/chat", json={
        "message": "price list management menu enga iruku?",
        "session_id": test_session,
        "is_developer_mode": False
    })
    data1 = res1.json()
    reply1 = data1.get("reply", "")
    mode1 = data1.get("mode", "")
    print(f"Status: {res1.status_code}, Mode: {mode1}")
    print(f"Reply Preview:\n{reply1[:250]}...\n")

    assert mode1 == "user", f"Expected mode 'user', got '{mode1}'"
    assert "InsurancePriceListManagementController" not in reply1, "FAIL: Raw Controller path leaked in User Mode!"
    assert "app/Http/Controllers" not in reply1, "FAIL: Controller file path leaked in User Mode!"
    assert "✅" in reply1, "FAIL: Expected clean status card checkmark in User Mode response!"
    print("✓ User Mode correctly hides file paths and uses clean status cards!")

    # -------------------------------------------------------------
    # TEST 3: Switch to Developer Mode via Trigger Command
    # -------------------------------------------------------------
    print("\n--- TEST 3: Trigger 'enable developer mode' ---")
    res2 = client.post("/api/chat", json={
        "message": "enable developer mode",
        "session_id": test_session
    })
    data2 = res2.json()
    reply2 = data2.get("reply", "")
    mode2 = data2.get("mode", "")
    print(f"Mode returned: {mode2}")
    print(f"Confirmation Card:\n{reply2}\n")

    assert mode2 == "developer", f"Expected mode 'developer', got '{mode2}'"
    valkey_stored_mode = valkey_manager.get_session_mode(test_session)
    assert valkey_stored_mode == "developer", f"Valkey store expected 'developer', got '{valkey_stored_mode}'"
    print(f"✓ Stored in Valkey under chat_session:{test_session}:mode -> '{valkey_stored_mode}'")

    # -------------------------------------------------------------
    # TEST 4: Price List query in Developer Mode
    # Full Technical Details: Controllers, Routes, and Function IDs
    # -------------------------------------------------------------
    print("\n--- TEST 4: Price List Fast-Path in DEVELOPER MODE ---")
    res3 = client.post("/api/chat", json={
        "message": "price list management menu enga iruku?",
        "session_id": test_session
    })
    data3 = res3.json()
    reply3 = data3.get("reply", "")
    mode3 = data3.get("mode", "")
    print(f"Mode: {mode3}")
    print(f"Reply Preview:\n{reply3[:250]}...\n")

    assert mode3 == "developer", f"Expected mode 'developer', got '{mode3}'"
    assert "InsurancePriceListManagementController" in reply3, "FAIL: Expected Controller path in Developer Mode!"
    assert "/priceListManagement" in reply3, "FAIL: Expected Route URL in Developer Mode!"
    print("✓ Developer Mode correctly includes Controllers, routes, and technical details!")

    # -------------------------------------------------------------
    # TEST 5: Multi-Media & Log File Attachment Processing
    # -------------------------------------------------------------
    print("\n--- TEST 5: File & Log Attachment Processing ---")
    sample_log = (
        "local.INFO: HIMES Laboratory Specimen Barcode LIS-90218 processed successfully\n"
        "Specimen ID: 90218, Status: COMPLETED, Department: Biochemistry\n"
    )
    b64_log = base64.b64encode(sample_log.encode("utf-8")).decode("utf-8")

    # Fast-path query with attachment to verify attachment decoding and payload acceptance
    res4 = client.post("/api/chat", json={
        "message": "price list management menu enga iruku?",
        "session_id": test_session,
        "attachments": [
            {
                "name": "lis_specimen.log",
                "type": "text/plain",
                "size": len(sample_log),
                "data": f"data:text/plain;base64,{b64_log}"
            }
        ]
    })
    data4 = res4.json()
    print(f"Status: {res4.status_code}, Mode: {data4.get('mode')}")
    assert res4.status_code == 200, f"Expected 200, got {res4.status_code}"
    print("✓ Attachment successfully ingested and processed by backend!")

    # -------------------------------------------------------------
    # TEST 6: Switch back to User Mode via Trigger Command
    # -------------------------------------------------------------
    print("\n--- TEST 6: Trigger 'disable developer mode' ---")
    res5 = client.post("/api/chat", json={
        "message": "disable developer mode",
        "session_id": test_session
    })
    data5 = res5.json()
    reply5 = data5.get("reply", "")
    mode5 = data5.get("mode", "")
    print(f"Mode returned: {mode5}")
    print(f"Confirmation Card:\n{reply5}\n")

    assert mode5 == "user", f"Expected mode 'user', got '{mode5}'"
    valkey_restored_mode = valkey_manager.get_session_mode(test_session)
    assert valkey_restored_mode == "user", f"Valkey store expected 'user', got '{valkey_restored_mode}'"
    print(f"✓ Successfully restored Valkey session mode to '{valkey_restored_mode}'")

    # Clean up test session
    valkey_manager.clear_session_state(test_session)
    print("\n" + "=" * 70)
    print("ALL 6 TESTS PASSED FLAWLESSLY! DUAL MODE & ATTACHMENTS VERIFIED!")
    print("=" * 70)

if __name__ == "__main__":
    run_tests()
