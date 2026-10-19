"""
sync_chroma_to_valkey.py
========================
Synchronizes all HIMES application knowledge from ChromaDB into Valkey.
Builds a structured, high-speed Key-Value Index in Valkey covering ALL HIMES MODULE FLOWS:

Structured Key Namespaces:
1. himes:module:registration        -> Simple & Detailed Registration flow
2. himes:module:prior_visit         -> pa_ prefix tables & workflows
3. himes:module:prior_authorization -> General PA approval flows & insurance coverage
4. himes:module:pharmacy_pa         -> pharmacy_ prefix tables & prescription authorization
5. himes:module:billing             -> Invoice generation, co-pay calculation & payments
6. himes:module:insurance           -> claim_ prefix tables, batch generation & submission
7. himes:module:emr                 -> EMR, Doctor consultations, Vitals, Diagnoses
8. himes:module:masters             -> System configurations, ICD lists & User permissions

Also indexes individual documents under himes:doc:<id> and creates himes:modules:index.
"""

import os
import sys
import json
import time
import re
from typing import Dict, List, Any

# Ensure stdout handles UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import chromadb
from dotenv import load_dotenv

load_dotenv(override=True)

from valkey_himes_manager import valkey_manager

# ChromaDB storage path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_DIR = os.path.join(BASE_DIR, "chroma_data")
COLLECTION_NAME = "agent_knowledge_base"

