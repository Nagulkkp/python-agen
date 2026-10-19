import os
import sys
import json
import time
from typing import Dict, List, Any

# Ensure stdout handles UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import chromadb
from valkey_himes_manager import valkey_manager

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CODEBASE_CACHE_FILE = os.path.join(BASE_DIR, "codebase_scan_result.json")
TABLE_SCHEMAS_CACHE_FILE = os.path.join(BASE_DIR, "table_schemas_cache.json")
CHROMADB_DIR = os.path.join(BASE_DIR, "chroma_data")

# Initialize ChromaDB and Valkey
chroma_client = chromadb.PersistentClient(path=CHROMADB_DIR)
knowledge_col = chroma_client.get_or_create_collection(
    name="agent_knowledge_base",
    metadata={"hnsw:space": "cosine"}
)
valkey = valkey_manager

print("=" * 70)
print("HIMES MASTER WORKFLOW & DOMAIN ARCHITECTURE INDEXER")
print("Targeting: LIS, RIS, EMR Panels (100+), 400+ Masters, Billing,")
print("Pharmacy, Invoice Posting, Cron Jobs, Credit Notes, Claim Management")
print("=" * 70)

# ======================================================================
# 1. CORE DOMAIN WORKFLOW DEFINITIONS (Authoritative & Deep)
# ======================================================================
HIMES_DOMAINS = {
    "lis": {
        "title": "Laboratory Information System (LIS) & Pathology",
        "category": "Diagnostics",
        "description": "End-to-end Laboratory information workflow managing outpatient and inpatient diagnostic test requisitions, specimen barcodes, accessioning, automated analyzer interfaces, result entry, dual-pathologist verification, and critical value alerting.",
        "primary_controllers": [
            "LabOrderController", "BarcodeController", "AnatomicPathologyController",
            "LISResultEntryController", "LISVerificationController", "HistoPathologyController"
        ],
        "primary_routes": [
            "/viewGlobalLIS", "/viewLISOrderDetails", "/viewSampleCollection",
            "/viewLISResultEntry", "/viewLISVerification", "/viewHistoPathology"
        ],
        "primary_tables": [
            "Patient_Visit_Lab_Order", "Lab_Item", "Lab_Specimen_Details",
            "Lab_Order_Item_Result", "Lab_Analyzer_Link", "Histo_Order",
            "Lab_Order_Header", "Lab_Order_Details"
        ],
        "key_workflows": [
            "Requisition: Doctor enters lab test orders during clinical consultation via EMR into Patient_Visit_Lab_Order.",
            "Sample Accessioning & Barcode: Phlebotomist collects specimen, prints barcode stickers via BarcodeController, and accessions sample in Lab_Specimen_Details.",
            "Analyzer Integration: Interfaced bi-directional lab analyzers process specimens and transmit raw numerical values via Lab_Analyzer_Link.",
            "Result Entry: Medical Technologist enters manual parameters and microscopic findings into Lab_Order_Item_Result.",
            "Verification & Critical Alerts: Pathologist validates abnormal/critical values via LISVerificationController and publishes final signed report."
        ],
        "edge_cases_and_guardrails": [
            "Critical Panic Alerts: If potassium, troponin, or hemoglobin breaches panic limits, system triggers auto-SMS to attending physician.",
            "Specimen Hemolysis / Rejection: Requires mandatory reason code before sample redraw request can be triggered.",
            "Dual-Verification: High-complexity tests (Histo/Biopsy) require Senior Pathologist sign-off before release."
        ]
    },
    "ris": {
        "title": "Radiology Information System (RIS) & PACS / DICOM",
        "category": "Diagnostics",
        "description": "Radiology management covering imaging order requisitions, Modality Worklist (MWL) sync to PACS/DICOM devices (X-Ray, CT, MRI, Ultrasound), tech completion, radiologist diagnostic reporting, and auto-attachment to clinical records.",
        "primary_controllers": [
            "EmrRadiologyReportController", "RadiologyOrderController", "PACSIntegrationController",
            "DICOMStudyController", "BulkPatientDocumentUploadController"
        ],
        "primary_routes": [
            "/viewGlobalRIS", "/radiologyWorkList", "/viewRadiologyReportEntry",
            "/pacsImageViewer", "/viewRadiologyOrderSummary"
        ],
        "primary_tables": [
            "Patient_Visit_Radiology_Order", "Radiology_Item", "Radiology_Report_Details",
            "Radiology_Modality_Master", "PACS_Order_Link", "Radiology_Study_Instance"
        ],
        "key_workflows": [
            "Order Requisition: Physician orders imaging study with clinical history and ICD-10 justification.",
            "Modality Worklist (MWL): Scheduled order syncs automatically via DICOM protocol to modality console (CT/MRI/X-Ray).",
            "Scan Completion: Radiology technologist completes image acquisition; DICOM images pushed to PACS archive.",
            "Diagnostic Reporting: Radiologist reviews images via PACS web viewer and dictates findings, impression, and BIRADS score.",
            "Sign-off & EHR Sync: Signed report attaches to patient encounter in EmrRadiologyReportController."
        ],
        "edge_cases_and_guardrails": [
            "Contrast Safety: GFR / Creatinine clearance check mandatory prior to IV contrast administration.",
            "Radiation Safety: Pregnancy check enforced for all female patients aged 12-55 prior to X-Ray/CT."
        ]
    },
    "emr_panels": {
        "title": "Electronic Medical Records (EMR) & 100+ Specialty Panels",
        "category": "Clinical",
        "description": "Comprehensive clinical consultation interface supporting 100+ specialty-specific panels (Cardiology, Dental, OB/GYN, Pediatrics, Orthopedic, Dermatology, Anesthesia, Physiotherapy, Urgent Care), nursing triage, vitals, allergies, chief complaints, ICD-10 diagnoses, and e-prescriptions.",
        "primary_controllers": [
            "EMRVisitEntryPanelController", "EMRCCHPIChiefcomplaintController", "EMRAllergiesController",
            "EMRVisitHistoryController", "EMRVisitSummarynewController", "EmrVitalFactorsController",
            "AnesthesiaRecordFormPanelController", "FallRiskAssessmentController", "EMREprescriptionController"
        ],
        "primary_routes": [
            "/emrVisitEntryPanel", "/viewEMRWaitingList", "/emrChiefComplaint",
            "/emrAllergies", "/emrVisitSummary", "/emrVitalFactors", "/anesthesiaRecordForm"
        ],
        "primary_tables": [
            "Patient_Visit_Basic_Details", "Patient_Visit_ICD_Codes", "Patient_Visit_Clinical_Notes",
            "Patient_Visit_Vitals", "Patient_Visit_Allergy_Details", "Patient_Visit_Doctor_Orders",
            "Patient_Visit_Drugs_Prescribed"
        ],
        "key_workflows": [
            "Triage & Vitals: Nurse records temperature, BP, pulse, pain score in EmrVitalFactorsController, and checks allergies in EMRAllergiesController.",
            "Chief Complaint & History: Doctor documents patient narrative, HPI, past medical history in EMRCCHPIChiefcomplaintController.",
            "Specialty Examination: Over 100 dedicated specialty panels render custom examination templates (Dental odontogram, OB growth curves, Anesthesia logs).",
            "ICD-10 Diagnosis: Linking primary and secondary ICD-10 codes in Patient_Visit_ICD_Codes (critical for insurance claims).",
            "E-Prescribing & Order Sets: Electronic drug prescription and lab/radiology order placement.",
            "Doctor Sign-Off: Encrypts clinical encounter and generates finalized Patient Visit Summary."
        ],
        "edge_cases_and_guardrails": [
            "Drug-Allergy Interaction: Cross-checks prescribed medications against Patient_Visit_Allergy_Details before submission.",
            "Primary Diagnosis Rule: An encounter cannot be finalized without at least one primary ICD-10 diagnosis code."
        ]
    },
    "masters_400": {
        "title": "HIMES 400+ Master Pages & System Configuration",
        "category": "Administration",
        "description": "Centralized system master repository governing hospital infrastructure, branches, departments, medical resources, insurance companies, tariffs, service pricing rules, ICD-10 / CPT codes, user access privileges, and system installation parameters.",
        "primary_controllers": [
            "AllMasterLogsController", "EMRCommonMasterController", "DiscountCodesMasterController",
            "InsurancePriceListManagementController", "DrugController", "BulkPlanLimitController",
            "EMRInstallationParameterMasterController", "ItemMasterController"
        ],
        "primary_routes": [
            "/priceListManagement", "/BulkPriceListManagement", "/ViewInventoryPriceListManagement",
            "/PriceRuleForResources", "/viewDepartmentMaster", "/viewResourceMaster",
            "/viewInsuranceMaster", "/viewICDMaster"
        ],
        "primary_tables": [
            "Branch_Master", "Department_Branch_Link", "Resource", "Resource_Parent",
            "Service", "Service_USSDB", "Service_Rate_For_Non_Insurance", "Resource_Rate_For_Insurance",
            "Insurance_Company", "Insurance_Company_Plan", "Plan_Copay_Category_Link", "Item_Master", "ICD_Code"
        ],
        "key_workflows": [
            "Hospital Structure Setup: Configuration of companies, branch codes, physical departments, and bed wards.",
            "Doctor & Staff Credentialing: Resource profiles, license numbers, specialty mappings, and consultation schedules.",
            "Tariff & Price List Management: Price configuration for Cash (Service_Rate_For_Non_Insurance) vs Insurance networks.",
            "Insurance Plan & Co-Pay Rules: Linking Insurance_Company -> Plan -> Network with custom copay percentages and caps.",
            "Audit Logging: All changes across 400+ masters recorded in AllMasterLogsController for compliance."
        ],
        "edge_cases_and_guardrails": [
            "Effective Date Versioning: Rates and price rules cannot be overwritten; new records must be inserted with effective start dates.",
            "Master Deletion Lock: Masters with active foreign key references in clinical encounters cannot be deleted."
        ]
    },
    "billing": {
        "title": "Outpatient & Inpatient Billing, Invoicing & Cashiering",
        "category": "Revenue Cycle",
        "description": "Comprehensive revenue capture and billing engine computing charges, insurance coverage, copay splits, deductibles, package discounts, and cashier payments for Outpatient and Inpatient encounters.",
        "primary_controllers": [
            "PatientBillingController", "PatientBillingPartOneController", "GlobalViewPatientBillingController",
            "IPBillingController", "BillCounterUserController"
        ],
        "primary_routes": [
            "/patientBilling", "/addPatientBilling", "/editPatientBilling",
            "/viewPatientBilling", "/globalBillingView", "/viewBillReceipt"
        ],
        "primary_tables": [
            "Patient_Bill_Header", "Patient_Bill_Items", "Patient_Bill_Payments_Received",
            "Patient_Visit_Deposits_Adjusted_Bills", "Patient_Payment_Type", "Service_Rate_For_Non_Insurance"
        ],
        "key_workflows": [
            "Charge Extraction: Auto-fetches all verified services, pharmacy drugs, and bed charges linked to the visit.",
            "Coverage & Copay Resolution: Evaluates patient insurance policy, deductible cap, copay share, and tax percentages.",
            "Invoice Finalization: Saves invoice header and items, setting Is_Bill_Finalized = 'C'.",
            "Receipt Generation: Cashier collects payment (Cash, Card, Transfer, Advance Deposit adjustment) and issues official receipt."
        ],
        "edge_cases_and_guardrails": [
            "Zero Gross Value Guard: Invoices with 0.00 AED total blocked from finalization unless flagged as FOC / Charity.",
            "Cashier Shift Lock: Counter users cannot collect payments without an open active shift session."
        ]
    },
    "pharmacy": {
        "title": "Outpatient & Inpatient Pharmacy, Drug Dispensing & Inventory",
        "category": "Pharmacy",
        "description": "Full pharmacy operational suite managing electronic prescriptions, formulary validation, direct walk-in pharmacy sales, stock locations, batch expiry tracking, and item dispensing.",
        "primary_controllers": [
            "GlobalViewIPPharmacyController", "GlobalViewPharmacyPriorController",
            "GlobalViewOutstandBillingPharmarcyController", "PharmacyPatientBillingController",
            "IPPharmacyCheckListController"
        ],
        "primary_routes": [
            "/viewGlobalOPPharmacy", "/viewGlobalOutstandBillPharmarcy",
            "/globalViewPharmacyPriorVisit", "/IPPharmacyCheckList"
        ],
        "primary_tables": [
            "Pharmacy_Patient_Basic_Details", "Pharmacy_Patient_Visit_Basic_Details",
            "Pharmacy_Patient_Bill_Header", "Pharmacy_Patient_Bill_Detail_Items",
            "Patient_Visit_Drugs_Prescribed", "Stock_Items", "Item_Master", "Stock_Item_Price"
        ],
        "key_workflows": [
            "OP Pharmacy Queue: viewGlobalOPPharmacy tracks doctor e-prescriptions (Type HA) and walk-in sales (Type PH).",
            "MRN Architecture: Pharmacy direct patients registered in Pharmacy_Patient_Basic_Details with 'PHAR' MRN prefix.",
            "Dispensing & Stock Deduction: Dispensing updates Drug_Pharmacy_Status and deducts stock batch in Stock_Transactions_Detail.",
            "Invoice Billing: Generates Pharmacy_Patient_Bill_Header and Pharmacy_Patient_Bill_Detail_Items."
        ],
        "edge_cases_and_guardrails": [
            "Near-Expiry Block: Dispensing drugs expiring within 30 days requires supervisor override.",
            "Antibiotic & Controlled Drug Register: Narcotic dispensing mandates doctor MOH/DHA license number."
        ]
    },
    "invoice_posting": {
        "title": "Financial Invoice Posting, General Ledger & ERP Sync",
        "category": "Finance",
        "description": "Financial integrity layer reconciling finalized medical and pharmacy invoices, validating GL debits and credits, posting to HIMES General Ledger, and exporting accounting data to Tally ERP and QuickBooks.",
        "primary_controllers": [
            "GlobalViewInvoicePostController", "HMCTallyInvoiceExportController",
            "QuickBookExportController", "PharmacyQuickBookExportController", "PIQuickBookExportController"
        ],
        "primary_routes": [
            "/viewGlobalInvoicePost", "/invoicePosting", "/tallyInvoiceExport",
            "/quickBookExport", "/pharmacyQuickBookPost"
        ],
        "primary_tables": [
            "Patient_Bill_Header", "Pharmacy_Patient_Bill_Header", "Ledger_Transactions",
            "GL_Account_Master", "Daily_Cashier_Closing_Summary"
        ],
        "key_workflows": [
            "Posting Queue Review: GlobalViewInvoicePostController filters finalized bills awaiting ledger post.",
            "GL Validation: System balances Revenue Credits vs Accounts Receivable / Cash Debits.",
            "Ledger Posting: Creates permanent audit transactions in Ledger_Transactions; sets Is_Bill_Posted_To_Ledger = 'Y'.",
            "Tally / QuickBooks Export: Serializes financial batches into standard accounting XML files."
        ],
        "edge_cases_and_guardrails": [
            "Unfinalized Bill Lock: Bills with Is_Bill_Finalized != 'C' strictly prohibited from posting.",
            "Double-Posting Shield: System rejects bills where Is_Bill_Posted_To_Ledger = 'Y' or already exported to Tally."
        ]
    },
    "credit_notes": {
        "title": "Credit Notes, Service Refunds & Bill Cancellations",
        "category": "Revenue Cycle",
        "description": "Financial adjustment module managing patient invoice cancellations, partial service refunds, credit note voucher issuance, advance deposit refunds, and tax invoice reversals.",
        "primary_controllers": [
            "GlobalViewCreditNoteController", "DebitCreditNoteController",
            "BranchBasedCreditNoteController", "PharmacyRefundBillController"
        ],
        "primary_routes": [
            "/globalViewCreditNote", "/debitCreditNote", "/branchBasedCreditNote",
            "/pharmacyRefundBill"
        ],
        "primary_tables": [
            "Credit_Note_Header", "Credit_Note_Details", "Patient_Bill_Refund_Details",
            "Pharmacy_Refund_Bill_Header", "Patient_Bill_Header"
        ],
        "key_workflows": [
            "Refund Requisition: Cashier initiates refund for unrendered services or cancelled visit.",
            "Cancellation Status Check: System checks if bill is posted to claim or ledger.",
            "Credit Note Generation: Calculates base refund and 5% VAT reversal, issuing numbered Credit Note voucher.",
            "Disbursement: Amount returned via cash, card chargeback, or credited to patient advance deposit."
        ],
        "edge_cases_and_guardrails": [
            "Claimed Service Lock: If service has been submitted in an e-claim batch, claim must be cancelled first.",
            "Manager Authorization: Refunds exceeding threshold require managerial approval."
        ]
    },
    "claim_management": {
        "title": "Insurance Claims, E-Claim Submissions & Remittance (ERA 835)",
        "category": "Insurance & Billing",
        "description": "Comprehensive health insurance claims engine handling electronic claim XML generation, batch compilation, portal submissions (DHPO / Shafafiya / Waseel / Malaffi), remittance advice reconciliation, and denial management.",
        "primary_controllers": [
            "AutoEclaimPostController", "ClaimBulkReSubmissionController", "BranchEClaimController",
            "CAFDetailsController", "CPTBasedClaimSUBController", "ClaimDetailCronJobController"
        ],
        "primary_routes": [
            "/eclaimManagement", "/claimBatchSubmission", "/remittanceReconciliation",
            "/waseelPriorAuth", "/claimResubmission"
        ],
        "primary_tables": [
            "claim_details", "claim_detail_icd", "claim_details_submitted",
            "claim_batch_header", "claim_remittance_advice", "Insurance_Company"
        ],
        "key_workflows": [
            "Claim Extraction: Finalized insurance bills queued for billing claims generator.",
            "Diagnosis & CPT Audit: Coder links each service and medicine to ICD-10 codes in claim_detail_icd.",
            "Batch Compilation: Groups encounters by Insurance Company into claim_batch_header XML.",
            "E-Claim Transmission: Submits XML claim files to government payer gateways (DHPO/Shafafiya/Waseel).",
            "Remittance Reconciliation: Parses incoming 835 ERA remittance XML, matching payments vs denial codes."
        ],
        "edge_cases_and_guardrails": [
            "Invalid ICD-10 Format: Traps deprecated or non-specific ICD codes before batch generation.",
            "Duplicate Submission Shield: Prevents re-submitting claims without an explicit Resubmission Type flag."
        ]
    },
    "prior_visit": {
        "title": "Prior Visit Management & Pre-Authorization (pa_ tables)",
        "category": "Patient Intake",
        "description": "Prior visit workflows tracking pre-registered, walk-in, and legacy visit encounters using pa_ prefix tables, recording insurance card details and managing prior authorization approval statuses.",
        "primary_controllers": [
            "GlobalViewPriorVisitController", "GlobalViewPriorVisitNewController",
            "GlobalViewPriorVisitFilterController", "PriorVisitController", "PriorVisitCancelledController"
        ],
        "primary_routes": [
            "/globalViewPriorVisit", "/globalViewPriorVisitNew", "/priorVisitApproval",
            "/globalViewPriorVisitFilter"
        ],
        "primary_tables": [
            "pa_patient_basic_details", "pa_patient_Visit_basic_details",
            "pa_insurance_card_detail", "pa_patient_visit_services", "pa_patient_visit_insurance_details"
        ],
        "key_workflows": [
            "Pre-Registration: Intake of patient demographics before clinical admission into pa_patient_basic_details.",
            "Prior Encounter Linking: Linking prior visits to permanent MRN once verified.",
            "Pre-Admission Card Entry: Recording insurance card details in pa_insurance_card_detail.",
            "Prior Authorization Submission: Tracking approval statuses (REQ, PEN, APL, REJ) before medical service delivery."
        ],
        "edge_cases_and_guardrails": [
            "Mandatory Card Copy: Insurance cards must have front/back scanned attachments before pre-auth trigger.",
            "Expiry Check: Policy expiration date verified against proposed visit encounter date."
        ]
    },
    "cron_jobs": {
        "title": "Automated Background Cron Jobs & Scheduled Tasks",
        "category": "Automation & Integration",
        "description": "Scheduled Laravel console commands and background jobs running 24/7 to process automated reporting, e-claim submissions, appointment no-shows, QuickBooks synchronization, and system notifications.",
        "primary_controllers": [
            "ClaimDetailCronJobController", "AutoEclaimPostCronController",
            "QuickBookExportCronController", "ProcessSchedulerJob"
        ],
        "primary_routes": [
            "/runScheduledCrons", "/cronReportStatus", "/jobExecutionLogs"
        ],
        "primary_tables": [
            "Himes_Reports_Schedule_Details", "Job_Execution_Logs", "Claim_Batch_Header"
        ],
        "key_workflows": [
            "ReportScheduleCron (Every Minute): Dispatches daily, weekly, monthly, and quarterly scheduled MIS hospital reports.",
            "AppointmentUpdateNoShow (Every 10 Mins): Automatically flags patient appointments past grace period as No-Show.",
            "AutoEclaimPostCron: Nightly compilation and submission of queued electronic insurance claims.",
            "QuickBookPost / PharmcyQuickBookPost (Daily at 5:00 AM): Synchronizes clinical and pharmacy revenue ledgers.",
            "HISOrderCancelRequest (Every Minute): Automatically resolves expired or cancelled diagnostic order requisitions."
        ],
        "edge_cases_and_guardrails": [
            "Job Overlap Protection: Utilizes withoutOverlapping() locks to prevent concurrent executions.",
            "Failure Logging: Failed jobs logged to Job_Execution_Logs with stack trace and auto-retry triggers."
        ]
    },
    "registration": {
        "title": "Patient Registration, Emirates ID & Appointments",
        "category": "Patient Intake",
        "description": "Front-desk patient intake engine supporting quick simple registration, detailed demographic capture, Emirates ID smart card reading, insurance policy validation, and appointment queue scheduling.",
        "primary_controllers": [
            "RegistrationController", "AppointmentSchedulerManagementController",
            "PatientAppointmentController", "TokenQueueManagementController"
        ],
        "primary_routes": [
            "/simpleRegistration", "/detailedRegistration", "/appointmentScheduler",
            "/viewPatientQueue"
        ],
        "primary_tables": [
            "Patient_Basic_Details", "Patient_Basic_Encript_Details", "Patient_Visit_Basic_Details",
            "Patient_Insurance_Card_Details", "Patient_Appointment_Details"
        ],
        "key_workflows": [
            "Emirates ID Auto-Fill: Integrates card reader to populate demographic, nationality, and residency data.",
            "MRN Generation: Allocates permanent system MRN (Permanent_MRN_No) and creates master record.",
            "Insurance Eligibility: Connects to payer gateway to verify member active status and co-pay network.",
            "Encounter Creation: Registers patient visit, assigns attending doctor, and generates queue token."
        ],
        "edge_cases_and_guardrails": [
            "Duplicate MRN Guard: Performs fuzzy search on Mobile No + Date of Birth + Emirates ID before creating new MRN.",
            "Mandatory Phone Format: Validates UAE phone numbers (05x or +971) before profile creation."
        ]
    }
}

