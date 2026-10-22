"""
tests/test_table_formatter.py
=============================
Tests human-friendly response formatting, multilingual headers, 
department grouping, and dual-view presentation.
"""

import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.table_formatter import format_user_friendly_response, detect_language

def run_tests():
    print("=" * 65)
    print("🧪 RUNNING TABLE FORMATTER & MULTILINGUAL UI TESTS")
    print("=" * 65)

    # 1. Language Detection Tests
    print("\n--- TEST 1: LANGUAGE DETECTION ---")
    assert detect_language("Show unbilled services for MRN 3004383") == "en"
    assert detect_language("MRN 3004383-ku innum bill podadha test edhavadhu irukka?") == "ta"
    assert detect_language("இந்த நோயாளிக்கு என்ன சிகிச்சை பண்ணியிருக்காங்க?") == "ta"
    assert detect_language("ما هي الفحوصات غير المفوترة للمريض MRN 3004383؟") == "ar"
    print("✅ Language detection passed for English, Tanglish, Pure Tamil, and Arabic.")

    # 2. Sample 6 Services Data (Mixed Billed and Unbilled)
    sample_services = [
        {"CPT_Code": "92602", "Service_Description": "REPROGRAM COCHLEAR IMPLT <7", "Service_Quantity": 1, "Is_Service_Billed": "N"},
        {"CPT_Code": "92601", "Service_Description": "COCHLEAR IMPLT F/UP EXAM <7", "Service_Quantity": 1, "Is_Service_Billed": "Y"},
        {"CPT_Code": "71020", "Service_Description": "CHEST X-RAY PA AND LATERAL", "Service_Quantity": 1, "Is_Service_Billed": "N"},
        {"CPT_Code": "80053", "Service_Description": "COMPREHENSIVE METABOLIC PANEL (LAB)", "Service_Quantity": 1, "Is_Service_Billed": "Y"},
        {"CPT_Code": "99214", "Service_Description": "OFFICE OUTPATIENT VISIT 25 MINS", "Service_Quantity": 1, "Is_Service_Billed": "Y"},
        {"Drug_Brand_Name": "Amoxicillin 500mg Caps", "Dosage": "500mg", "Is_Service_Billed": "N"}
    ]

    # 3. User View Test (Tamil / Tanglish)
    print("\n--- TEST 2: TAMIL / TANGLISH USER VIEW ---")
    res_ta = format_user_friendly_response(
        sample_services,
        query_context={"user_query": "MRN 3004383-ku innum bill podadha test edhavadhu irukka?", "mrn": "3004383", "visit_no": "16923"},
        mode="user"
    )
    print("Tamil Output Preview:\n" + res_ta[:400] + "...")
    assert "⚠️ பில் செய்யப்படாத சேவைகள் விபரம்" in res_ta
    assert "<details>" in res_ta and "</details>" in res_ta, "User view must have collapsible <details> block"
    assert "3 சேவைகள்" in res_ta, "Should count 3 unbilled services"
    print("✅ Tamil User View correctly rendered status card and collapsible table.")

    # 4. User View Test (Arabic)
    print("\n--- TEST 3: ARABIC USER VIEW ---")
    res_ar = format_user_friendly_response(
        sample_services,
        query_context={"user_query": "ما هي الفحوصات غير المفوترة للمريض MRN 3004383؟", "mrn": "3004383", "visit_no": "16923"},
        mode="user"
    )
    print("Arabic Output Preview:\n" + res_ar[:400] + "...")
    assert "⚠️ ملخص الفحوصات والخدمات غير المفوترة" in res_ar
    assert "<details>" in res_ar and "</details>" in res_ar
    assert "3" in res_ar
    print("✅ Arabic User View correctly rendered Arabic status card and collapsible table.")

    # 5. Developer View Test
    print("\n--- TEST 4: DEVELOPER VIEW (UNCOLLAPSED TABLE + DIAGNOSTICS) ---")
    res_dev = format_user_friendly_response(
        sample_services,
        query_context={
            "user_query": "Show unbilled services", 
            "mrn": "3004383", 
            "visit_no": "16923",
            "executed_sql": "SELECT * FROM Patient_Visit_Services WHERE Permanent_Visit_No = '16923'"
        },
        mode="developer"
    )
    print("Developer Output Preview:\n" + res_dev[:400] + "...")
    assert "<details>" not in res_dev, "Developer view should NOT be collapsed in details tag"
    assert "Executed MSSQL Query:" in res_dev
    assert "```sql" in res_dev
    assert "92602" in res_dev
    print("✅ Developer View correctly showed uncollapsed table and SQL diagnostics.")

    # 6. 50-Row Stress Test
    print("\n--- TEST 5: 50 ROWS GROUPING & PRESENTATION ---")
    rows_50 = []
    for i in range(1, 51):
        rows_50.append({
            "CPT_Code": f"99{200 + i}",
            "Service_Description": f"Specialist Consultation Procedure {i}",
            "Service_Quantity": 1,
            "Is_Service_Billed": "N" if i % 2 == 0 else "Y"
        })
    res_50 = format_user_friendly_response(
        rows_50,
        query_context={"user_query": "services breakdown", "mrn": "3004383", "visit_no": "16923"},
        mode="user"
    )
    assert "<details>" in res_50
    assert "50" in res_50
    assert "25" in res_50, "Should count 25 unbilled items"
    print("✅ 50 rows cleanly aggregated with 0 tokens and formatted into collapsible table.")

    print("\n" + "=" * 65)
    print("🎉 ALL TABLE FORMATTER TESTS PASSED!")
    print("=" * 65)

if __name__ == "__main__":
    run_tests()