# ====================================================================
# HIMES LIFECYCLE MODULE DEFINITIONS & TAXONOMY
# ====================================================================
MODULE_DEFINITIONS = {
    "registration": {
        "namespace": "himes:module:registration",
        "title": "Patient Registration & Encounter Lifecycle",
        "description": "Simple & Detailed Registration flow covering patient demographics, Emirates ID, insurance cards, payment types, and eligibility checks.",
        "primary_tables": [
            "Patient_Basic_Details",
            "Patient_Basic_Encript_Details",
            "Patient_Visit_Basic_Details",
            "Patient_Visit_Insurance_Details",
            "Patient_Payment_Types",
            "Branch_Master"
        ],
        "key_workflows": [
            "Demographics Capture: First Name, Middle Name, Last Name, Gender, DOB, Mobile stored in Patient_Basic_Encript_Details.",
            "Permanent MRN Generation: Auto-incremented or system generated Permanent_MRN_No in Patient_Basic_Details.",
            "Encounter Creation: Active status check (Active_Status = 'A' AND Visit_Cancellation_Flag = 'N') in Patient_Visit_Basic_Details.",
            "Insurance & Policy Validation: Card details, insurance company, PINUG network, and eligibility checks.",
            "Cash vs Insurance Flagging: Sets visit payment type for downstream billing and pharmacy."
        ],
        "match_patterns": [
            r"\bregistr", r"\bdemographic", r"\bpatient_basic_details\b", r"\bpatient_basic_encript_details\b",
            r"\bpatient_visit_basic_details\b", r"\beligibility\b", r"\bemirates_id\b", r"\bmrn\b",
            r"\bencounter\b", r"\bwalkin\b", r"\bappointment\b"
        ]
    },
    "prior_visit": {
        "namespace": "himes:module:prior_visit",
        "title": "Prior Visit Management (pa_ tables)",
        "description": "Prior visit workflows tracking pre-registered, walk-in, and legacy visit encounters using pa_ prefix tables.",
        "primary_tables": [
            "pa_patient_basic_details",
            "pa_patient_Visit_basic_details",
            "pa_insurance_card_detail",
            "pa_patient_visit_insurance_details",
            "pa_patient_visit_services"
        ],
        "key_workflows": [
            "Pre-Registration Intake: Initial capture of patient demographics before clinical admission into pa_patient_basic_details.",
            "Prior Encounter Linking: Linking prior visits to permanent MRN once verified.",
            "Pre-Admission Card Entry: Recording insurance card details in pa_insurance_card_detail for pre-approval.",
            "Service Requisition: Recording planned services in pa_patient_visit_services for verification."
        ],
        "match_patterns": [
            r"\bpa_patient", r"\bpa_insurance", r"\bprior_visit\b", r"\bprior\s+visit\b",
            r"\bpa_patient_visit_basic_details\b", r"\bpa_insurance_card_detail\b"
        ]
    },
    "prior_authorization": {
        "namespace": "himes:module:prior_authorization",
        "title": "Prior Authorization & Clinical Approvals (PA)",
        "description": "General Prior Authorization (PA) approval flows, visit insurance coverage rules, clinical justification, and card details.",
        "primary_tables": [
            "Prior_Authorization_Header",
            "Prior_Authorization_Details",
            "Patient_Visit_Insurance_Details",
            "Insurance_Company",
            "Universal_Code_Values"
        ],
        "key_workflows": [
            "PA Request Generation: Generated for restricted CPT codes or procedures requiring payer approval.",
            "Clinical Justification: Attached doctor diagnosis notes, vitals, and medical reports.",
            "Status Lifecycle: PENDING -> SUBMITTED -> APPROVED / DENIED / QUERY_RAISED.",
            "Approval Authorization Code: Stored and linked to invoice for auto-settlement."
        ],
        "match_patterns": [
            r"\bprior\s*authoriz", r"\bpre\s*authoriz", r"\bpa\s+approval", r"\bpa\s+request",
            r"\bauthoriz", r"\bapproval\s+flow", r"\bpre-approval\b"
        ]
    },
    "pharmacy_pa": {
        "namespace": "himes:module:pharmacy_pa",
        "title": "Pharmacy Prior Authorization & Prescription Coverage",
        "description": "pharmacy_ prefix tables, electronic prescription authorization, drug formulary checks, and medicine coverage limits.",
        "primary_tables": [
            "pharmacy_prescription_details",
            "pharmacy_authorization_header",
            "pharmacy_item_coverage",
            "Stock_Item_Price",
            "Stock_Item_Insurance_Price",
            "Item_Master"
        ],
        "key_workflows": [
            "Doctor E-Prescription: Doctor enters prescribed drugs and dosage via EMR.",
            "Formulary & Co-Pay Verification: System checks if drug is covered under patient insurance policy.",
            "Online Pharmacy PA: High-cost or non-formulary medications trigger electronic pharmacy PA.",
            "Dispensing & Stock Deduction: Approved prescriptions dispensed at pharmacy and inventory deducted."
        ],
        "match_patterns": [
            r"\bpharmacy", r"\bprescription", r"\bdrug\s*cover", r"\bmedicine", r"\bdispens",
            r"\bpharmacy_item\b", r"\bstock_item_price\b", r"\bstock_item_insurance_price\b"
        ]
    },
    "billing": {
        "namespace": "himes:module:billing",
        "title": "Patient Billing, Rates & Invoicing Lifecycle",
        "description": "Invoice generation, co-pay calculation, cash vs insurance tariff rates, credit notes, receipts, and payment updates.",
        "primary_tables": [
            "Patient_Bill_Header",
            "Patient_Bill_Details",
            "Patient_Bill_Header_Payments_Received",
            "Receipts_For_Payments_Received",
            "Patient_Visit_Deposits",
            "Service_Rate_For_Non_Insurance",
            "Service_Rate_For_Insurance"
        ],
        "key_workflows": [
            "Active Services Aggregation: Query Patient_Visit_Services (Cancellation_Flag = 'N' AND Active_Status = 'A').",
            "Rate Resolution: Non-Insurance uses Service_Rate_For_Non_Insurance; Insurance uses Service_Rate_For_Insurance (TOP 1 ... Start_Date <= GETDATE()).",
            "Bill Finalization: Patient_Bill_Header.Is_Bill_Finalized = 'C' indicates finalized bill with Bill_No and Bill_Net_Value.",
            "Receipts Grid: Receipts_For_Payments_Received and pbpr.Bill_Amount_Paid_By_Patient record patient share (UI Receipt No: pbpr.Patient_Bill_Header_Payments_Received_Serial_No).",
            "Deposits: Patient_Visit_Deposits balance adjusted against final bill."
        ],
        "match_patterns": [
            r"\bbill", r"\binvoice", r"\bco-pay", r"\bcredit\s*note", r"\breceipt", r"\btariff",
            r"\bpatient_bill_header\b", r"\bpatient_bill_details\b", r"\bservice_rate", r"\bnet_value\b",
            r"\bdeposit\b", r"\baddpatientbilling\b", r"\beditpatientbilling\b"
        ]
    },
    "insurance": {
        "namespace": "himes:module:insurance",
        "title": "Insurance Claims & E-Claim Submissions (claim_ tables)",
        "description": "claim_ prefix tables, batch generation, ICD diagnosis linking, e-claim XML submissions, remittances, and denials.",
        "primary_tables": [
            "claim_details",
            "claim_detail_icd",
            "claim_details_submitted",
            "claim_batch_header",
            "claim_remittance_advice",
            "Insurance_Company"
        ],
        "key_workflows": [
            "Claim Extraction: Finalized insurance bills queued for billing claims generator.",
            "Diagnosis Mapping: Links each service/medication with ICD-10 diagnosis in claim_detail_icd.",
            "Batch Compilation: Groups claims by Insurance Company into claim_batch_header.",
            "E-Claim Transmission: Submits XML claim files to payer portals (DHPO / Shafafiya / Malaffi).",
            "Remittance Reconciliation: Matches paid amounts vs deductions/denials."
        ],
        "match_patterns": [
            r"\bclaim", r"\beclaim", r"\bclaim_details\b", r"\bclaim_detail_icd\b",
            r"\bclaim_details_submitted\b", r"\bbatch", r"\bremittance", r"\bshafafiya\b",
            r"\bdhpo\b", r"\bdenial\b", r"\badjudicat"
        ]
    },
    "emr": {
        "namespace": "himes:module:emr",
        "title": "Electronic Medical Record (EMR) & Clinical Consultations",
        "description": "Doctor workstation, nurse vitals, chief complaints, clinical examination, ICD-10 diagnoses, orders, and prescriptions.",
        "primary_tables": [
            "Patient_Visit_Doctor_Notes",
            "Patient_Visit_Diagnoses",
            "Patient_Visit_Vitals",
            "Patient_Visit_Prescription_Details",
            "Patient_Visit_Services",
            "ICD10_Master"
        ],
        "key_workflows": [
            "Nurse Triage: Recording Blood Pressure, Heart Rate, Temperature, SpO2 in Patient_Visit_Vitals.",
            "Physician Encounter: Doctor opens EMR Workstation, enters Subjective (Chief Complaint) and Objective findings.",
            "Assessment & Diagnosis: Coded primary and secondary diagnoses mapped from ICD10_Master.",
            "Order Requisition: Doctor orders lab tests, radiology imaging, or therapy procedures.",
            "E-Prescribing: Medication prescription transmitted to pharmacy module."
        ],
        "match_patterns": [
            r"\bemr\b", r"\bclinical\b", r"\bdoctor", r"\bvital", r"\bdiagnos", r"\bconsult",
            r"\btriage\b", r"\bchief_complaint\b", r"\bicd10\b", r"\blab_order\b", r"\bradiology\b"
        ]
    },
    "masters": {
        "namespace": "himes:module:masters",
        "title": "System Master Configurations, ICD & User Permissions",
        "description": "Master data tables, CPT services, ICD-10 catalogs, tariffs, branches, user permissions, and lookups.",
        "primary_tables": [
            "Service",
            "Service_USSDB",
            "ICD10_Master",
            "User_Master",
            "Role_Master",
            "Branch_Master",
            "Insurance_Company",
            "Universal_Code_Values"
        ],
        "key_workflows": [
            "Service Master Setup: CPT Code, description, and internal service code in Service and Service_USSDB.",
            "ICD-10 Master Library: Complete WHO ICD-10 disease classification catalog.",
            "User & Role Management: Role-based access control, branch assignments, and security permissions.",
            "Branch & Facility Setup: Clinics, hospitals, departments, and work stations."
        ],
        "match_patterns": [
            r"\bmaster", r"\bconfigur", r"\brole_master\b", r"\buser_master\b", r"\bbranch_master\b",
            r"\bservice_ussdb\b", r"\buniversal_code_values\b", r"\blookup\b", r"\bpermission\b"
        ]
    }
}


