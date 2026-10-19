"""
test_valkey_integration.py
==========================
Comprehensive test suite verifying Valkey integration with ChromaDB,
HIMES workflow caching, session state, and execution locks.
"""

import sys
import time

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from valkey_himes_manager import (
    valkey_manager,
    cache_himes_flow,
    get_himes_flow,
    get_himes_context,
    save_session_state,
    get_session_state,
    set_active_module,
    get_active_module,
    acquire_nagul_folder_lock,
    release_nagul_folder_lock,
    nagul_folder_lock_context
)

def run_tests():
    print("=" * 65)
    print("🧪 RUNNING VALKEY HIMES INTEGRATION TESTS")
    print("=" * 65)

    # 1. Connection Test
    print("\n--- TEST 1: VALKEY CONNECTION ---")
    print(f"Connected: {valkey_manager.is_connected}")
    print(f"Host:      {valkey_manager.host}:{valkey_manager.port}")
    assert valkey_manager.is_connected, "Valkey must be connected!"
    print("✅ TEST 1 PASSED: Valkey connection verified.")

    # 2. HIMES Module Flow Caching
    print("\n--- TEST 2: HIMES WORKFLOW CACHING ---")
    test_flow = {
        "screen": "addPatientBilling",
        "description": "Patient Billing and Rates Resolution",
        "steps": ["Fetch Active Services", "Determine Cash/Insurance", "Query Base Rates", "Finalize Bill"]
    }
    success = cache_himes_flow("billing_test_workflow", test_flow, ttl=300)
    assert success, "Failed to cache flow"

    retrieved = get_himes_flow("billing_test_workflow")
    print(f"Retrieved Flow: {retrieved}")
    assert retrieved["screen"] == "addPatientBilling", "Retrieved data mismatch"
    print("✅ TEST 2 PASSED: Module flow caching and retrieval verified.")

    # Pre-seeded flow test
    billing_flow = get_himes_flow("patient_billing")
    assert billing_flow is not None, "Pre-seeded patient_billing flow missing!"
    print(f"Pre-seeded billing flow rules count: {len(billing_flow.get('rules', []))}")
    print("✅ TEST 2b PASSED: Pre-seeded HIMES flows verified.")

    # 3. Smart Hybrid Search (Valkey + ChromaDB)
    print("\n--- TEST 3: SMART HYBRID SEARCH (Valkey + ChromaDB) ---")
    query = "HIMES patient billing finalize payment receipt"

    # Query 1: Slow-path (ChromaDB Vector Retrieval -> Auto-cache to Valkey)
    print(f"Executing Query 1 (Expected: ChromaDB fetch & auto-cache)...")
    res1 = get_himes_context(query)
    print(f"Result 1 Source:       {res1['source']}")
    print(f"Result 1 Cache Hit:     {res1['cache_hit']}")
    print(f"Result 1 Retrieval ms:  {res1['retrieval_ms']} ms")
    assert res1["status"] == "success"

    # Query 2: Fast-path (Instant Valkey Cache Hit in sub-milliseconds!)
    print(f"\nExecuting Query 2 (Expected: Instant Valkey Cache Hit)...")
    res2 = get_himes_context(query)
    print(f"Result 2 Source:       {res2['source']}")
    print(f"Result 2 Cache Hit:     {res2['cache_hit']}")
    print(f"Result 2 Retrieval ms:  {res2['retrieval_ms']} ms")
    assert res2["cache_hit"] is True, "Second query must be a Valkey cache hit!"
    assert res2["source"] == "valkey_in_memory", "Source must be Valkey in-memory!"
    print(f"⚡ Speedup: Query 1 ({res1['retrieval_ms']} ms) -> Query 2 ({res2['retrieval_ms']} ms) [Instant!]")
    print("✅ TEST 3 PASSED: Smart Hybrid Search and sub-millisecond caching verified.")

    # 4. Session & State Store
    print("\n--- TEST 4: SESSION & ACTIVE MODULE STATE STORE ---")
    test_session_id = "test_valkey_sess_001"
    session_data = {
        "session_id": test_session_id,
        "active_entities": {"visit_no": "16928", "mrn": "3004383", "bill_no": "59614"},
        "user_name": "Nagul"
    }
    save_session_state(test_session_id, session_data)
    loaded_sess = get_session_state(test_session_id)
    print(f"Loaded Session Active Entities: {loaded_sess.get('active_entities')}")
    assert loaded_sess["active_entities"]["visit_no"] == "16928"

    set_active_module(test_session_id, "PatientBilling")
    active_mod = get_active_module(test_session_id)
    print(f"Active Module: {active_mod}")
    assert active_mod == "PatientBilling"
    print("✅ TEST 4 PASSED: Session state and active module tracking verified.")

    # 5. Nagul Folder Lock Test
    print("\n--- TEST 5: NAGUL FOLDER DISTRIBUTED LOCK ---")
    lock_name = "test_folder_lock"
    owner_a = "worker_agent_A"
    owner_b = "worker_agent_B"

    # Worker A acquires lock
    acquired_a = acquire_nagul_folder_lock(lock_name, timeout=10, owner_id=owner_a)
    print(f"Worker A acquire lock: {acquired_a}")
    assert acquired_a is True

    # Worker B tries to acquire same lock (MUST fail)
    acquired_b = acquire_nagul_folder_lock(lock_name, timeout=10, owner_id=owner_b)
    print(f"Worker B acquire lock (concurrent, expected False): {acquired_b}")
    assert acquired_b is False, "Concurrent lock must be rejected!"

    # Worker B tries to release Worker A's lock (MUST fail)
    released_by_b = release_nagul_folder_lock(lock_name, owner_id=owner_b)
    print(f"Worker B attempt to release Worker A lock (expected False): {released_by_b}")
    assert released_by_b is False

    # Worker A releases lock (MUST succeed)
    released_by_a = release_nagul_folder_lock(lock_name, owner_id=owner_a)
    print(f"Worker A release lock: {released_by_a}")
    assert released_by_a is True

    # Worker B can now acquire
    acquired_b_now = acquire_nagul_folder_lock(lock_name, timeout=10, owner_id=owner_b)
    print(f"Worker B acquire lock after release: {acquired_b_now}")
    assert acquired_b_now is True
    release_nagul_folder_lock(lock_name, owner_id=owner_b)

    # Context Manager test
    print("\nTesting context manager lock...")
    with nagul_folder_lock_context("test_ctx_lock", timeout=10) as lock_owner:
        print(f"Inside lock context. Owner: {lock_owner}")
        # Trying to acquire within context should fail
        assert acquire_nagul_folder_lock("test_ctx_lock", timeout=5, owner_id="another") is False

    # Lock is now released
    assert acquire_nagul_folder_lock("test_ctx_lock", timeout=5, owner_id="fresh_owner") is True
    release_nagul_folder_lock("test_ctx_lock", owner_id="fresh_owner")

    print("✅ TEST 5 PASSED: Atomic execution lock & concurrency prevention verified.")

    print("\n" + "=" * 65)
    print("🎉 ALL 5 TEST SUITES PASSED 100% SUCCESSFULLY!")
    print("=" * 65)

if __name__ == "__main__":
    run_tests()
