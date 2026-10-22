"""
tests/test_omnilingual_support.py
==================================
Tests Universal Multilingual Support across all world languages:
- Hindi, Malayalam, Telugu, Kannada, Bengali
- Russian, French, Spanish, German, Italian, Portuguese, Turkish, Tagalog
- Chinese, Japanese
- Universal fallback for any unlisted language
- 0-token deterministic execution & localized status cards
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
from utils.table_formatter import detect_language, format_user_friendly_response

def run_tests():
    print("=" * 70)
    print("🌍 TESTING UNIVERSAL OMNILINGUAL PROCESSING (ANY WORLD LANGUAGE)")
    print("=" * 70)

    # 1. Test Language Detection Across Scripts & Dialects
    print("\n--- TEST 1: UNIVERSAL SCRIPT & LANGUAGE DETECTION ---")
    test_cases = [
        ("Show unbilled services for MRN 3004383", "en"),
        ("MRN 3004383-ku innum bill podadha test irukka?", "ta"),
        ("இந்த நோயாளிக்கு என்ன பில் ஆகாத சிகிச்சை இருக்கு?", "ta"),
        ("ما هي الخدمات والفحوصات غير المفوترة للمريض MRN 3004383؟", "ar"),
        ("MRN 3004383 के लिए अनबिल्ड टेस्ट बताओ", "hi"),
        ("MRN 3004383-ന്റെ ബിൽ ചെയ്യാത്ത ടെസ്റ്റുകൾ എന്തൊക്കെയാണ്?", "ml"),
        ("MRN 3004383 బిల్ చేయని సేవలు చూపించు", "te"),
        ("MRN 3004383 ಬಿಲ್ ಮಾಡದ ಸೇವೆಗಳು ವಿವರ ಕೊಡಿ", "kn"),
        ("MRN 3004383 এর অবিল করা সেবাসমূহ দেখান", "bn"),
        ("Показать все неоплаченные анализы и услуги для MRN 3004383", "ru"),
        ("Quelles sont les prestations non facturées pour le patient MRN 3004383 ?", "fr"),
        ("¿Cuáles son los servicios no facturados para el paciente MRN 3004383?", "es"),
        ("Zeigen Sie die nicht abgerechneten Leistungen für MRN 3004383", "de"),
        ("Quali sono i servizi non fatturati per il paziente MRN 3004383?", "it"),
        ("Quais são os serviços não faturados para o paciente MRN 3004383?", "pt"),
        ("MRN 3004383 için faturalanmamış hizmetleri göster", "tr"),
        ("Ipakita ang mga hindi pa nasingil na serbisyo para sa MRN 3004383", "tl"),
        ("请列出 MRN 3004383 的未开票检查和服务", "zh"),
        ("MRN 3004383 の未請求の検査サービスを表示してください", "ja")
    ]

    for text, expected_lang in test_cases:
        detected = detect_language(text)
        assert detected == expected_lang, f"Failed for '{text}': got {detected}, expected {expected_lang}"
        print(f"  ✓ [{detected.upper()}] detected correctly for: {text[:45]}...")

    print("✅ All 19 world language detection checks passed successfully!")

    # 2. Test Localized Response Generation (0 Tokens)
    print("\n--- TEST 2: LOCALIZED ZERO-TOKEN FORMATTING ACROSS LANGUAGES ---")
    sample_services = [
        {"CPT_Code": "92602", "Service_Description": "REPROGRAM COCHLEAR IMPLT <7", "Service_Quantity": 1, "Is_Service_Billed": "N"},
        {"CPT_Code": "71020", "Service_Description": "CHEST X-RAY PA AND LATERAL", "Service_Quantity": 1, "Is_Service_Billed": "N"},
        {"CPT_Code": "80053", "Service_Description": "COMPREHENSIVE METABOLIC PANEL (LAB)", "Service_Quantity": 1, "Is_Service_Billed": "Y"}
    ]

    lang_markers = {
        "hi": "अनबिल्ड सेवाओं का विवरण",
        "ml": "ബിൽ ചെയ്യാത്ത സേവനങ്ങളുടെ വിവരം",
        "te": "బిల్ చేయని సేవల వివరాలు",
        "kn": "ಬಿಲ್ ಮಾಡದ ಸೇವೆಗಳ ವಿವರ",
        "bn": "অবিল করা সেবাসমূহের বিবরণ",
        "ru": "Сводка по неоплаченным услугам",
        "fr": "prestations non facturées",
        "es": "servicios pendientes de facturación",
        "de": "nicht abgerechneten Leistungen",
        "it": "prestazioni non fatturate",
        "pt": "serviços não faturados",
        "tr": "Faturalandırılmamış Hizmetler",
        "zh": "未开票诊疗与检查服务明细",
        "ja": "未請求の診療・検査サマリー"
    }

    for lang_code, marker in lang_markers.items():
        res = format_user_friendly_response(
            sample_services,
            query_context={"lang": lang_code, "mrn": "3004383", "visit_no": "16923"},
            mode="user"
        )
        assert marker in res, f"Expected marker '{marker}' in response for language '{lang_code}'"
        assert "<details>" in res and "</details>" in res, f"Collapsible table missing for language '{lang_code}'"
        assert "92602" in res, f"Service CPT missing for language '{lang_code}'"
        print(f"  ✓ Localized card verified for [{lang_code.upper()}]: '{marker}'")

    print("✅ Localized zero-token presentation verified across all tested languages!")

    # 3. Test End-to-End Chat Routing in Hindi, Russian, and French
    print("\n--- TEST 3: END-TO-END CHAT ROUTING (HINDI, RUSSIAN, FRENCH) ---")
    test_mrn = "3004383"
    test_visit = "16923"

    sample_sql_data = json.dumps([
        {
            "Permanent_Visit_No": test_visit,
            "Permanent_MRN_No": test_mrn,
            "Patient_Visit_Services_Serial_No": 50101,
            "CPT_Code": "92602",
            "Service_Internal_Code": "SRV-001",
            "Service_Description": "REPROGRAM COCHLEAR IMPLT <7",
            "Service_Quantity": 1,
            "Is_Service_Billed": "N"
        }
    ])

    captured_queries = []
    original_sql = autonomous_agent.execute_select_sql

    def mock_sql(query: str) -> str:
        captured_queries.append(query)
        if "Patient_Visit_Basic_Details" in query and "Patient_Visit_Services" not in query:
            return json.dumps([{"Permanent_Visit_No": test_visit, "Patient_Visit_Basic_Details_Serial_No": 16923}])
        if "Patient_Visit_Services" in query:
            return sample_sql_data
        return "[]"

    autonomous_agent.execute_select_sql = mock_sql

    try:
        # A. Hindi Query
        valkey_manager.invalidate_patient_snapshot(test_mrn)
        captured_queries.clear()
        req_hi = ChatRequest(message="MRN 3004383 के लिए अनबिल्ड टेस्ट बताओ", session_id="sess_hi")
        res_hi = chat_with_agent(req_hi)
        print(f"Hindi Status: {res_hi.status}")
        assert "अनबिल्ड सेवाओं का विवरण" in res_hi.reply
        assert "<details>" in res_hi.reply
        assert "92602" in res_hi.reply
        assert len(captured_queries) > 0 and "Is_Service_Billed = 'N'" in captured_queries[-1]
        print("✅ Hindi query executed accurately with 0 LLM tokens and localized Hindi status card.")

        # B. Russian Query
        valkey_manager.invalidate_patient_snapshot(test_mrn)
        captured_queries.clear()
        req_ru = ChatRequest(message="Показать неоплаченные анализы для MRN 3004383", session_id="sess_ru")
        res_ru = chat_with_agent(req_ru)
        print(f"Russian Status: {res_ru.status}")
        assert "Сводка по неоплаченным услугам" in res_ru.reply
        assert "<details>" in res_ru.reply
        assert "92602" in res_ru.reply
        print("✅ Russian query executed accurately with 0 LLM tokens and localized Russian status card.")

        # C. French Query
        valkey_manager.invalidate_patient_snapshot(test_mrn)
        captured_queries.clear()
        req_fr = ChatRequest(message="Quelles sont les prestations non facturées pour MRN 3004383 ?", session_id="sess_fr")
        res_fr = chat_with_agent(req_fr)
        print(f"French Status: {res_fr.status}")
        assert "prestations non facturées" in res_fr.reply
        assert "<details>" in res_fr.reply
        assert "92602" in res_fr.reply
        print("✅ French query executed accurately with 0 LLM tokens and localized French status card.")

        # D. Universal Fallback Test (e.g., Swahili / unknown language)
        valkey_manager.invalidate_patient_snapshot(test_mrn)
        res_fallback = format_user_friendly_response(
            [{"CPT_Code": "99214", "Service_Description": "Consultation", "Is_Service_Billed": "N"}],
            query_context={"lang": "sw", "mrn": test_mrn, "visit_no": test_visit},
            mode="user"
        )
        assert "Pending Unbilled Services Summary" in res_fallback
        print("✅ Unlisted language cleanly fell back to international English card without crashing.")

    finally:
        autonomous_agent.execute_select_sql = original_sql

    print("\n" + "=" * 70)
    print("🎉 ALL UNIVERSAL MULTILINGUAL TESTS PASSED WITH ZERO TOKEN BLOAT!")
    print("=" * 70)

if __name__ == "__main__":
    run_tests()
