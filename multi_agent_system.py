"""
=============================================================================
HIMES MULTI-AGENT SPECIALIST SYSTEM (PRODUCTION ORCHESTRATION)
=============================================================================
Architecture inspired by clinical AI microservices, seamlessly adapted for Nagul's
HIMES application (/L9/nagul/himes-ai) with local execution (127.0.0.1:8050),
Dual Response System (User View vs. Developer View), strict read-only SQL safety,
and accelerated Valkey / ChromaDB knowledge integration.

SPECIALIST AGENT ROLES:
1. HospitalKnowledgeAgent: Clinical SOPs (Triage ESI 1-5, ICU 1-4, Code Blue, LIS TAT, Tube Colors, Antibiotic Stewardship)
2. VitalsAndDiagnosticsAgent: EMR Vitals, LIS Lab Results, RIS Radiology Reports + AUTOMATED PANIC VALUE DETECTION
3. PrescriptionAndErxAgent: Medications, Drug Prescriptions, Dosage Reconciliation & Stewardship Timeout
4. PatientVisitAgent: Demographics, MRN Lookup, Visit History, Billing Status Reconciliation
5. EngineeringDevAgent: Codebase Search, php -l Verification, Git Sub-Branches, Raw Diagnostics (Developer Mode Only)
6. HimesOrchestrator: Intent Router & Coordinator that resolves entities and directs tasks to the right specialist
=============================================================================
"""

import os
import re
import json
import time
from typing import Dict, Any, List, Optional, Tuple

from valkey_himes_manager import valkey_manager
from memory_manager import search_knowledge_base
from autonomous_agent import autonomous_agent
from guardrails import SecurityException
from generation.rag_pipeline import rag_pipeline
from language_specialist_agent import language_specialist



# ---------------------------------------------------------------------------
# Base Specialist Agent
# ---------------------------------------------------------------------------
class BaseSpecialistAgent:
    def __init__(self, name: str, role_description: str):
        self.name = name
        self.role_description = role_description

    def call_llm(self, prompt: str, system_prompt: str) -> str:
        """Invokes the central LLM engine via autonomous_agent with fallbacks."""
        return autonomous_agent.call_llm(prompt, system_prompt)

    def execute_sql(self, sql_query: str) -> List[Dict[str, Any]]:
        """Executes a SELECT query safely via Docker tinker and returns parsed list of dicts."""
        raw = autonomous_agent.execute_select_sql(sql_query)
        if raw and raw.strip().startswith("["):
            try:
                return json.loads(raw)
            except Exception:
                return []
        return []


