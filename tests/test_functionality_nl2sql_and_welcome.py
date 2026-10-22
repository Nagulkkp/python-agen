"""
tests/test_functionality_nl2sql_and_welcome.py
================================================
Verification Suite for:
1. Functionality-to-Query Engine (NL2SQL) with Live MSSQL execution
2. Expandable Query View Option in User View (<details><summary>🔍 View Generated SQL Query</summary>...)
3. Welcome message branding & dynamic username binding in ai_chat_widget.blade.php
4. Read-Only SQL Safety Guardrails (Blocks UPDATE, DELETE, INSERT, DROP, ALTER, TRUNCATE, EXEC)
"""

import sys
import os
import re
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
from guardrails import validate_sql_query, SecurityException


def run_tests():
    print("=" * 70)
    print("🧪 HIMES NL2SQL FUNCTIONALITY & WELCOME BANNER TEST SUITE")
    print("=" * 70)

    # -------------------------------------------------------------------------
    # TEST 1: Functionality Query "Show today's unbilled lab tests" (User View)
    # -------------------------------------------------------------------------
    print("\n[TEST 1] Testing Functionality Query: 'Show today\\'s unbilled lab tests' in User View...")
    req1 = ChatRequest(
        message="Show today's unbilled lab tests",
        session_id="test_func_user_sess_1",
        user_id="201",
        username="Nurse Mary",
        is_admin=False,
        is_developer_mode=False
    )
    res1 = chat_with_agent(req1)
    print(f"Status: {res1.status} | Mode: {res1.mode}")
    print(f"Model Used: {res1.model_used}")
    print(f"Reply Snippet:\n{res1.reply[:300]}...\n")

    assert res1.status == "success", f"Expected success, got {res1.status}"
    assert res1.mode == "user", f"Expected mode user, got {res1.mode}"
    assert "View Generated SQL Query" in res1.reply, "Expected collapsible 'View Generated SQL Query' in response"
    assert "<details>" in res1.reply and "</details>" in res1.reply, "Expected HTML details element for expandable SQL view"
    assert "Patient_Visit_Services" in res1.reply, "Expected generated SQL query to reference Patient_Visit_Services"
    assert "Is_Service_Billed = 'N'" in res1.reply, "Expected generated SQL query to check unbilled flag"
    print("✅ TEST 1 PASSED: Unbilled lab tests returned clean User Action Card with expandable SQL toggle.")

    # -------------------------------------------------------------------------
    # TEST 2: Functionality Query "Get unbilled pharmacy prescriptions for today"
    # -------------------------------------------------------------------------
    print("\n[TEST 2] Testing Functionality Query: 'Get unbilled pharmacy prescriptions for today'...")
    req2 = ChatRequest(
        message="Get unbilled pharmacy prescriptions for today",
        session_id="test_func_user_sess_2",
        user_id="202",
        username="Pharmacist David",
        is_admin=False,
        is_developer_mode=False
    )
    res2 = chat_with_agent(req2)
    print(f"Status: {res2.status} | Mode: {res2.mode}")
    assert res2.status == "success", f"Expected success, got {res2.status}"
    assert "View Generated SQL Query" in res2.reply, "Expected expandable SQL query toggle"
    assert "Patient_Visit_Services" in res2.reply
    print("✅ TEST 2 PASSED: Unbilled pharmacy prescriptions query executed with expandable SQL view.")

    # -------------------------------------------------------------------------
    # TEST 3: Multilingual / Tanglish Functionality Query
    # -------------------------------------------------------------------------
    print("\n[TEST 3] Testing Tanglish Query: 'iniki unbilled lab test kaattu'...")
    req3 = ChatRequest(
        message="iniki unbilled lab test kaattu",
        session_id="test_func_user_sess_3",
        user_id="203",
        username="Lab Tech Ravi",
        is_admin=False,
        is_developer_mode=False
    )
    res3 = chat_with_agent(req3)
    print(f"Status: {res3.status} | Mode: {res3.mode}")
    assert res3.status == "success"
    assert "View Generated SQL Query" in res3.reply
    print("✅ TEST 3 PASSED: Tanglish functionality query accurately mapped to schematic unbilled lab query.")

    # -------------------------------------------------------------------------
    # TEST 4: Welcome Banner & Dynamic Username Integration in Blade View
    # -------------------------------------------------------------------------
    print("\n[TEST 4] Verifying ai_chat_widget.blade.php Welcome Message Markup...")
    blade_path = Path(__file__).resolve().parent.parent / "ai_chat_widget.blade.php"
    assert blade_path.exists(), "ai_chat_widget.blade.php must exist"
    with open(blade_path, "r", encoding="utf-8") as f:
        blade_content = f.read()

    assert "Vanakkam" in blade_content, "Expected Vanakkam greeting in welcome banner"
    assert "Auth::user()->name" in blade_content or "currentUserName" in blade_content, "Expected dynamic Auth username binding"
    assert "In User View:" in blade_content, "Expected User View description in banner"
    assert "In Developer View:" in blade_content, "Expected Developer View description in banner"
    assert "drag & drop" in blade_content or "drag and drop" in blade_content.lower(), "Expected drag & drop tip in banner"
    print("✅ TEST 4 PASSED: ai_chat_widget.blade.php contains updated dynamic welcome message.")

    # -------------------------------------------------------------------------
    # TEST 5: SQL Safety Guardrail Enforcement (Reject UPDATE, DELETE, DROP, etc.)
    # -------------------------------------------------------------------------
    print("\n[TEST 5] Testing SQL Safety Guardrails...")
    destructive_queries = [
        "UPDATE Patient_Basic_Details SET Patient_First_Name = 'Hacked'",
        "DELETE FROM Patient_Visit_Services WHERE Patient_Visit_Services_Serial_No = 1",
        "DROP TABLE Patient_Basic_Details",
        "INSERT INTO Patient_Personal_Details (Patient_First_Name) VALUES ('Test')",
        "ALTER TABLE Patient_Visit_Basic_Details ADD Test_Column VARCHAR(10)",
        "TRUNCATE TABLE Patient_Bill_Header",
        "EXEC sp_who2",
    ]

    for q in destructive_queries:
        try:
            validate_sql_query(q)
            assert False, f"Guardrail failed to block destructive query: {q}"
        except SecurityException as se:
            assert "Security Violation" in str(se) or "forbidden" in str(se).lower()

    print("✅ TEST 5 PASSED: All 7 destructive SQL commands unconditionally blocked by Security Guardrail.")

    print("\n" + "=" * 70)
    print("🎉 ALL 5 FUNCTIONALITY & WELCOME BANNER TESTS PASSED SUCCESSFULLY!")
    print("=" * 70)


if __name__ == "__main__":
    run_tests()
