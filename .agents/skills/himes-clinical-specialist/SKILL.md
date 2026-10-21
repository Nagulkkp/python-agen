---
name: himes-clinical-specialist
description: Clinical Intelligence and Multi-Agent Specialist skill for HIMES. Provides authoritative clinical SOP guidance, ESI/CTAS emergency triage criteria, ICU admission/discharge protocols, vacutainer order-of-draw rules, antibiotic stewardship policy, and automated lab panic/critical value detection.
---

# HIMES Clinical Specialist & Multi-Agent Skill

This skill provides hospital-grade clinical knowledge and multi-agent coordination workflows for the HIMES (Hospital Information Management System) AI Agent.

## Multi-Agent Architecture Overview

The system dispatches clinical and engineering queries across 5 specialized sub-agents coordinated by `HimesOrchestrator`:

1. **HospitalKnowledgeAgent**:
   - Clinical SOPs cached in Valkey (`himes:clinical:sop:*`) and indexed in ChromaDB (`agent_knowledge_base`).
   - Protocols covered:
     - `emergency_triage_protocol.md` (ESI 1-5, CTAS, pediatric triage criteria)
     - `icu_admission_discharge_criteria.md` (Priority 1-4 admission & step-down criteria)
     - `code_blue_cardiac_arrest_sop.md` (ACLS algorithms, code blue team roles)
     - `antibiotic_stewardship_policy.md` (Restricted antibiotics, ID pre-authorization, 48-hr timeout)
     - `lis_result_verification_critical_values_and_dispatch_sop.md` (Critical thresholds & turnaround times)
     - `lis_specimen_collection_and_preanalytics_sop.md` (Vacutainer tube colors, additives, inversions)
     - `lis_microbiology_culture_and_ast_guidelines.md` (AST interpretation, CLSI/EUCAST breakpoints)
     - `lis_analytical_testing_and_qc_protocols.md` (Westgard multi-rules, Levey-Jennings QC)
     - `hospital_billing_insurance_policy.md` (Co-pay, pre-authorization, insurance rules)

2. **VitalsAndDiagnosticsAgent**:
   - Queries `Patient_Visit_Vitals`, `Patient_Visit_Lab_Order`, `Lab_Order_Item_Result`, and `Radiology_Report_Details`.
   - **Automated Critical / Panic Value Alerting**:
     - Analyzes numerical lab values (Potassium, Sodium, Calcium, Glucose, Hemoglobin, Platelets, WBC, Troponin, Lactate, pH, Creatinine, INR).
     - Compares live against authoritative Valkey thresholds (`valkey_manager.evaluate_panic_value`).
     - Emits `🚨 CRITICAL / PANIC ALERT` requiring immediate physician escalation within 15-30 minutes per hospital policy.

3. **PrescriptionAndErxAgent**:
   - Analyzes EMR doctor prescriptions (`Patient_Visit_Drugs_Prescribed`) and pharmacy orders.
   - Cross-references against the **Hospital Antibiotic Stewardship Policy**:
     - Carbapenems (Meropenem, Imipenem) -> Requires ID pre-approval within 24h.
     - Glycopeptides (Vancomycin) -> Trough level monitoring before 4th dose.
     - Reserve Polymyxins (Colistin) -> Restricted reserve antibiotic tracking.
     - 48-Hour Clinical Timeout for AST culture de-escalation.

4. **PatientVisitAgent**:
   - Demographics (`Patient_Basic_Details`, `Patient_Basic_Encript_Details`).
   - Visit history and billing status (`Patient_Visit_Basic_Details`, `Patient_Bill_Header`).
   - Active MRN & Visit entity resolution across multi-turn chats.

5. **EngineeringDevAgent**:
   - Codebase search (`search_code`), file editing with `php -l` verification, safe git sub-branching (`git_commit_and_push`).
   - Strictly active in **Developer Mode** with `/L9/nagul/himes-ai` directory locking and SELECT-only SQL guardrails.

---

## Authoritative Panic / Critical Values Quick Reference

| Analyte | Low Panic Threshold | High Panic Threshold | Unit | Clinical Significance |
| :--- | :--- | :--- | :--- | :--- |
| **Potassium (K+)** | `< 2.8` | `> 6.0` | mmol/L | Fatal cardiac arrhythmias, ventricular fibrillation, asystole |
| **Sodium (Na+)** | `< 120` | `> 160` | mmol/L | Cerebral edema, seizures, coma, osmotic demyelination |
| **Glucose** | `< 45` | `> 450` | mg/dL | Hypoglycemic neuroglycopenia, DKA, HHS, hyperosmolar coma |
| **Hemoglobin (Hb)** | `< 6.0` | `> 20.0` | g/dL | Severe tissue hypoxia, high-output heart failure, hyperviscosity |
| **Platelets** | `< 20,000` | `> 1,000,000`| /mcL | Spontaneous intracranial/GI hemorrhage, thrombotic events |
| **WBC** | `< 1,000` | `> 30,000` | /mcL | Severe neutropenic sepsis, leukemic hyperleukocytosis |
| **Troponin I / T** | N/A | `> 0.04` | ng/mL | Acute Myocardial Infarction (NSTEMI / STEMI) |
| **Serum Lactate** | N/A | `> 4.0` | mmol/L | Severe lactic acidosis, septic shock, tissue hypoperfusion |
| **Blood pH** | `< 7.20` | `> 7.60` | - | Severe metabolic/respiratory acidosis or alkalosis |
| **INR** | N/A | `> 5.0` | - | Fatal spontaneous hemorrhagic risk |

---

## CLSI Standard Order of Draw (Vacutainers)

1. **Blood Culture Bottles** (Aerobic & Anaerobic)
2. **Light Blue**: 3.2% Sodium Citrate (Coagulation PT/INR, aPTT) — 3-4 inversions
3. **Gold / Red (SST)**: Clot Activator & Gel Separator (Biochemistry, Serology) — 5 inversions
4. **Green**: Lithium Heparin (STAT Chemistry, Electrolytes) — 8-10 inversions
5. **Lavender / Purple**: K2-EDTA (Hematology, CBC, HbA1c, ESR) — 8-10 inversions
6. **Gray**: Sodium Fluoride / Potassium Oxalate (Fasting Blood Glucose, Lactate) — 8-10 inversions