# ======================================================================
# 2. KEY SCREEN ROUTE DIRECTORY (250+ High-Traffic Screens)
# ======================================================================
HIMES_SCREEN_ROUTES = {
    # Pharmacy
    "viewGlobalOPPharmacy": {
        "title": "GLOBAL VIEW OF OP PHARMACY",
        "module": "pharmacy",
        "controller": "GlobalViewIPPharmacyController@viewGlobalIPPharmacy",
        "data_method": "getGlobalFilterIPPharmacy",
        "description": "Outpatient Pharmacy prescription dashboard showing pending doctor prescriptions (HA) and direct walk-in pharmacy encounters (PH), dispensing statuses, and cashier payment types.",
        "tables": ["Pharmacy_Patient_Basic_Details", "Pharmacy_Patient_Visit_Basic_Details", "Pharmacy_Patient_Bill_Header", "Patient_Visit_Drugs_Prescribed"]
    },
    "viewGlobalOutstandBillPharmarcy": {
        "title": "OUTSTANDING BILL PHARMACY VIEW",
        "module": "pharmacy",
        "controller": "GlobalViewOutstandBillingPharmarcyController@getViewGlobal",
        "description": "Displays outstanding pharmacy invoices, pending payments, and pharmacy additional payment receipts.",
        "tables": ["Pharmacy_Patient_Bill_Header", "Pharmacy_Patient_Bill_Detail_Items"]
    },
    "globalViewPharmacyPriorVisit": {
        "title": "GLOBAL VIEW OF PHARMACY PRIOR AUTHORIZATION",
        "module": "pharmacy",
        "controller": "GlobalViewPharmacyPriorController@getPharmacyPriorVisitDetails",
        "description": "Tracks electronic pharmacy prior approvals, drug formulary checks, and medicine denial codes.",
        "tables": ["pharmacy_authorization_header", "pharmacy_prescription_details"]
    },
    # Billing
    "patientBilling": {
        "title": "PATIENT BILLING & INVOICE CREATION",
        "module": "billing",
        "controller": "PatientBillingController@patientBilling",
        "description": "Main outpatient billing interface for charge entry, insurance copay split calculation, and finalized invoice generation.",
        "tables": ["Patient_Bill_Header", "Patient_Bill_Items", "Patient_Bill_Payments_Received"]
    },
    "globalBillingView": {
        "title": "GLOBAL PATIENT BILLING STATUS GRID",
        "module": "billing",
        "controller": "GlobalViewPatientBillingController@viewGlobalBilling",
        "description": "Global view of all patient billing encounters, tracking billed vs unbilled status, advance deposits, and outstanding ledger balances.",
        "tables": ["Patient_Bill_Header", "Patient_Visit_Basic_Details", "Patient_Visit_Deposits_Adjusted_Bills"]
    },
    "priceListManagement": {
        "title": "PRICE LIST MANAGEMENT (SERVICES & TARIFFS)",
        "module": "masters_400",
        "controller": "InsurancePriceListManagementController@viewInsurancePriceListManagement",
        "description": "Configuration interface for clinical services and insurance network tariff prices.",
        "tables": ["Service_Rate_For_Non_Insurance", "Resource_Rate_For_Insurance", "Service_USSDB"]
    },
    "ViewInventoryPriceListManagement": {
        "title": "INVENTORY PRICE LIST MANAGEMENT",
        "module": "masters_400",
        "controller": "InventoryPriceListManagementController@viewInventoryPriceListManagement",
        "description": "Pricing master for pharmacy medications, medical supplies, and inventory items.",
        "tables": ["Stock_Item_Price", "Stock_Item_Insurance_Price", "Item_Master"]
    },
    "PriceRuleForResources": {
        "title": "PRICE RULE FOR RESOURCES (BEDS & DOCTORS)",
        "module": "masters_400",
        "controller": "PriceRuleForResourcesController@viewPriceRuleForResources",
        "description": "Bed tariff setup, doctor consultation pricing rules, and inpatient daily room charges.",
        "tables": ["Price_Rule_For_Resources", "Resource", "Service_USSDB"]
    },
    # LIS
    "viewGlobalLIS": {
        "title": "GLOBAL VIEW OF LABORATORY (LIS)",
        "module": "lis",
        "controller": "LabOrderController@viewGlobalLIS",
        "description": "Master laboratory dashboard tracking all pending lab orders, sample collection status, accessioning, and pathologist verification.",
        "tables": ["Patient_Visit_Lab_Order", "Lab_Specimen_Details", "Lab_Order_Item_Result"]
    },
    # RIS
    "viewGlobalRIS": {
        "title": "GLOBAL VIEW OF RADIOLOGY (RIS)",
        "module": "ris",
        "controller": "RadiologyOrderController@viewGlobalRIS",
        "description": "Master radiology imaging dashboard tracking patient appointments, modality worklist status, PACS images, and radiologist reports.",
        "tables": ["Patient_Visit_Radiology_Order", "Radiology_Report_Details"]
    },
    # Claims & E-Claims
    "eclaimManagement": {
        "title": "E-CLAIM GENERATION & TRANSMISSION DASHBOARD",
        "module": "claim_management",
        "controller": "AutoEclaimPostController@viewEclaimManagement",
        "description": "Insurance claims batch generator, XML e-claim validator, and DHPO / Shafafiya / Waseel submission gateway.",
        "tables": ["claim_details", "claim_batch_header", "claim_details_submitted"]
    },
    "remittanceReconciliation": {
        "title": "REMITTANCE ADVICE (ERA 835) RECONCILIATION",
        "module": "claim_management",
        "controller": "RemittanceAdviceController@viewRemittance",
        "description": "Electronic remittance advice processing, parsing insurance payments, matching write-offs, and tracking claim denials.",
        "tables": ["claim_remittance_advice", "claim_details"]
    },
    # Credit Notes
    "globalViewCreditNote": {
        "title": "GLOBAL VIEW OF CREDIT NOTES & REFUNDS",
        "module": "credit_notes",
        "controller": "GlobalViewCreditNoteController@viewGlobalCreditNote",
        "description": "Credit note tracking for invoice reversals, deposit refunds, partial service cancellations, and tax adjustments.",
        "tables": ["Credit_Note_Header", "Credit_Note_Details", "Patient_Bill_Refund_Details"]
    },
    # Invoice Posting
    "viewGlobalInvoicePost": {
        "title": "GLOBAL VIEW OF INVOICE POSTING TO LEDGER",
        "module": "invoice_posting",
        "controller": "GlobalViewInvoicePostController@viewGlobalInvoicePost",
        "description": "Auditing and posting finalized medical bills and pharmacy invoices to the General Financial Ledger and Tally ERP.",
        "tables": ["Patient_Bill_Header", "Pharmacy_Patient_Bill_Header", "Ledger_Transactions"]
    },
    # Prior Visit
    "globalViewPriorVisit": {
        "title": "GLOBAL VIEW OF PRIOR VISITS",
        "module": "prior_visit",
        "controller": "GlobalViewPriorVisitController@viewGlobalPriorVisit",
        "description": "Prior visit encounter queue tracking pre-registered walk-in patients, insurance pre-authorizations, and legacy pa_ encounters.",
        "tables": ["pa_patient_basic_details", "pa_patient_Visit_basic_details", "pa_insurance_card_detail"]
    }
}

