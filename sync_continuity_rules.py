"""
sync_continuity_rules.py
========================
Saves critical HIMES architecture rules into ChromaDB Vector DB and Valkey:
1. Strict exact matching for MRN and Visit No (No partial matches / No SQL LIKE).
2. Multi-turn chat conversation continuity & entity inheritance across turns.
3. Billing route parameter architecture (/addPatientBilling/{pbdno}/{pvbdno}).
4. Unbilled services schema and query structure.
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from memory_manager import add_to_knowledge_base
from valkey_himes_manager import valkey_manager

def sync_rules():
    rules = [
        {
            "text": (
                "HIMES Strict Exact Matching Rule: Always match MRN (Permanent_MRN_No) and Visit Number (Permanent_Visit_No) "
                "with exact equality (=). NEVER use SQL LIKE, partial substring matches, or fuzzy searches. "
                "Partial matching causes critical patient data crossover and retrieves records belonging to wrong patients."
            ),
            "metadata": {"source": "himes_architecture_rules", "topic": "patient_exact_matching"}
        },
        {
            "text": (
                "HIMES Multi-Turn Chat Continuity & Entity Inheritance Rule: When a user provides an MRN (e.g. MRN: 3004436) "
                "or Visit No in chat, store it in active_entities. If the user subsequently asks follow-up questions such as "
                "'billing details ah share pannu', 'unbilled services', 'intha visit la...' WITHOUT repeating the MRN or Visit No, "
                "the system MUST retrieve and inherit the active MRN and Visit No from previous chat history and session memory."
            ),
            "metadata": {"source": "himes_architecture_rules", "topic": "chat_entity_continuity"}
        },
        {
            "text": (
                "HIMES Billing Route Parameter Architecture: In HIMES URL routes like /addPatientBilling/{pbdno}/{pvbdno} "
                "and /editPatientBilling/{pbdno}/{pvbdno}, the first parameter {pbdno} is Patient_Basic_Details_Serial_No (Patient Master ID), "
                "and the second parameter {pvbdno} is Patient_Visit_Basic_Details_Serial_No (Visit Serial ID). "
                "Never confuse {pbdno} with visit serial number. Use pvbdno to look up Permanent_Visit_No and Permanent_MRN_No."
            ),
            "metadata": {"source": "himes_architecture_rules", "topic": "billing_route_parameters"}
        },
        {
            "text": (
                "HIMES Unbilled Services Architecture: In Patient_Visit_Services table, unbilled services for a visit have "
                "Is_Service_Billed = 'N', Active_Status = 'A', Patient_Visit_Service_Cancellation_Flag = 'N'. "
                "They link via Service_USSDB_Serial_No -> Service_USSDB -> Service table (Service_Description, CPT_Code, Service_Internal_Code)."
            ),
            "metadata": {"source": "himes_architecture_rules", "topic": "unbilled_services"}
        }
    ]

    print("Adding rules to ChromaDB vector knowledge base...")
    doc_ids = add_to_knowledge_base(rules)
    print(f"✅ ChromaDB Added {len(doc_ids)} rules: {doc_ids}")

    print("Caching rules in Valkey in-memory store...")
    for r in rules:
        topic = r["metadata"]["topic"]
        key = f"himes:rule:{topic}"
        valkey_manager._set(key, r["text"], ttl=86400 * 30)
        print(f"✅ Valkey Cached: {key}")

    print("Synchronization of rules completed successfully!")

if __name__ == "__main__":
    sync_rules()
