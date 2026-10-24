"""
seed_registration_skill_to_valkey_and_chroma.py
================================================
Loads the complete 12-section HIMES Patient Registration Workflow from SKILL.md into:
1. Valkey In-Memory Cache (RAM sub-millisecond fast-path key: 'himes:flow:registration_workflow')
2. Valkey In-Memory Key ('himes:registration:full_spec')
3. ChromaDB Persistent Vector Collection ('agent_knowledge_base')
"""

import os
import sys
import re
from typing import List, Dict, Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from memory_manager import add_to_knowledge_base
from valkey_himes_manager import valkey_manager

SKILL_FILE = os.path.join(BASE_DIR, ".agents", "skills", "registration-workflow", "SKILL.md")

def parse_and_seed():
    print("=" * 60)
    print("INDEXING FULL REGISTRATION WORKFLOW INTO VALKEY & CHROMADB")
    print("=" * 60)

    if not os.path.exists(SKILL_FILE):
        print(f"Error: {SKILL_FILE} not found!")
        return

    with open(SKILL_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Store Full Document in Valkey
    valkey_manager.set_cached_data("himes:registration:full_spec", content, ttl_seconds=86400 * 30)
    print("  ✓ Stored full document in Valkey under 'himes:registration:full_spec' (30-day TTL)")

    # 2. Update 'himes:flow:registration_workflow'
    flow_data = {
        "module": "registration_workflow",
        "description": "HIMES Patient Registration & Visit Management Architecture",
        "engines": {
            "simple_registration": "Quick Registration (/viewQuickRegistration - DRP) for rapid walk-in / ER triage intake with auto-loaded previous insurance",
            "detailed_registration": "Full 4-tab Enterprise Registration (/patientRegistration) for multi-payer, secondary insurance, inpatient admission, documents"
        },
        "masters_inventory": [
            "Demographics: Patient_Basic_Details, Patient_Basic_Encript_Details, Patient_Basic_Details_Link_Merging, Gender, Nationality",
            "Identifications: Identification_Type, Country_Identification_Type (mandatory_status: MA, MV, MB, NM), Patient_Identification_Details",
            "Organization & Provider: Company, Branch, Department, Speciality_Sub_Department_Branch, Resource_Parent, Resource, Resource_Service",
            "Visit & Clinical: Visit_Encounter_Type (OPD, IPD, DAY, ER), Patient_Visit_Basic_Details, Patient_Visit_Resources (AD, CD, RD), Patient_Visit_Services, Patient_Visit_Admission_Details",
            "Insurance & Copay: Patient_Payment_Types (CSH, INS, CRP, TPA), Insurance_Company, Insurance_Associate_Company, Insurance_Plans, Insurance_Plan_Department_Cover, Insurance_Plan_Copay_Category_Link, Service_Rate_For_Insurance"
        ],
        "provider_roles": {
            "AD": "Attending Doctor - owns EMR caseload and active encounter",
            "CD": "Consulting Doctor - secondary specialist opinion",
            "RD": "Referring Doctor - internal or external referral tracking"
        },
        "copay_and_deductibles": "Insurance_Plan_Department_Cover (Coinsurance %, Copay Amount, Limits, PA Limit) - Cloned into Patient_Visit_Insurance_Plan_Department_Cover at registration to freeze terms",
        "excluded_services": "Insurance_Plan_Excluded_Prior_Approval_Services ('E') or cptckChkboxExc[] override -> 0.00 AED insurance cover, 100% patient share",
        "pre_auth_and_suppression": "Flagged 'P' or rate > PA_Limit_Value triggers pre-auth. If prior approval reference exists, Insurance_Prior_Approval_Status = 'A' is set and resubmission is suppressed",
        "patient_merging": "Reconciles duplicate MRNs via Patient_Basic_Details_Link_Merging, re-links all visits, appointments, bills, and EMR records, retires source MRN with Active_Status = 'D'",
        "service_deletion_restrictions": "Blocked if invoiced (Is_Service_Billed = 'Y'), LIS processing started (SK/TP/RE/TA/PR), RIS study initiated, or visit checked out",
        "edit_lockouts": "Visit locked when checked out (Visit_Is_Checkedout = 'Y'), patient discharged, invoice finalized, or e-claim XML batched for DHA/Waseel"
    }
    valkey_manager.cache_himes_flow("registration_workflow", flow_data, ttl=86400 * 30)
    print("  ✓ Updated 'himes:flow:registration_workflow' in Valkey (30-day TTL)")

    # 3. Chunk Sections into ChromaDB
    sections = re.split(r'\n##\s+', content)
    chroma_docs = []

    # Header / Overview chunk
    header_chunk = sections[0].strip()
    chroma_docs.append({
        "text": header_chunk,
        "metadata": {
            "source": "registration_workflow_skill.md",
            "module": "registration_workflow",
            "section": "Overview & Architecture",
            "type": "registration_architecture"
        }
    })

    for sec in sections[1:]:
        lines = sec.split("\n", 1)
        sec_title = lines[0].strip()
        sec_body = lines[1].strip() if len(lines) > 1 else ""

        full_chunk = f"## {sec_title}\n\n{sec_body}"
        chroma_docs.append({
            "text": full_chunk,
            "metadata": {
                "source": "registration_workflow_skill.md",
                "module": "registration_workflow",
                "section": sec_title[:60],
                "type": "registration_section"
            }
        })

    print(f"\nAdding {len(chroma_docs)} detailed registration workflow sections into ChromaDB...")
    added_ids = add_to_knowledge_base(chroma_docs)
    print(f"  ✓ Successfully indexed {len(added_ids)} registration sections into ChromaDB!")

    print("\n" + "=" * 60)
    print("REGISTRATION INDEXING COMPLETED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    parse_and_seed()
