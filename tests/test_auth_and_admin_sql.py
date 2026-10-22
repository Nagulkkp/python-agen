"""
tests/test_auth_and_admin_sql.py
=================================
Verification Suite for:
1. User Authentication & Role Guards (Admin-Only Developer Mode)
2. User-Isolated LangChain Valkey Session Memory (himes:chat_history:{user_id}:{session_id})
3. Admin-Only Raw SQL Execution Engine with live MSSQL & table formatting
4. Destructive SQL Guardrail Rejection (DROP, DELETE, UPDATE, etc.)
"""

import sys
import json
import time
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
from memory.session_memory import get_session_memory, ValkeySessionMemory
from autonomous_agent import autonomous_agent


def run_tests():
    print("=" * 70)
    print("🧪 HIMES USER AUTH, SESSION ISOLATION & ADMIN SQL TEST SUITE")
    print("=" * 70)

    # -------------------------------------------------------------------------
    # TEST 1: Non-Admin Cannot Activate Developer Mode
    # -------------------------------------------------------------------------
    print("\n[TEST 1] Non-Admin Mode Switch Rejection...")
    req_non_admin_dev = ChatRequest(
        message="enable developer mode",
        session_id="himes_user_101_sess_test",
        user_id="101",
        username="Staff Nurse",
        is_admin=False
    )
    res1 = chat_with_agent(req_non_admin_dev)
    print(f"Status: {res1.status} | Mode: {res1.mode}")
    print(f"Reply: {res1.reply[:120]}...")
    assert res1.status == "forbidden", f"Expected forbidden, got {res1.status}"
    assert res1.mode == "user", f"Expected mode user, got {res1.mode}"
    assert "Access Denied" in res1.reply, "Expected Access Denied in reply"
    print("✅ TEST 1 PASSED: Non-admin correctly blocked from activating Developer Mode.")

    # -------------------------------------------------------------------------
    # TEST 2: Admin Can Successfully Activate Developer Mode
    # -------------------------------------------------------------------------
    print("\n[TEST 2] Admin Mode Switch Success...")
    req_admin_dev = ChatRequest(
        message="enable developer mode",
        session_id="himes_user_999_admin_sess",
        user_id="999",
        username="Nagul Admin",
        is_admin=True
    )
    res2 = chat_with_agent(req_admin_dev)
    print(f"Status: {res2.status} | Mode: {res2.mode}")
    assert res2.status == "success", f"Expected success, got {res2.status}"
    assert res2.mode == "developer", f"Expected mode developer, got {res2.mode}"
    assert "Developer Mode Activated" in res2.reply, "Expected Developer Mode Activated in reply"
    print("✅ TEST 2 PASSED: Admin successfully activated Developer Mode.")

    # -------------------------------------------------------------------------
    # TEST 3: Non-Admin Payload Flag Overridden (Tampering Prevention)
    # -------------------------------------------------------------------------
    print("\n[TEST 3] Non-Admin Payload Tampering Prevention...")
    req_tamper = ChatRequest(
        message="Patient 3004383 status",
        session_id="himes_user_102_sess_tamper",
        user_id="102",
        username="Attendant",
        is_admin=False,
        is_developer_mode=True  # Maliciously attempting to force developer mode
    )
    res3 = chat_with_agent(req_tamper)
    print(f"Status: {res3.status} | Mode: {res3.mode}")
    assert res3.mode == "user", f"Expected non-admin mode to be strictly downgraded to user, got {res3.mode}"
    print("✅ TEST 3 PASSED: Non-admin payload developer flag strictly locked to user mode.")

    # -------------------------------------------------------------------------
    # TEST 4: Non-Admin Cannot Execute Raw SQL Queries
    # -------------------------------------------------------------------------
    print("\n[TEST 4] Non-Admin Raw SQL Rejection...")
    raw_query = "SELECT TOP 5 * FROM Patient_Basic_Details WITH(NOLOCK)"
    req_non_admin_sql = ChatRequest(
        message=raw_query,
        session_id="himes_user_103_sess_sql",
        user_id="103",
        username="Pharmacist",
        is_admin=False
    )
    res4 = chat_with_agent(req_non_admin_sql)
    print(f"Status: {res4.status} | Mode: {res4.mode}")
    assert res4.status == "forbidden", f"Expected forbidden, got {res4.status}"
    assert "Access Denied" in res4.reply, "Expected Access Denied message"
    print("✅ TEST 4 PASSED: Non-admin strictly blocked from raw SQL execution.")

    # -------------------------------------------------------------------------
    # TEST 5: Admin Can Execute Raw SELECT SQL with Live DB & Formatter
    # -------------------------------------------------------------------------
    print("\n[TEST 5] Admin Raw SELECT SQL Live Execution...")
    req_admin_sql = ChatRequest(
        message="SELECT TOP 2 Permanent_MRN_No, Patient_First_Name FROM Patient_Basic_Details WITH(NOLOCK)",
        session_id="himes_user_999_admin_sess",
        user_id="999",
        username="Nagul Admin",
        is_admin=True,
        is_developer_mode=True
    )
    res5 = chat_with_agent(req_admin_sql)
    print(f"Status: {res5.status} | Mode: {res5.mode}")
    print(f"Model Used: {res5.model_used}")
    print(f"Reply Snippet:\n{res5.reply[:300]}...")
    assert res5.status == "success", f"Expected success, got {res5.status}"
    assert res5.mode == "developer", f"Expected developer mode, got {res5.mode}"
    assert "Developer Diagnostics" in res5.reply or "Executed MSSQL Query" in res5.reply
    assert "DB Latency:" in res5.reply, "Expected DB Latency metric in output"
    assert res5.action_executed.get("raw_sql_execution") is True, "Expected raw_sql_execution action"
    print("✅ TEST 5 PASSED: Admin raw SQL executed on live MSSQL with table formatting and DB latency.")

    # -------------------------------------------------------------------------
    # TEST 6: Destructive SQL Guardrail Interception (DROP / DELETE)
    # -------------------------------------------------------------------------
    print("\n[TEST 6] Destructive SQL Guardrail Interception...")
    req_destructive = ChatRequest(
        message="DROP TABLE Patient_Basic_Details",
        session_id="himes_user_999_admin_sess",
        user_id="999",
        username="Nagul Admin",
        is_admin=True,
        is_developer_mode=True
    )
    res6 = chat_with_agent(req_destructive)
    print(f"Status: {res6.status}")
    print(f"Reply: {res6.reply[:150]}...")
    assert res6.status == "blocked_by_guardrails", f"Expected blocked_by_guardrails, got {res6.status}"
    assert "Security Guardrail" in res6.reply or "Security Guardrail" in res6.model_used
    print("✅ TEST 6 PASSED: Destructive SQL immediately blocked by Guardrail before execution.")

    # -------------------------------------------------------------------------
    # TEST 7: User-Isolated Valkey Chat History (LangChain Memory)
    # -------------------------------------------------------------------------
    print("\n[TEST 7] User-Isolated Valkey Chat History Verification...")
    user_a = "user_alpha"
    user_b = "user_beta"
    sess_a = f"himes_user_{user_a}_uuid1"
    sess_b = f"himes_user_{user_b}_uuid2"

    mem_a = get_session_memory(sess_a, user_id=user_a)
    mem_b = get_session_memory(sess_b, user_id=user_b)
    mem_a.clear()
    mem_b.clear()

    # User A talks about Cardiology
    mem_a.add_turn("Who is the chief of cardiology?", "Dr. Smith is the chief of cardiology.")
    # User B talks about Pediatrics
    mem_b.add_turn("Where is the pediatrics ward?", "Pediatrics is on Level 3 East.")

    # Verify keys in Valkey storage
    expected_key_a = f"himes:chat_history:{user_a}:{sess_a}"
    expected_key_b = f"himes:chat_history:{user_b}:{sess_b}"
    assert mem_a._memory_key == expected_key_a, f"Key mismatch: {mem_a._memory_key} vs {expected_key_a}"
    assert mem_b._memory_key == expected_key_b, f"Key mismatch: {mem_b._memory_key} vs {expected_key_b}"

    # Verify history isolation: User A cannot see User B's messages
    hist_a = mem_a.get_history()
    hist_b = mem_b.get_history()
    assert len(hist_a) == 1
    assert len(hist_b) == 1
    assert "cardiology" in hist_a[0]["user"].lower()
    assert "cardiology" not in hist_b[0]["user"].lower()
    assert "pediatrics" in hist_b[0]["user"].lower()
    assert "pediatrics" not in hist_a[0]["user"].lower()

    # Test LangChain Window Memory integration
    lc_mem_a = mem_a.get_langchain_window_memory()
    assert lc_mem_a is not None, "Expected LangChain window memory instance"
    messages = mem_a.get_langchain_messages()
    assert len(messages) == 2, f"Expected 2 messages (1 human, 1 AI), got {len(messages)}"

    # Add 5 more turns to test 5-turn windowing
    for i in range(5):
        mem_a.add_turn(f"Question {i}", f"Answer {i}")
    hist_a_windowed = mem_a.get_history()
    assert len(hist_a_windowed) == 5, f"Expected window size 5, got {len(hist_a_windowed)}"
    assert hist_a_windowed[-1]["user"] == "Question 4"

    # Clean up
    mem_a.clear()
    mem_b.clear()
    print("✅ TEST 7 PASSED: User-isolated Valkey LangChain history correctly separated and windowed.")

    print("\n" + "=" * 70)
    print("🎉 ALL 7 AUTHENTICATION, ISOLATION & ADMIN SQL TESTS PASSED!")
    print("=" * 70)


if __name__ == "__main__":
    run_tests()