def classify_document_to_modules(doc_text: str, metadata: Dict[str, Any]) -> List[str]:
    """
    Classifies a ChromaDB document text and metadata into one or more
    of the 8 HIMES module keys based on regex patterns and metadata hints.
    """
    matched_modules = []
    text_lower = (doc_text or "").lower()
    meta_str = json.dumps(metadata or {}).lower()
    combined_str = f"{text_lower} {meta_str}"

    for mod_key, mod_info in MODULE_DEFINITIONS.items():
        is_match = False
        for pattern in mod_info["match_patterns"]:
            if re.search(pattern, combined_str, re.IGNORECASE):
                is_match = True
                break
        if is_match:
            matched_modules.append(mod_key)

    # Fallback to masters or billing if not explicitly classified
    if not matched_modules:
        if "table" in combined_str or "sql" in combined_str:
            matched_modules.append("masters")
        else:
            matched_modules.append("billing")

    return matched_modules


def run_chroma_to_valkey_sync():
    print("=" * 70)
    print("🚀 HIMES CHROMA TO VALKEY KNOWLEDGE SYNCHRONIZATION")
    print("=" * 70)

    # 1. Connect to ChromaDB
    print(f"\n1. Connecting to ChromaDB at: {CHROMA_DIR}...")
    if not os.path.exists(CHROMA_DIR):
        print(f"[ERROR] ChromaDB directory not found: {CHROMA_DIR}")
        return

    chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
    try:
        col = chroma_client.get_collection(COLLECTION_NAME)
        total_chroma_docs = col.count()
        print(f"   Connected! Found {total_chroma_docs} documents in collection '{COLLECTION_NAME}'.")
    except Exception as e:
        print(f"[ERROR] Could not load ChromaDB collection: {e}")
        return

    if total_chroma_docs == 0:
        print("[WARNING] ChromaDB collection is empty. Nothing to sync.")
        return

    # 2. Check Valkey connection
    print(f"\n2. Connecting to Valkey instance at {valkey_manager.host}:{valkey_manager.port}...")
    is_live = valkey_manager.is_connected
    backend = "Live Valkey / Redis Server" if is_live else "In-Memory Local Fallback"
    print(f"   Active Backend: {backend}")

    # 3. Retrieve all documents from ChromaDB
    print(f"\n3. Fetching all {total_chroma_docs} documents from ChromaDB...")
    all_records = col.get()
    doc_ids = all_records.get("ids", [])
    documents = all_records.get("documents", [])
    metadatas = all_records.get("metadatas", [])

    print(f"   Successfully fetched {len(doc_ids)} records from ChromaDB.")

    # 4. Prepare structured module buckets
    module_buckets: Dict[str, List[Dict[str, Any]]] = {k: [] for k in MODULE_DEFINITIONS}
    indexed_doc_count = 0

    print(f"\n4. Parsing, classifying, and indexing documents into HIMES modules...")
    for i in range(len(doc_ids)):
        d_id = doc_ids[i]
        d_text = documents[i] if documents and i < len(documents) else ""
        d_meta = metadatas[i] if metadatas and i < len(metadatas) else {}

        # Classify document
        assigned_modules = classify_document_to_modules(d_text, d_meta)

        doc_payload = {
            "id": d_id,
            "section": d_meta.get("section") or d_meta.get("module") or "General",
            "category": d_meta.get("category") or "module_knowledge",
            "snippet": d_text[:250].strip() + ("..." if len(d_text) > 250 else ""),
            "full_text": d_text,
            "metadata": d_meta
        }

        # Store individual document in Valkey under himes:doc:<id>
        valkey_manager._set(f"himes:doc:{d_id}", doc_payload, ttl=604800)  # 7 days
        indexed_doc_count += 1

        # Add to assigned module buckets
        for mod in assigned_modules:
            module_buckets[mod].append(doc_payload)

    # 5. Build and save structured module entries in Valkey
    print(f"\n5. Saving structured HIMES module indexes to Valkey...")
    modules_directory = []

    for mod_key, mod_info in MODULE_DEFINITIONS.items():
        namespace = mod_info["namespace"]
        docs_for_mod = module_buckets[mod_key]

        module_payload = {
            "module_key": mod_key,
            "namespace": namespace,
            "title": mod_info["title"],
            "description": mod_info["description"],
            "primary_tables": mod_info["primary_tables"],
            "key_workflows": mod_info["key_workflows"],
            "document_count": len(docs_for_mod),
            "documents_summary": [
                {"id": d["id"], "section": d["section"], "snippet": d["snippet"]}
                for d in docs_for_mod[:25]  # Top 25 snippets in main payload for instant access
            ],
            "synced_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        # Save to Valkey with 7 days TTL (persistent index)
        valkey_manager._set(namespace, module_payload, ttl=604800)

        # Also cache the workflow under himes:flow:<mod_key> for get_himes_flow()
        valkey_manager.cache_himes_flow(mod_key, {
            "title": mod_info["title"],
            "description": mod_info["description"],
            "tables": mod_info["primary_tables"],
            "workflows": mod_info["key_workflows"],
            "total_knowledge_chunks": len(docs_for_mod)
        }, ttl=604800)

        modules_directory.append({
            "module_key": mod_key,
            "namespace": namespace,
            "title": mod_info["title"],
            "tables_count": len(mod_info["primary_tables"]),
            "docs_matched": len(docs_for_mod)
        })

        print(f"   * [{namespace}] -> {len(docs_for_mod)} docs mapped.")

    # 6. Save Global Index of all modules
    valkey_manager._set("himes:modules:index", {
        "total_modules": len(modules_directory),
        "total_chroma_docs_indexed": indexed_doc_count,
        "modules": modules_directory,
        "last_synced": time.strftime("%Y-%m-%d %H:%M:%S")
    }, ttl=604800)

    # 7. Verification Test
    print("\n6. Verifying Valkey retrieval in sub-milliseconds...")
    t0 = time.perf_counter()
    billing_data = valkey_manager._get("himes:module:billing")
    t1 = time.perf_counter()
    retrieval_ms = (t1 - t0) * 1000.0

    print(f"   Billing Module retrieval from Valkey: {retrieval_ms:.2f} ms!")
    print(f"   Title: {billing_data.get('title') if billing_data else 'None'}")
    print(f"   Document Count in Billing: {billing_data.get('document_count') if billing_data else 0}")

    print("\n" + "=" * 70)
    print("✅ SYNCHRONIZATION COMPLETE! ALL 8 HIMES MODULES INDEXED IN VALKEY!")
    print("=" * 70)


if __name__ == "__main__":
    run_chroma_to_valkey_sync()
