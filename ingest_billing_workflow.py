"""
ingest_billing_workflow.py
==========================
Synchronizes the complete HIMES Senior Architect Billing Workflow Specification
into ChromaDB (vectorstore) and Valkey (in-memory key-value cache).
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

SKILL_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", ".agents", "skills", "billing-workflow", "SKILL.md"))

def parse_and_ingest_billing():
    print("=" * 70)
    print("INGESTING SENIOR ARCHITECT BILLING WORKFLOW INTO CHROMADB & VALKEY")
    print("=" * 70)

    if not os.path.exists(SKILL_PATH):
        print(f"Error: Skill file not found at {SKILL_PATH}")
        return

    with open(SKILL_PATH, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    print(f"Loaded SKILL.md ({len(content)} bytes)")

    # 1. Structure key workflow modules for Valkey In-Memory Cache
    billing_modules = {
        "billing_workflow": {
            "title": "HIMES Patient Billing & Financial Management System",
            "description": "Senior architect guide covering standalone vs registration billing, 3 item pillars, multi-invoice visit model, invoice lifecycle state machine, calculation engine, deposits/short payments, and credit notes.",
            "rules": [
                "Dual Interface: Standalone Billing Screen (/patientBilling/{id?} / PatientBillingGetCont) for cashier desk vs Embedded Registration Billing Tab (/patientRegistration Tab: Bill / RegistrationTabController) for instant walk-in check-in collection.",
                "3 Billing Item Pillars: Services (Patient_Visit_Services), Inventory Items & Pharmacy (Patient_Visit_Drug_Item_Details & Patient_Visit_Inventory_Billing), and IPD Bed Services (Patient_Visit_IPD_Bed_Details).",
                "Multi-Invoice Architecture: Multiple invoices per visit (e.g., 3 services in Invoice #1, remaining 7 stay in Pending Queue Is_Service_Billed = 'N' for Invoice #2). Carry forward unbilled items via Patient_Previous_Visit_Basic_Details_Serial_No.",
                "Invoice Lifecycle & State Machine: Draft/Open (Is_Bill_Finalized = 'N'), Finalized/Closed (Is_Bill_Finalized = 'C' or 'Y', Closed_By_User_Id), Privileged Revert (revertInvoiceInsData resets to 'N'), Claim Posted (Is_Bill_Posted_To_Insurance_Claim = 'Y' permanently sealed), and Cancelled (Bill_Cancellation_Flag = 'Y').",
                "Calculation Pipeline: Gross = Unit Price x Quantity; Row Discount = Gross x (D%/100); Net Before Addl = Gross - Row Discount; Line Additional Discount pro-rated across eligible lines; Copay/Deductible Split based on Insurance_Plan_Department_Cover (CP% and Deductible Cap); VAT/Tax computed on Net and split into Patient Tax and Insurance Tax.",
                "Payment Settlement: Multi-mode collection (Cash, Card, Bank, Online). Deposit Adjustment draws from Patient_Visit_Deposits_Adjusted_Bills / Patient_Deposit_Log. Short payment logged in Short_Payment_Value with mandatory supervisor reason code.",
                "Refunds & Credit Notes: Recalculation excess refunded to cash or wallet deposit via refundamt dialog. Finalized invoice reversals use AddCreditNote() to generate official Credit Notes. Invoice cancellation restores inventory stock via returnallstockfromcustomerQtyforcancelrequest().",
                "UI Customization & ACL: Drag-and-drop column swapping (List_Based_Column_Swapping / User_Based_Column_Swapping). Protected by role privileges in config/functions.php (billhd_add, billhd_edit, billhd_GENERATE CLOSE, billhd_REVERT, billhd_CancelInv, billhd_UtilizeDeposit, etc.)."
            ]
        },
        "billing_pillars": {
            "title": "HIMES 3 Core Billing Item Pillars",
            "pillars": {
                "services": "Patient_Visit_Services: Doctor Consultations, Lab Tests, Radiology, OT Procedures, Health Packages. Status: Is_Service_Billed ('N' -> 'Y'), Is_Service_Fulfilled (SC=Sample Collected, RC=Report Completed), Service_Secondary_Status (E=Excluded, P=Pre-auth, C=Covered).",
                "inventory": "Patient_Visit_Drug_Item_Details & Patient_Visit_Inventory_Billing: Pharmacy medications, surgical consumables, implants. Tracks Stock_Location_Serial_No, Item_Master_Serial_No, Batch_No, Expiry_Date. Reversals via returnstockfromcustomerQty().",
                "bed_management": "Patient_Visit_IPD_Bed_Details: IPD and Daycare admission, hourly/daily room rent, ICU surcharges, nursing and doctor rounds via getBillingBedManagementGrid."
            }
        },
        "billing_multi_invoice": {
            "title": "HIMES Multi-Invoice Architecture & Carry-Forward",
            "description": "One visit encounter can span multiple sequential invoices.",
            "rules": [
                "Partial Billing: Selecting subset of items creates Invoice #1 (pbsrd.Bill_Header_Serial_No). Unselected items remain unbilled (Is_Service_Billed = 'N') in the Pending Queue.",
                "Global Billing Monitor (viewGlobalPatientBilling): Displays Row 1 for Billed Invoices (Permanent_Invoice_No, gross, receipts) and Row 2 for Pending Invoices (unbilled items queue).",
                "Subsequent Billing: Cashier can open Invoice #1 to append items or generate independent Invoice #2.",
                "Prior Visit Unbilled Carry-Forward: getInvoicePendingServices checks Patient_Previous_Visit_Basic_Details_Serial_No and brings historical unbilled items into current invoice without reopening closed books."
            ]
        },
        "billing_state_machine": {
            "title": "HIMES Invoice Lifecycle & Locking State Machine",
            "states": {
                "draft": "Is_Bill_Finalized = 'N', Bill_Cancellation_Flag = 'N'. Fully editable. Add/delete services, adjust price/discounts, update payments.",
                "finalized": "Is_Bill_Finalized = 'C' or 'Y', Closed_By_User_Id != NULL. Locked against standard edits. Official printable Tax/Credit/Cash invoice.",
                "revert": "Privileged Revert: Allowed only if user holds isRevertInvoice and Revert ACL permissions, no active credit note exists (Credit_Note_Flag = 'N'), and claim is not posted.",
                "claim_posted": "Is_Bill_Posted_To_Insurance_Claim = 'Y'. Permanently sealed for DHA/Waseel EDI transmission. Revert and deletion strictly blocked.",
                "cancelled": "Bill_Cancellation_Flag = 'Y'. Supervised cancellation via cancelInvoiceUpdate(). Receipts voided, inventory restored to stock."
            }
        },
        "billing_calculation": {
            "title": "HIMES Tariff, Discount, Co-Pay & VAT Calculation Pipeline",
            "pipeline": [
                "1. Gross Amount = Unit Price * Quantity",
                "2. Row Discount Amount = Gross Amount * (Row_Discount_% / 100). Enforced by User_Wise_Discount_Limit (Min/Max %). Excess requires supervisor discount code.",
                "3. Line Net Before Additional Discount = Gross Amount - Row Discount Amount",
                "4. Line Additional Discount = (Line Net Before Addl / Sum Eligible Net) * Total Additional Invoice Discount",
                "5. Final Line Net Amount = Line Net Before Addl - Line Additional Discount",
                "6. Copay & Deductible Split: Co-Pay % and Deductible Cap from Insurance_Plan_Department_Cover. Calculated Patient Share = MIN(Final Line Net * Copay %, Deductible Cap). Insurance Share = Final Line Net - Calculated Patient Share. Pre-Auth approval limits cap insurance share; excess shifts to patient.",
                "7. VAT / Tax Engine: Tax Rate T%. Patient Tax = Calculated Patient Share * (T% / 100); Insurance Tax = Insurance Share * (T% / 100).",
                "8. Totals: Total Patient Payable = SUM(Patient Share + Patient Tax); Total Insurance Claim = SUM(Insurance Share + Insurance Tax)."
            ]
        },
        "billing_settlements": {
            "title": "HIMES Payment Settlement, Deposits & Short Payments",
            "rules": [
                "Payment Modes: Cash, Card (authorization code, card terminal, last 4 digits), Bank Transfer, Online Voucher.",
                "Deposit Adjustment: Patient advance deposits in Patient_Deposit_Log utilized via reloadDeposit / Patient_Visit_Deposits_Adjusted_Bills. Supports split payments (part deposit, part cash/card).",
                "Short Payment: If patient cannot pay in full and Allow_Short_Payment_In_Billing = 'Y', balance logged in Patient_Bill_Header.Short_Payment_Value with mandatory short_discountCodeModal reason. Deficit tracked in viewGlobalOutstandBilling."
            ]
        },
        "billing_cancellation_refunds": {
            "title": "HIMES Invoice Modification, Excess Refunds & Credit Notes",
            "rules": [
                "Excess Refund Prompt: If editing an open invoice reduces patient share below already collected amount (refundamt > 0), system triggers refund dialog to pay cash or credit internal deposit wallet.",
                "Credit Notes: Finalized invoices use AddCreditNote() to generate official credit notes (Patient_Visit_Credit_Notes), crediting customer balance and reversing accounting ledger.",
                "Cancellation Workflow: InvoiceCancelRequestController -> Supervisor approval in InvoiceWaitingListDetails -> cancelInvoiceUpdate sets Bill_Cancellation_Flag = 'Y', voids receipts, and restores stock via returnallstockfromcustomerQtyforcancelrequest()."
            ]
        }
    }

    # 2. Store all structured workflow modules in Valkey
    print("\nCaching structured billing workflows into Valkey...")
    for mod_name, mod_data in billing_modules.items():
        key = f"himes:flow:{mod_name}"
        valkey_manager.cache_himes_flow(mod_name, mod_data, ttl=86400 * 30)
        valkey_manager.set_cached_data(key, mod_data, ttl_seconds=86400 * 30)
        print(f"  ✓ Cached in Valkey: {key}")

    # Also cache under module namespace
    valkey_manager.cache_himes_flow("patient_billing", billing_modules["billing_workflow"], ttl=86400 * 30)
    valkey_manager.set_cached_data("himes:module:billing", billing_modules["billing_workflow"], ttl_seconds=86400 * 30)

    # 3. Prepare rich semantic chunks for ChromaDB
    print("\nChunking SKILL.md for ChromaDB Vector Store...")
    chroma_chunks = []

    # Overview chunk
    chroma_chunks.append({
        "text": f"HIMES Patient Billing & Financial Management System Overview:\n\n{content[:2800]}",
        "metadata": {
            "domain": "billing",
            "source": "billing-workflow/SKILL.md",
            "title": "Billing System Architecture Overview",
            "section": "1. Architectural Overview & System Entry Points",
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
        sec_title = h_match.group(1).strip() if h_match else "Billing Architecture Detail"

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
                    "text": f"HIMES Billing - {sec_title} - {sub_title}:\n\n{sub_clean}",
                    "metadata": {
                        "domain": "billing",
                        "source": "billing-workflow/SKILL.md",
                        "title": f"Billing - {sec_title}",
                        "section": sub_title,
                        "type": "workflow_sub_section"
                    }
                })
        else:
            chroma_chunks.append({
                "text": f"HIMES Billing - {sec_title}:\n\n{sec_clean}",
                "metadata": {
                    "domain": "billing",
                    "source": "billing-workflow/SKILL.md",
                    "title": f"Billing - {sec_title}",
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
    print("BILLING WORKFLOW INGESTION TO VALKEY & CHROMADB COMPLETED SUCCESSFULLY!")
    print("=" * 70)

if __name__ == "__main__":
    parse_and_ingest_billing()
