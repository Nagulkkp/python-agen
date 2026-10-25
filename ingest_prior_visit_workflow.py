"""
ingest_prior_visit_workflow.py
==============================
Synchronizes the complete HIMES Senior Architect Prior Visit & Prior Authorization (Pre-Auth)
Specification into ChromaDB (vectorstore) and Valkey (in-memory key-value cache).
"""

import os
import sys
import re
import json

# Ensure stdout handles UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from memory_manager import add_to_knowledge_base
from valkey_himes_manager import valkey_manager

SKILL_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", ".agents", "skills", "prior-visit-workflow", "SKILL.md"))

def parse_and_ingest_prior_visit():
    print("=" * 70)
    print("INGESTING SENIOR ARCHITECT PRIOR VISIT WORKFLOW INTO CHROMADB & VALKEY")
    print("=" * 70)

    if not os.path.exists(SKILL_PATH):
        print(f"Error: Skill file not found at {SKILL_PATH}")
        return

    with open(SKILL_PATH, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    print(f"Loaded SKILL.md ({len(content)} bytes)")

    # 1. Structure key workflow modules for Valkey In-Memory Cache
    pa_modules = {
        "prior_visit_workflow": {
            "title": "HIMES Prior Visit & Prior Authorization (Pre-Auth) System",
            "description": "Senior architect guide covering the 6 entry points, parallel PA database schema, isolated pricing, multi-gateway clearinghouse submission, approval lifecycle, automated expiry cron, and 3 downstream clinical utilization pathways.",
            "rules": [
                "Dedicated Subsystem: Standalone Ingress Portal (/viewPriorVisit/{id?} via PriorVisitController) for external intake vs Global Management Workspace (/globalViewForPriorVisitNew via GlobalViewPriorVisitNewCont) for tracking, observation attachments, and resubmissions.",
                "6 Ingress Creation Pathways: 1) Direct External Patient Registration (Strictly Non-Cash payment only; cash is blocked as pre-auth is solely for Insurance/TPA/Corporate), 2) Clinic Visit Encounter Conversion (services requiring pre-auth linked via PA_Patient_Visit_Basic_Details.Patient_Visit_Basic_Details_Serial_No), 3) Treatment Plan Services (Dental teeth numbers, Derma packages), 4) Physiotherapy Modalities (session counts & tracking), 5) Direct from Appointments (pageFrom='AP' before patient arrives), 6) IPD/Daycare Admission Panel (elective surgical and inpatient approvals).",
                "Parallel Database Architecture: Isolated PA_ prefix tables (PA_Patient_Basic_Details, PA_Patient_Visit_Basic_Details, PA_Patient_Visit_Services, PA_Patient_Visit_Insurance_Service_Cover_Details, PA_Prior_Approval_Log). Adjusting rate, quantity, or patient share in Prior Visit workspace updates ONLY PA tables, strictly isolating clinical and billing ledgers from financial drift.",
                "Multi-Gateway Clearinghouse Engine: Adaptive dispatcher supporting DHA (eClaimLink Dubai - SOAP XML), SHA (Shafafiya Abu Dhabi - SOAP XML), RHA (Riayati MOHAP - REST JSON with Bearer tokens), and Waseel (KSA CCHI - Web Service). Visit-level override via Claim_Gateway falls back to Installation_Parameters.Insurance_Method.",
                "Status State Machine: R=Required (pending submission), I=Applied/In-Progress, A=Approved (Pre-Auth ID issued), J=Partially Approved, D=Denied (with Denial_Code), M=Need More Info (supplemental clinical reports requested), E=Expired/Error, V=Cancelled/Void, C=Completed/Closed.",
                "Automated Expiry Cron: PriorVisitCronController evaluates Applied Date + Validity Days <= Yesterday. Updates status to 'E' (Expired). Clinical Safety Rule: If linked to an unbilled clinic visit, automatically updates Patient_Visit_Services.Patient_Payment_Type_Code = 'CASH' to prevent illegal billing to insurance.",
                "3 Downstream Clinical Pathways: 1) Auto-Reflection (active clinic visit PVISCD updated with Auth ID and approved limits), 2) Transfer to Clinic Visit (transferPriorVisitDetails transforms standalone PA into new clinic visit, MRN, and token), 3) Ingestion into Existing Clinic Visit or Billing (addProirVisitServicetoHimesVisit pulls valid unexpired pre-auths End_Date >= Current_Date into ongoing encounters or billing queue)."
            ]
        },
        "pa_ingress_channels": {
            "title": "HIMES 6 Prior Visit Ingress Channels",
            "channels": {
                "direct_external": "Direct External Registration (/viewPriorVisit): For pre-approval prior to patient arrival. Strictly Non-Cash payment types (Cash blocked). Patient_Visit_Basic_Details_Serial_No is NULL.",
                "clinic_conversion": "Clinic Visit Conversion: Detailed Registration or EMR orders flag services with Prior_Approval_Required_Flag = 'Y'. Linked via Patient_Visit_Basic_Details_Serial_No and Patient_Visit_Services_Serial_No.",
                "treatment_plans": "Treatment Plan Services: Dental charting (Alternate_Teeth_Name, Dental_Teeth_Surface), Ortho/Derma procedures. Stamped Is_Service_Sent_To_PA_Visit = 'Y'.",
                "physiotherapy": "Physiotherapy Modalities: Prescribed session blocks (Total_No_Of_Sessions_Remaining) linked via Physio_Order_Details_Services.",
                "appointments": "Direct Appointments Conversion: Front desk schedules procedure (pageFrom = 'AP'), triggering pre-auth before check-in.",
                "ipd_admission": "IPD Admission Panel: Elective surgeries, room category, and LOS approval via priorToExistingHAModel."
            }
        },
        "pa_clearinghouses": {
            "title": "HIMES Multi-Gateway Clearinghouse Specifications",
            "gateways": {
                "dha": "DHA / eClaimLink (Dubai): SOAP 1.1/1.2 XML to https://www.eClaimLink.ae/UploadTransaction. Injects clinician license, card details, activities, diagnoses, and observations.",
                "sha": "SHA / Shafafiya (Abu Dhabi): DOH Web Services SOAP XML.",
                "rha": "RHA / Riayati (MOHAP UAE): REST JSON API payload (/api/Authorization/PostRequest) with Bearer token authentication.",
                "waseel": "Waseel (KSA CCHI): WSDL Web Services SOAP XML."
            }
        },
        "pa_lifecycle_status": {
            "title": "HIMES Prior Authorization Status Codes & Transitions",
            "statuses": {
                "R": "Required: Pre-auth required, not yet transmitted to payer gateway.",
                "I": "Applied / In-Progress: Dispatched to clearinghouse, awaiting payer adjudication.",
                "A": "Approved: Full approval granted. Prior_Authorization_Id, approved amount and validity days recorded.",
                "J": "Partially Approved: Partial quantity or reduced tariff approved; remainder rejected.",
                "D": "Denied / Rejected: Rejected by payer. Accompanied by official Denial_Code.",
                "M": "Need More Info: Payer requested clinical justification, lab reports, or X-rays.",
                "E": "Expired / Error: Validity lapsed (automated cron) or unrecoverable gateway error.",
                "V": "Cancelled / Void: Pre-auth request formally retracted.",
                "C": "Completed / Closed: Pre-auth consumed by clinical visit and finalized in billing."
            }
        },
        "pa_downstream_egress": {
            "title": "HIMES 3 Downstream Clinical Utilization Pathways",
            "pathways": {
                "auto_reflection": "Auto-Reflection: Pre-auths converted from existing clinic visits automatically update Patient_Visit_Insurance_Service_Cover_Details upon approval.",
                "transfer_to_clinic": "Transfer to Clinic Visit (transferPriorVisitDetails): Converts standalone PA record into live clinic encounter, generating permanent MRN, visit number, and token.",
                "pull_into_billing": "Pull into Visit / Billing (addProirVisitServicetoHimesVisit): Front desk or cashier imports approved services into an ongoing encounter or pending billing queue. Validates End_Date >= Current_Date."
            }
        }
    }

    # 2. Store structured workflow modules in Valkey
    print("\nCaching structured Prior Visit workflows into Valkey...")
    for mod_name, mod_data in pa_modules.items():
        key = f"himes:flow:{mod_name}"
        valkey_manager.cache_himes_flow(mod_name, mod_data, ttl=86400 * 30)
        valkey_manager.set_cached_data(key, mod_data, ttl_seconds=86400 * 30)
        print(f"  ✓ Cached in Valkey: {key}")

    # Also cache under module and topic namespaces
    valkey_manager.cache_himes_flow("prior_authorization", pa_modules["prior_visit_workflow"], ttl=86400 * 30)
    valkey_manager.cache_himes_flow("prior_visit", pa_modules["prior_visit_workflow"], ttl=86400 * 30)
    valkey_manager.set_cached_data("himes:module:prior_visit", pa_modules["prior_visit_workflow"], ttl_seconds=86400 * 30)
    valkey_manager.set_cached_data("himes:module:prior_authorization", pa_modules["prior_visit_workflow"], ttl_seconds=86400 * 30)

    # 3. Prepare rich semantic chunks for ChromaDB
    print("\nChunking SKILL.md for ChromaDB Vector Store...")
    chroma_chunks = []

    # Overview chunk
    chroma_chunks.append({
        "text": f"HIMES Prior Visit & Prior Authorization (Pre-Auth) Architecture Overview:\n\n{content[:2800]}",
        "metadata": {
            "domain": "prior_visit",
            "source": "prior-visit-workflow/SKILL.md",
            "title": "Prior Visit Subsystem Architecture Overview",
            "section": "1. Architectural Overview & Purpose",
            "type": "workflow_overview"
        }
    })

    # Chunk sections by markdown header ##
    sections = re.split(r"\n(?=##\s+)", content)
    for sec in sections:
        sec_clean = sec.strip()
        if len(sec_clean) < 50:
            continue
        h_match = re.search(r"^##\s+(.+)$", sec_clean, re.MULTILINE)
        sec_title = h_match.group(1).strip() if h_match else "Prior Visit Detail"

        # If section is very large (> 2500 chars), sub-chunk by ###
        if len(sec_clean) > 2500 and "\n### " in sec_clean:
            subsections = re.split(r"\n(?=###\s+)", sec_clean)
            for sub in subsections:
                sub_clean = sub.strip()
                if len(sub_clean) < 40:
                    continue
                sub_h = re.search(r"^###\s+(.+)$", sub_clean, re.MULTILINE)
                sub_title = sub_h.group(1).strip() if sub_h else sec_title
                chroma_chunks.append({
                    "text": f"HIMES Prior Visit - {sec_title} - {sub_title}:\n\n{sub_clean}",
                    "metadata": {
                        "domain": "prior_visit",
                        "source": "prior-visit-workflow/SKILL.md",
                        "title": f"Prior Visit - {sec_title}",
                        "section": sub_title,
                        "type": "workflow_sub_section"
                    }
                })
        else:
            chroma_chunks.append({
                "text": f"HIMES Prior Visit - {sec_title}:\n\n{sec_clean}",
                "metadata": {
                    "domain": "prior_visit",
                    "source": "prior-visit-workflow/SKILL.md",
                    "title": f"Prior Visit - {sec_title}",
                    "section": sec_title,
                    "type": "workflow_section"
                }
            })

    print(f"Generated {len(chroma_chunks)} rich semantic chunks.")

    # 4. Ingest into ChromaDB
    try:
        inserted_ids = add_to_knowledge_base(chroma_chunks)
        print(f"  ✓ Successfully indexed {len(inserted_ids)} chunks into ChromaDB agent_knowledge_base!")
    except Exception as e:
        print(f"  ❌ Error indexing into ChromaDB: {e}")

    print("\n" + "=" * 70)
    print("PRIOR VISIT WORKFLOW INGESTION TO VALKEY & CHROMADB COMPLETED SUCCESSFULLY!")
    print("=" * 70)

if __name__ == "__main__":
    parse_and_ingest_prior_visit()