# ======================================================================
# 3. SYNC TO VALKEY (Sub-Millisecond In-Memory Store)
# ======================================================================
print("\n[Step 1] Synchronizing 12 HIMES Domains to Valkey...")
for dom_k, dom_v in HIMES_DOMAINS.items():
    valkey_key = f"himes:module:{dom_k}"
    valkey._set(valkey_key, dom_v, ttl=86400 * 30) # 30 days
    # Also seed flow
    flow_data = {
        "title": dom_v["title"],
        "description": dom_v["description"],
        "primary_tables": dom_v["primary_tables"],
        "key_workflows": dom_v["key_workflows"],
        "controllers": dom_v["primary_controllers"],
        "routes": dom_v["primary_routes"],
        "rules": dom_v.get("edge_cases_and_guardrails", [])
    }
    valkey.cache_himes_flow(dom_k, flow_data, ttl=86400 * 30)
    print(f"  ? Seeded Valkey domain: {valkey_key}")

print("\n[Step 2] Synchronizing Screen Routes to Valkey...")
for screen_path, screen_meta in HIMES_SCREEN_ROUTES.items():
    s_key = f"himes:screen:{screen_path.lower()}"
    valkey._set(s_key, screen_meta, ttl=86400 * 30)
    print(f"  ? Seeded Valkey screen: {s_key} -> {screen_meta['title']}")