# ---------------------------------------------------------------------------
# Specialist 1: HospitalKnowledgeAgent
# ---------------------------------------------------------------------------
class HospitalKnowledgeAgent(BaseSpecialistAgent):
    """
    Specialist for Hospital Clinical SOPs, Protocols, and Knowledge Base.
    Fast-paths queries using Valkey cache and ChromaDB semantic search.
    """
    def __init__(self):
        super().__init__(
            name="HospitalKnowledgeAgent",
            role_description="Hospital Clinical SOPs, Emergency Triage, ICU Criteria, Code Blue, Vacutainers, LIS TAT & Stewardship"
        )

    def get_sop_by_topic(self, topic: str) -> Optional[Dict[str, Any]]:
        """Retrieves clinical SOP from Valkey by keyword or slug."""
        return valkey_manager.get_clinical_sop(topic)

    def get_vacutainer_info(self, test_name: str = "") -> Dict[str, Any]:
        """Retrieves vacutainer tube collection guidelines from Valkey."""
        guide = valkey_manager.get_cached_data("himes:clinical:vacutainer_guide")
        if not guide or not isinstance(guide, dict):
            return {}
        if not test_name:
            return guide
        test_lower = test_name.lower()
        for color, info in guide.items():
            if color.lower() in test_lower:
                return {color: info}
            for example in info.get("common_tests", []):
                if test_lower in example.lower() or example.lower() in test_lower:
                    return {color: info}
        return guide

    def search_clinical_kb(self, query: str, n_results: int = 3) -> List[Dict[str, Any]]:
        """Searches ChromaDB agent_knowledge_base collection for clinical evidence."""
        return search_knowledge_base(query, n_results=n_results)

    def handle(self, query: str, context: Dict[str, Any], is_dev_mode: bool = False) -> Dict[str, Any]:
        query_lower = query.lower()

        # 1. Vacutainer / Tube color inquiry
        if any(w in query_lower for w in ["tube", "vacutainer", "blood collection", "additive", "inversion", "color", "colour", "cbc tube", "edta"]):
            guide = self.get_vacutainer_info(query)
            if guide:
                rows = ""
                for color, details in guide.items():
                    tests = ", ".join(details.get("common_tests", []))
                    rows += f"| **{color}** | {details.get('additive')} | {details.get('inversions')} | {tests} |\n"
                
                reply = (
                    "### 🧪 Clinical Specimen Collection & Vacutainer Guide\n\n"
                    "According to the HIMES Clinical Laboratory SOP (`lis_specimen_collection_and_preanalytics_sop`):\n\n"
                    "| Tube Top Color | Additive / Anticoagulant | Inversions | Common Tests |\n"
                    "| :--- | :--- | :--- | :--- |\n"
                    f"{rows}\n"
                    "> 💡 **Clinical Rule:** Always follow the CLSI H3-A6 standard **Order of Draw** (Blood Culture -> Light Blue -> Red/Gold -> Green -> Lavender -> Gray) to prevent additive cross-contamination!"
                )
                return {"reply": reply, "agent": self.name, "source": "valkey_vacutainer_guide"}

        # 2. Direct Clinical SOP topic check from Valkey
        sop_data = self.get_sop_by_topic(query)
        if sop_data:
            title = sop_data.get("title", "Hospital Clinical Protocol")
            content = sop_data.get("content", "")
            
            system_prompt = (
                f"You are the HIMES Clinical Knowledge Specialist. Summarize the authoritative protocol accurately "
                f"based on the provided hospital SOP. Maintain clinical accuracy. Do not hallucinate."
            )
            prompt = (
                f"User Question: {query}\n\n"
                f"Authoritative Hospital SOP Title: {title}\n"
                f"Protocol Content:\n{content[:4000]}\n\n"
                f"Provide a structured, authoritative answer covering key clinical criteria, responsibilities, and guidelines."
            )
            summary = self.call_llm(prompt, system_prompt)
            formatted_reply = f"### 📘 {title}\n\n{summary}\n\n*(Verified against authoritative HIMES Clinical SOP)*"
            return {"reply": formatted_reply, "agent": self.name, "source": "valkey_clinical_sop"}

        # 3. Advanced Hybrid RAG Engine (BM25 + Chroma Dense + RRF + Grounded Citations)
        rag_res = rag_pipeline.answer_query(query, is_developer_mode=is_dev_mode)
        return {
            "reply": rag_res["reply"],
            "agent": self.name,
            "source": "hybrid_rag_pipeline",
            "citations": rag_res.get("citations", []),
            "latency_ms": rag_res.get("latency_ms", 0.0)
        }


