"""
tests/test_patient_privacy_guardrail.py
=======================================
Verification suite for Healthcare Patient Data Privacy (PHI) & Real-time Live DB Guardrail.
Guarantees:
1. Zero Patient PII/PHI stored into ChromaDB cache_collection.
2. Patient and visit-specific queries ALWAYS bypass cache and query live MSSQL DB.
3. Static organizational / menu / SOP questions can still be safely cached.
"""

import sys
from pathlib import Path

# Ensure UTF-8 stdout on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from semantic_cache import (
    is_patient_or_phi_data,
    check_semantic_cache,
    save_to_semantic_cache,
    purge_patient_phi_from_cache,
    cache_collection
)

def test_phi_detection():
    print("\n--- TEST 1: PHI & PATIENT ENTITY DETECTION ---")
    
    # 1. Patient MRN Queries -> MUST BE TRUE
    assert is_patient_or_phi_data("MRN 3004383 patient name enna?") == True
    assert is_patient_or_phi_data("Patient 3004389 vitals check pannu") == True
    assert is_patient_or_phi_data("visit no 16923 unbilled services list") == True
    assert is_patient_or_phi_data("check lab orders for MRN 3004383") == True
    assert is_patient_or_phi_data("What medications were prescribed for visit 16915?") == True
    print("✅ All patient-specific queries correctly detected as PHI (True).")

    # 2. General / Menu / System Queries -> MUST BE FALSE
    assert is_patient_or_phi_data("Where is the price list management menu located?") == False
    assert is_patient_or_phi_data("What tube top color is used for CBC test?") == False
    assert is_patient_or_phi_data("Explain LIS laboratory workflow and sample accession") == False
    assert is_patient_or_phi_data("How does antibiotic stewardship timeout work?") == False
    print("✅ General system, menu, and SOP queries correctly allowed as non-PHI (False).")

def test_cache_block_and_bypass():
    print("\n--- TEST 2: CACHE BLOCK AND BYPASS VERIFICATION ---")
    
    patient_query = "MRN 9999999 patient details enna?"
    patient_answer = "Patient Name: Test Patient, MRN: 9999999, Visit No: 88888"

    # Attempt to save patient data to cache
    save_result = save_to_semantic_cache(patient_query, patient_answer)
    assert save_result is None, "save_to_semantic_cache MUST return None (blocked) for patient PHI!"
    print("✅ save_to_semantic_cache successfully blocked storing patient PHI.")

    # Attempt to check cache for patient data
    check_result = check_semantic_cache(patient_query)
    assert check_result is None, "check_semantic_cache MUST return None (bypassed) for patient query!"
    print("✅ check_semantic_cache successfully bypassed cache for patient query to force live DB lookup.")

def test_static_caching_still_works():
    print("\n--- TEST 3: STATIC SYSTEM KNOWLEDGE CACHING ---")
    
    system_query = "What is the standard order of draw for vacutainer tubes?"
    system_answer = "Blood Culture -> Light Blue -> Red/Gold SST -> Green -> Lavender EDTA -> Gray."

    # Non-PHI queries can be saved
    saved_id = save_to_semantic_cache(system_query, system_answer)
    assert saved_id is not None, "Non-PHI query should be successfully saved to semantic cache."
    print(f"✅ Non-PHI query successfully saved to cache (ID: {saved_id[:8]}...).")

    # Check that it hits the cache
    hit = check_semantic_cache(system_query, threshold=0.30)
    assert hit is not None, "check_semantic_cache should return cache hit for static non-PHI query!"
    assert "Blood Culture" in hit["answer"]
    print("✅ Non-PHI query successfully retrieved from cache on repeat query.")

    # Clean up test entry
    try:
        cache_collection.delete(ids=[saved_id])
    except Exception:
        pass

if __name__ == "__main__":
    print("=" * 65)
    print("🧪 RUNNING PATIENT DATA PRIVACY & LIVE DB GUARDRAIL TESTS")
    print("=" * 65)
    test_phi_detection()
    test_cache_block_and_bypass()
    test_static_caching_still_works()
    print("\n" + "=" * 65)
    print("🎉 ALL PATIENT PRIVACY & LIVE DB GUARDRAIL TESTS PASSED!")
    print("=" * 65)