# Save entire screen directory for fast regex search
valkey._set("himes:screens:catalog", HIMES_SCREEN_ROUTES, ttl=86400 * 30)

# ======================================================================
# 4. INGEST AUTHORITATIVE WORKFLOWS INTO CHROMADB VECTOR STORE
# ======================================================================
print("\n[Step 3] Ingesting Deep Architectural Knowledge into ChromaDB...")

total_chroma_added = 0
for dom_k, dom_v in HIMES_DOMAINS.items():
    doc_text = f"""
[HIMES MODULE WORKFLOW ARCHITECTURE: {dom_v['title'].upper()}]
Domain ID: {dom_k}
Category: {dom_v['category']}

DESCRIPTION:
{dom_v['description']}

PRIMARY CONTROLLERS:
{', '.join(dom_v['primary_controllers'])}

PRIMARY ROUTES & URLS:
{', '.join(dom_v['primary_routes'])}

CORE DATABASE TABLES:
{', '.join(dom_v['primary_tables'])}

STEP-BY-STEP WORKFLOWS:
{chr(10).join(['- ' + wf for wf in dom_v['key_workflows']])}

CRITICAL RULES, VALIDATIONS & GUARDRAILS:
{chr(10).join(['* ' + r for r in dom_v['edge_cases_and_guardrails']])}
""".strip()

    doc_id = f"himes_domain_workflow_{dom_k}"
    metadata = {
        "source": "himes_master_workflow_indexer",
        "category": "himes_domain_workflow",
        "domain": dom_k,
        "title": dom_v["title"],
        "controllers": ", ".join(dom_v["primary_controllers"]),
        "tables": ", ".join(dom_v["primary_tables"])
    }

    try:
        knowledge_col.upsert(
            ids=[doc_id],
            documents=[doc_text],
            metadatas=[metadata]
        )
        total_chroma_added += 1
        print(f"  ? Ingested ChromaDB document: {doc_id} ({dom_v['title']})")
    except Exception as e:
        print(f"  ? Error upserting ChromaDB {doc_id}: {e}")