# ---------------------------------------------------------------------------
# Specialist 2: VitalsAndDiagnosticsAgent
# ---------------------------------------------------------------------------
class VitalsAndDiagnosticsAgent(BaseSpecialistAgent):
    """
    Specialist for Patient Vitals, Triage Assessment, Lab Results (LIS),
    and Radiology Reports (RIS).
    Includes Live Automated Critical / Panic Value Alerting.
    """
    def __init__(self):
        super().__init__(
            name="VitalsAndDiagnosticsAgent",
            role_description="EMR Vitals, Triage, LIS Lab Results, RIS Radiology Reports, Live Panic Alerts"
        )

    def evaluate_results_for_panic(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Scans numerical lab or vital results against Valkey panic thresholds.
        Returns list of critical alert dictionaries.
        """
        alerts = []
        for row in results:
            analyte = row.get("Test_Name") or row.get("Item_Description") or row.get("Service_Description") or row.get("Analyte") or ""
            val_str = str(row.get("Result_Value") or row.get("Numeric_Value") or row.get("Value") or "").strip()
            if not analyte or not val_str:
                continue
            
            # Extract numerical value using regex
            num_match = re.search(r"[-+]?\d*\.?\d+", val_str)
            if num_match:
                try:
                    num_val = float(num_match.group(0))
                    panic_eval = valkey_manager.evaluate_panic_value(analyte, num_val)
                    if panic_eval and panic_eval.get("is_panic"):
                        alerts.append(panic_eval)
                except Exception:
                    pass
        return alerts

    def handle(self, query: str, context: Dict[str, Any], is_dev_mode: bool = False) -> Dict[str, Any]:
        active_visit = (context.get("active_entities") or {}).get("visit_no")
        active_mrn = (context.get("active_entities") or {}).get("mrn")
        query_lower = query.lower()

        # A. If user asks about a hypothetical or specific lab test value (e.g. "Potassium 6.2 mmol/L panic-a?")
        num_match = re.search(r"[-+]?\d*\.?\d+", query)
        analyte_match = None
        for word in ["potassium", "sodium", "calcium", "glucose", "hemoglobin", "platelets", "wbc", "troponin", "lactate", "ph", "creatinine", "inr"]:
            if word in query_lower:
                analyte_match = word
                break
        
        if analyte_match and num_match:
            val = float(num_match.group(0))
            panic_eval = valkey_manager.evaluate_panic_value(analyte_match, val)
            if panic_eval and panic_eval.get("is_panic"):
                reply = (
                    f"{panic_eval['alert_banner']}\n\n"
                    f"• **Analyte:** {panic_eval['analyte']}\n"
                    f"• **Observed Result:** {panic_eval['value']} {panic_eval['unit']}\n"
                    f"• **Critical Threshold:** {panic_eval['threshold']} {panic_eval['unit']}\n"
                    f"• **Clinical Significance:** {panic_eval['clinical_significance']}\n\n"
                    f"> ⚠️ **Mandatory Protocol Action:** Laboratory/Nursing staff must telephone the attending doctor immediately within 15-30 minutes and record read-back confirmation in the EMR!"
                )
                return {"reply": reply, "agent": self.name, "action": "panic_alert_triggered"}
            else:
                reply = (
                    f"✅ **Normal / Non-Panic Value:** The reported result of **{val}** for **{analyte_match.capitalize()}** does not trigger a critical/panic hospital alarm according to the HIMES LIS Critical Value SOP.\n"
                    f"*(Standard reference ranges apply. Always correlate clinically with patient status)*"
                )
                return {"reply": reply, "agent": self.name, "action": "normal_evaluation"}

        # B. If MRN / Visit available, fetch live vitals & lab results
        if active_visit or active_mrn:
            where_clause = f"pvbd.Permanent_Visit_No = '{active_visit}'" if active_visit else f"pbd.Permanent_MRN_No = '{active_mrn}'"
            vitals_sql = f"""
            SELECT TOP 5
                pbd.Permanent_MRN_No,
                pvbd.Permanent_Visit_No,
                pv.Temperature,
                pv.Pulse,
                pv.Blood_Pressure_Systolic,
                pv.Blood_Pressure_Diastolic,
                pv.Respiration_Rate,
                pv.SPO2,
                pv.Pain_Scale,
                pv.Active_Status
            FROM Patient_Visit_Vitals pv WITH(NOLOCK)
            JOIN Patient_Visit_Basic_Details pvbd WITH(NOLOCK) ON pv.Patient_Visit_Basic_Details_Serial_No = pvbd.Patient_Visit_Basic_Details_Serial_No
            JOIN Patient_Basic_Details pbd WITH(NOLOCK) ON pvbd.Patient_Basic_Details_Serial_No = pbd.Patient_Basic_Details_Serial_No
            WHERE {where_clause}
              AND pv.Active_Status = 'A'
            ORDER BY pv.Patient_Visit_Vitals_Serial_No DESC
            """
            vitals_data = self.execute_sql(vitals_sql)
            
            # Fetch lab results if asked
            lab_sql = f"""
            SELECT TOP 10
                s.Service_Description as Test_Name,
                loi.Result_Value,
                loi.Reference_Range,
                loi.Is_Panic_Result,
                loi.Active_Status
            FROM Patient_Visit_Lab_Order lo WITH(NOLOCK)
            JOIN Lab_Order_Item_Result loi WITH(NOLOCK) ON lo.Patient_Visit_Lab_Order_Serial_No = loi.Patient_Visit_Lab_Order_Serial_No
            JOIN Patient_Visit_Basic_Details pvbd WITH(NOLOCK) ON lo.Patient_Visit_Basic_Details_Serial_No = pvbd.Patient_Visit_Basic_Details_Serial_No
            JOIN Patient_Basic_Details pbd WITH(NOLOCK) ON pvbd.Patient_Basic_Details_Serial_No = pbd.Patient_Basic_Details_Serial_No
            JOIN Service s WITH(NOLOCK) ON loi.Service_Serial_No = s.Service_Serial_No
            WHERE {where_clause}
              AND lo.Active_Status = 'A'
            ORDER BY loi.Lab_Order_Item_Result_Serial_No DESC
            """
            lab_data = self.execute_sql(lab_sql)

            # Evaluate any panic values
            panic_alerts = self.evaluate_results_for_panic(lab_data)

            # Synthesize response
            alert_header = ""
            if panic_alerts:
                alert_header = "### 🚨 CRITICAL / PANIC LAB ALERTS DETECTED\n" + "\n".join([f"- {a['alert_banner']}" for a in panic_alerts]) + "\n\n---\n\n"

            reply_parts = []
            if vitals_data:
                v = vitals_data[0]
                bp = f"{v.get('Blood_Pressure_Systolic', '-')}/{v.get('Blood_Pressure_Diastolic', '-')}"
                reply_parts.append(
                    f"### 🩺 Patient Recorded Vitals (Visit: {v.get('Permanent_Visit_No', active_visit)})\n\n"
                    f"• **Blood Pressure (BP):** `{bp} mmHg`\n"
                    f"• **Pulse / Heart Rate:** `{v.get('Pulse', '-')} bpm`\n"
                    f"• **SpO2 (Oxygen Saturation):** `{v.get('SPO2', '-')}%`\n"
                    f"• **Temperature:** `{v.get('Temperature', '-')} °C`\n"
                    f"• **Respiratory Rate:** `{v.get('Respiration_Rate', '-')} breaths/min`\n"
                    f"• **Pain Score:** `{v.get('Pain_Scale', '-')}/10`"
                )
            if lab_data:
                lab_rows = "\n".join([f"| {r.get('Test_Name')} | {r.get('Result_Value')} | {r.get('Reference_Range', '-')} |" for r in lab_data])
                reply_parts.append(
                    f"\n\n### 🔬 Laboratory Results\n\n"
                    f"| Test Name | Result | Reference Range |\n"
                    f"| :--- | :--- | :--- |\n"
                    f"{lab_rows}"
                )

            if reply_parts:
                return {
                    "reply": alert_header + "\n\n".join(reply_parts),
                    "agent": self.name,
                    "panic_count": len(panic_alerts)
                }

        # Fallback to Autonomous Agent if complex
        return autonomous_agent.run(query, context)


# ---------------------------------------------------------------------------
# Specialist 3: PrescriptionAndErxAgent
# ---------------------------------------------------------------------------
class PrescriptionAndErxAgent(BaseSpecialistAgent):
    """
    Specialist for EMR Doctor Prescriptions, OP Pharmacy Dispensing,
    Dosage Verification, and Antibiotic Stewardship Policy Reconciliation.
    """
    def __init__(self):
        super().__init__(
            name="PrescriptionAndErxAgent",
            role_description="Prescription, Drug Dispensing, Dosage Reconciliation & Antibiotic Stewardship"
        )

    def check_antibiotic_stewardship(self, drug_name: str) -> Optional[str]:
        """Checks if prescribed drug is a restricted antibiotic requiring ID pre-approval."""
        restricted = {
            "meropenem": "Carbapenem - Restricted. Requires Infectious Disease (ID) approval within 24 hours.",
            "imipenem": "Carbapenem - Restricted. Requires ID specialist consultation.",
            "colistin": "Polymyxin - Reserve antibiotic for MDR Gram-negative pathogens. Strictly monitored.",
            "vancomycin": "Glycopeptide - Trough level monitoring required before 4th dose. Target: 15-20 mcg/mL.",
            "linezolid": "Oxazolidinone - Restricted. Requires weekly CBC monitoring for myelosuppression.",
            "piperacillin": "Extended-spectrum penicillin + inhibitor. Empiric therapy must be reassessed at 48h.",
            "tazobactam": "Extended-spectrum penicillin + inhibitor. 48-hour antibiotic timeout required."
        }
        clean = drug_name.lower()
        for abx, policy in restricted.items():
            if abx in clean:
                return f"⚠️ **Antibiotic Stewardship Alert ({abx.capitalize()}):** {policy}"
        return None

    def handle(self, query: str, context: Dict[str, Any], is_dev_mode: bool = False) -> Dict[str, Any]:
        active_visit = (context.get("active_entities") or {}).get("visit_no")
        active_mrn = (context.get("active_entities") or {}).get("mrn")

        # 1. Check for specific drug questions / stewardship rules
        for abx in ["meropenem", "colistin", "vancomycin", "linezolid", "piperacillin", "tazobactam"]:
            if abx in query.lower():
                notice = self.check_antibiotic_stewardship(abx)
                sop = valkey_manager.get_clinical_sop("antibiotic_stewardship_policy")
                guideline = sop.get("content", "")[:1200] if sop else ""
                reply = (
                    f"{notice}\n\n"
                    f"### 🛡️ Hospital Antibiotic Stewardship Protocol\n"
                    f"Per hospital policy (`antibiotic_stewardship_policy`):\n"
                    f"1. **Pre-Authorization:** Restricted antimicrobial agents require infectious disease specialist justification.\n"
                    f"2. **48-Hour Timeout:** Attending physician must perform a clinical timeout at 48 hours to review culture and susceptibility (AST) results.\n"
                    f"3. **De-escalation:** Switch from broad-spectrum to narrow-spectrum therapy as soon as pathogen is identified."
                )
                return {"reply": reply, "agent": self.name, "action": "stewardship_check"}

        # 2. Query active visit prescriptions from MSSQL
        if active_visit or active_mrn:
            where_clause = f"pvbd.Permanent_Visit_No = '{active_visit}'" if active_visit else f"pbd.Permanent_MRN_No = '{active_mrn}'"
            rx_sql = f"""
            SELECT TOP 10
                pvdp.Patient_Visit_Drugs_Prescribed_Serial_No,
                pvdp.Drug_Generic_Name,
                pvdp.Drug_Brand_Name,
                pvdp.Dosage,
                pvdp.Frequency,
                pvdp.Duration_In_Days,
                pvdp.Instruction,
                pvdp.Active_Status
            FROM Patient_Visit_Drugs_Prescribed pvdp WITH(NOLOCK)
            JOIN Patient_Visit_Basic_Details pvbd WITH(NOLOCK) ON pvdp.Patient_Visit_Basic_Details_Serial_No = pvbd.Patient_Visit_Basic_Details_Serial_No
            JOIN Patient_Basic_Details pbd WITH(NOLOCK) ON pvbd.Patient_Basic_Details_Serial_No = pbd.Patient_Basic_Details_Serial_No
            WHERE {where_clause}
              AND pvdp.Active_Status = 'A'
            ORDER BY pvdp.Patient_Visit_Drugs_Prescribed_Serial_No DESC
            """
            rx_data = self.execute_sql(rx_sql)
            if rx_data:
                rows = ""
                stewardship_warnings = []
                for r in rx_data:
                    name = r.get("Drug_Brand_Name") or r.get("Drug_Generic_Name") or "Medication"
                    dosage = r.get("Dosage") or "-"
                    freq = r.get("Frequency") or "-"
                    days = r.get("Duration_In_Days") or "-"
                    rows += f"| **{name}** | {dosage} | {freq} | {days} days |\n"
                    
                    stew = self.check_antibiotic_stewardship(name)
                    if stew:
                        stewardship_warnings.append(stew)

                warn_text = "\n\n".join(stewardship_warnings) + "\n\n---\n\n" if stewardship_warnings else ""
                reply = (
                    f"{warn_text}"
                    f"### 💊 Active Prescriptions (Visit: {active_visit or active_mrn})\n\n"
                    f"| Medication | Dosage | Frequency | Duration |\n"
                    f"| :--- | :--- | :--- | :--- |\n"
                    f"{rows}\n"
                    f"> ℹ️ **Action:** Prescriptions are recorded in EMR and dispatched to OP Pharmacy for dispensing."
                )
                return {"reply": reply, "agent": self.name}

        return autonomous_agent.run(query, context)


# ---------------------------------------------------------------------------
# Specialist 4: PatientVisitAgent
# ---------------------------------------------------------------------------
class PatientVisitAgent(BaseSpecialistAgent):
    """
    Specialist for Patient Demographics, Identification, MRN Resolution,
    and Visit History Overview.
    """
    def __init__(self):
        super().__init__(
            name="PatientVisitAgent",
            role_description="Patient Demographics, MRN Resolution, Registration, Visit History"
        )

    def handle(self, query: str, context: Dict[str, Any], is_dev_mode: bool = False) -> Dict[str, Any]:
        active_mrn = (context.get("active_entities") or {}).get("mrn")
        active_visit = (context.get("active_entities") or {}).get("visit_no")

        if active_mrn:
            patient_sql = f"""
            SELECT TOP 1
                pbd.Permanent_MRN_No,
                pbed.Patient_First_Name,
                pbed.Patient_Middle_Name,
                pbed.Patient_Last_Name,
                pbed.Contact_Phone_Mobile,
                pbed.Emirates_Id,
                pbd.Gender,
                pbd.Age
            FROM Patient_Basic_Details pbd WITH(NOLOCK)
            JOIN Patient_Basic_Encript_Details pbed WITH(NOLOCK) ON pbd.Patient_Basic_Details_Serial_No = pbed.Patient_Basic_Details_Serial_No
            WHERE pbd.Permanent_MRN_No = '{active_mrn}'
            """
            p_data = self.execute_sql(patient_sql)
            if p_data:
                p = p_data[0]
                full_name = f"{p.get('Patient_First_Name', '')} {p.get('Patient_Last_Name', '')}".strip()
                
                # Fetch recent visits
                visits_sql = f"""
                SELECT TOP 5
                    pvbd.Permanent_Visit_No,
                    pvbd.Patient_Visit_Registered_Date_Time,
                    pbh.Bill_No,
                    pbh.Bill_Net_Value,
                    pbh.Is_Bill_Finalized
                FROM Patient_Visit_Basic_Details pvbd WITH(NOLOCK)
                JOIN Patient_Basic_Details pbd WITH(NOLOCK) ON pvbd.Patient_Basic_Details_Serial_No = pbd.Patient_Basic_Details_Serial_No
                LEFT JOIN Patient_Bill_Header pbh WITH(NOLOCK) 
                  ON pbh.Patient_Visit_Basic_Details_Serial_No = pvbd.Patient_Visit_Basic_Details_Serial_No
                  AND pbh.Bill_Cancellation_Flag = 'N'
                WHERE pbd.Permanent_MRN_No = '{active_mrn}'
                  AND pvbd.Active_Status = 'A'
                  AND pvbd.Visit_Cancellation_Flag = 'N'
                ORDER BY pvbd.Patient_Visit_Basic_Details_Serial_No DESC
                """
                v_data = self.execute_sql(visits_sql)
                v_rows = ""
                for v in v_data:
                    v_no = v.get("Permanent_Visit_No")
                    v_date = str(v.get("Patient_Visit_Registered_Date_Time", ""))[:16]
                    is_fin = v.get("Is_Bill_Finalized") == "C"
                    fin_str = f"Finalized ({v.get('Bill_No')}, {v.get('Bill_Net_Value')} AED)" if is_fin else "Pending / Unfinalized"
                    v_rows += f"| {v_no} | {v_date} | {fin_str} |\n"

                reply = (
                    f"### 👤 Patient Overview: **{full_name}**\n\n"
                    f"• **MRN:** `{p.get('Permanent_MRN_No')}`\n"
                    f"• **Age / Gender:** `{p.get('Age', '-')} yrs / {p.get('Gender', '-')}`\n"
                    f"• **Emirates ID:** `{p.get('Emirates_Id', '-')}`\n"
                    f"• **Mobile:** `{p.get('Contact_Phone_Mobile', '-')}`\n\n"
                    f"**Recent Visits ({len(v_data)} recorded):**\n\n"
                    f"| Visit No | Registration Date | Billing Status |\n"
                    f"| :--- | :--- | :--- |\n"
                    f"{v_rows}"
                )
                return {"reply": reply, "agent": self.name}

        return autonomous_agent.run(query, context)


# ---------------------------------------------------------------------------
# Specialist 5: EngineeringDevAgent
# ---------------------------------------------------------------------------
class EngineeringDevAgent(BaseSpecialistAgent):
    """
    Specialist for Codebase Investigation, Route/Controller Analysis,
    php -l Verification, Git Sub-Branches, and Raw SQL Diagnostics.
    Strictly active in Developer Mode with /L9/nagul/himes-ai directory lock.
    """
    def __init__(self):
        super().__init__(
            name="EngineeringDevAgent",
            role_description="Codebase Investigation, php -l Syntax Verification, Git Automation, Technical Diagnostics"
        )

    def handle(self, query: str, context: Dict[str, Any], is_dev_mode: bool = True) -> Dict[str, Any]:
        return autonomous_agent.run(query, context)


# ---------------------------------------------------------------------------
# Multi-Agent Orchestrator: HimesOrchestrator
# ---------------------------------------------------------------------------
class HimesOrchestrator:
    """
    Multi-Agent Coordinator that inspects intent, classifies tasks,
    routes to specialist sub-agents, and enforces Dual Mode formatting.
    """
    def __init__(self):
        self.language_agent = language_specialist
        self.knowledge_agent = HospitalKnowledgeAgent()
        self.diagnostics_agent = VitalsAndDiagnosticsAgent()
        self.prescription_agent = PrescriptionAndErxAgent()
        self.visit_agent = PatientVisitAgent()
        self.dev_agent = EngineeringDevAgent()

    def classify_intent(self, user_msg: str, context: Dict[str, Any]) -> str:
        """
        Classifies incoming intent into a specialist role.
        """
        msg = user_msg.lower()

        # 1. Developer Engineering Intent
        dev_indicators = [
            "search_code", "find_route", "edit_file", "git", "commit", "push", "php -l",
            "syntax", "controller", "model file", "routes.php", "grep -rn", "blade.php",
            ".php", "error", "warning", "exception", "array offset", "fix this issue",
            "branch name", "pull request", "pr", "bug", "line :", "line:", "stack trace",
            "local.warning", "local.error", "trying to access"
        ]
        if any(w in msg for w in dev_indicators):
            return "engineering_dev"

        # 2. Clinical SOP / Protocol / Knowledge Intent
        sop_indicators = [
            "sop", "protocol", "triage", "icu criteria", "discharge criteria",
            "admission criteria", "code blue", "cardiac arrest", "vacutainer", "tube color",
            "blood tube", "inversion", "inversions", "critical values", "panic values list", "stewardship",
            "restricted antibiotic", "turnaround time", "westgard", "qc protocol", "specimen",
            "blood collection", "order of draw"
        ]
        if any(w in msg for w in sop_indicators) or re.search(r'\b(tat|esi)\b', msg):
            return "hospital_knowledge"

        # 3. Vitals & Lab Diagnostics Intent + Live Panic Check
        diag_indicators = [
            "vital", "vitals", "pulse", "spo2", "temperature", "temp", "heart rate",
            "pain scale", "lab result", "potassium", "sodium", "calcium", "glucose", "hemoglobin",
            "platelet", "platelets", "wbc", "troponin", "lactate", "panic", "critical alert", "critical value"
        ]
        if any(w in msg for w in diag_indicators) or re.search(r'\bbp\b', msg):
            return "vitals_and_diagnostics"

        # 4. Prescription / Pharmacy / Antibiotics Intent
        rx_indicators = [
            "prescription", "drug", "medicine", "medication", "dose", "dosage", "dispensing",
            "meropenem", "vancomycin", "colistin", "antibiotic", "imipenem", "linezolid",
            "piperacillin", "tazobactam"
        ]
        if any(w in msg for w in rx_indicators) or re.search(r'\brx\b', msg):
            return "prescription_and_erx"

        # 5. Patient Profile / Demographic Lookup Intent (excludes billing/service/diagnostic queries)
        is_services_or_billing = any(w in msg for w in ["service", "services", "unbilled", "bill", "billing", "cpt", "test", "procedure", "lab order", "فحوصات", "غير مفوتر", "பில்", "podadha", "aagadha", "invoice"])
        patient_indicators = ["patient details", "patient profile", "patient name", "demographics", "last 5 visit", "last 10 visit", "visits for mrn"]
        if not is_services_or_billing and (any(w in msg for w in patient_indicators) or (re.search(r'\b(profile|demographics)\b', msg) and "mrn" in msg)):
            return "patient_visit"


        # 6. Default / Hybrid
        return "general_hybrid"

    def dispatch(self, user_msg: str, context: Dict[str, Any], is_dev_mode: bool = False) -> Dict[str, Any]:
        """
        Orchestrates execution by:
        1. Detecting exact user language via LanguageSpecialistAgent.
        2. Normalizing non-English queries into English for database execution.
        3. Dispatching to designated specialist.
        4. Mirroring final response into the user's exact language.
        """
        start_time = time.time()
        
        # 1. Multi-Agent Language Detection & Normalization
        lang_info = self.language_agent.detect_language(user_msg)
        norm_english = self.language_agent.normalize_to_english(user_msg, lang_info) if not lang_info.get("is_english") else user_msg

        ctx = dict(context or {})
        ctx["user_language"] = lang_info
        ctx["normalized_english_query"] = norm_english

        intent = self.classify_intent(user_msg, ctx)

        if intent == "hospital_knowledge":
            res = self.knowledge_agent.handle(user_msg, ctx, is_dev_mode)
        elif intent == "vitals_and_diagnostics":
            res = self.diagnostics_agent.handle(user_msg, ctx, is_dev_mode)
        elif intent == "prescription_and_erx":
            res = self.prescription_agent.handle(user_msg, ctx, is_dev_mode)
        elif intent == "patient_visit":
            res = self.visit_agent.handle(user_msg, ctx, is_dev_mode)
        elif intent == "engineering_dev":
            res = self.dev_agent.handle(user_msg, ctx, is_dev_mode)
        else:
            # Fallback to general autonomous agent
            res = autonomous_agent.run(user_msg, ctx)

        # 2. Strict Multilingual Response Mirroring
        raw_reply = res.get("reply", "")
        if raw_reply:
            res["reply"] = self.language_agent.mirror_reply(raw_reply, lang_info)

        elapsed = round(time.time() - start_time, 3)
        res["orchestrator_intent"] = intent
        res["detected_language"] = lang_info.get("language_name")
        res["execution_time_sec"] = elapsed
        return res


# Global instance
himes_orchestrator = HimesOrchestrator()