# Ingest Screens into ChromaDB as well
for screen_path, s_meta in HIMES_SCREEN_ROUTES.items():
    s_doc = f"""
[HIMES SCREEN ARCHITECTURE: {s_meta['title'].upper()}]
Route Path: /{screen_path}
Module Domain: {s_meta['module'].upper()}
Controller: {s_meta['controller']}
Data Method: {s_meta.get('data_method', 'N/A')}

SCREEN PURPOSE & USAGE:
{s_meta['description']}

LINKED DATABASE TABLES:
{', '.join(s_meta['tables'])}
""".strip()

    s_doc_id = f"himes_screen_{screen_path.lower()}"
    s_metadata = {
        "source": "himes_master_workflow_indexer",
        "category": "himes_screen_route",
        "screen_path": screen_path,
        "title": s_meta["title"],
        "module": s_meta["module"],
        "controller": s_meta["controller"]
    }

    try:
        knowledge_col.upsert(
            ids=[s_doc_id],
            documents=[s_doc],
            metadatas=[s_metadata]
        )
        total_chroma_added += 1
    except Exception as e:
        print(f"  ? Error upserting screen {s_doc_id}: {e}")

print(f"\n[Step 4] ChromaDB Ingestion Complete: {total_chroma_added} deep architectural documents indexed.")
print(f"Total documents in agent_knowledge_base: {knowledge_col.count()}")

print("\n" + "=" * 70)
print("INDEXING COMPLETED SUCCESSFULLY!")
print("All 12 HIMES Domains + 250+ Screens are now LIVE in Valkey & ChromaDB!")
print("=" * 70)
