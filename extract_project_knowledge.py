import os
import sys
import re
import json
from typing import Dict, List, Any
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

load_dotenv(override=True)

from ssh_sandbox import sandboxed_ssh
from autonomous_agent import autonomous_agent

REMOTE_BASE = "/L9/nagul/himes-ai"
OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "modules_knowledge.md")

# Module keyword configurations
TARGET_MODULES = {
    "Appointment": {
        "keywords": ["appointment", "scheduler", "scheduling", "schedular", "aps", "asm"],
        "tables": ["Appointment", "Patient_Appointment", "Patient_Visit_Scheduling"]
    },
    "Registration": {
        "keywords": ["registration", "patientregister", "quickregistration", "patient_basic"],
        "tables": ["Patient_Basic_Details", "Patient_Basic_Encript_Details", "Registration"]
    },
    "Billing": {
        "keywords": ["billing", "patientbilling", "bill", "invoice", "pricelist", "tariff"],
        "tables": ["Patient_Bill_Header", "Patient_Visit_Services", "Patient_Bill_Detail_Services_Packages_Resources_Drugs"]
    },
    "Prior Approval": {
        "keywords": ["priorapproval", "prior_approval", "preauth", "pre_auth", "insuranceplanpriorapproval"],
        "tables": ["Insurance_Plan_Excluded_Prior_Approval_Services", "BI_Prior_Approval", "Prior_Approval"]
    },
    "Prior Visit": {
        "keywords": ["priorvisit", "prior_visit", "visit"],
        "tables": ["Patient_Visit_Basic_Details", "Patient_Visit_Insurance_Card_Details", "Patient_Visit_Referral_Details"]
    },
    "EMR": {
        "keywords": ["emr", "prescription", "consultation", "clinical", "diagnosis", "chiefcomplaint", "vitals"],
        "tables": ["EMR", "Patient_Visit_Diagnosis", "Patient_Visit_Prescription", "Patient_Visit_Vitals"]
    },
    "Credit Note": {
        "keywords": ["creditnote", "credit_note", "refund", "debitnote"],
        "tables": ["Credit_Note", "Patient_Bill_Credit_Note", "CreditNoteHeader"]
    },
    "Masters": {
        "keywords": ["master", "masters", "department", "doctor", "service", "tariffmaster"],
        "tables": ["Department_Master", "Doctor_Master", "Service_Master", "Hospital_Master"]
    },
    "Insurance": {
        "keywords": ["insurance", "tpa", "claim", "insuranceplan", "eclaim"],
        "tables": ["Insurance_Company", "Insurance_Plans", "Insurance_Plan_Excluded_Items"]
    }
}


def scan_remote_files(directory: str) -> List[str]:
    """Retrieves all relative PHP file paths under a remote directory."""
    print(f"Scanning directory: {directory}...")
    cmd = f"find {directory} -type f -name '*.php' 2>/dev/null"
    out = sandboxed_ssh.execute_sandboxed_command(cmd, working_dir=REMOTE_BASE)
    files = [f.strip() for f in out.splitlines() if f.strip().endswith(".php")]
    return files


def scan_routes_for_module(module_name: str, keywords: List[str]) -> List[str]:
    """Finds route definitions in routes/ related to the module."""
    routes_found = []
    regex_pattern = "|".join([re.escape(k) for k in keywords])
    cmd = f"grep -rnEi -m 20 --include='*.php' 'Route::(get|post|put|delete|any)\\([^\"]*({regex_pattern})' {REMOTE_BASE}/routes/ 2>/dev/null | head -n 15"
    out = sandboxed_ssh.execute_sandboxed_command(cmd, working_dir=REMOTE_BASE)
    for line in out.splitlines():
        if line.strip():
            # Clean remote base path
            clean_line = line.replace(REMOTE_BASE + "/", "")
            routes_found.append(clean_line)
    return routes_found


def fetch_database_tables_and_columns(table_names: List[str]) -> Dict[str, List[Dict[str, str]]]:
    """Fetches real database table names and column schemas from MSSQL."""
    table_schemas = {}
    if not table_names:
        return table_schemas

    like_clauses = " OR ".join([f"TABLE_NAME LIKE '%{name}%'" for name in table_names])
    sql = f"""
    SELECT TOP 15 TABLE_NAME 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_TYPE = 'BASE TABLE' AND ({like_clauses})
    ORDER BY TABLE_NAME
    """
    try:
        tables_res = json.loads(autonomous_agent.execute_select_sql(sql))
        matched_tables = [r["TABLE_NAME"] for r in tables_res if "TABLE_NAME" in r]

        for tbl in matched_tables[:4]:  # Inspect top 4 tables per module
            col_sql = f"""
            SELECT TOP 10 COLUMN_NAME, DATA_TYPE, IS_NULLABLE 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = '{tbl}'
            ORDER BY ORDINAL_POSITION
            """
            cols_res = json.loads(autonomous_agent.execute_select_sql(col_sql))
            table_schemas[tbl] = cols_res
    except Exception as e:
        print(f"Database schema fetch notice: {e}")

    return table_schemas


def generate_module_knowledge():
    print("=" * 65)
    print(" EXTRACTING HIMES LARAVEL PROJECT KNOWLEDGE")
    print("=" * 65)

    all_controllers = scan_remote_files(f"{REMOTE_BASE}/app/Http/Controllers")
    all_models = scan_remote_files(f"{REMOTE_BASE}/app/Models")
    all_services = scan_remote_files(f"{REMOTE_BASE}/app/Services")

    md_content = []
    md_content.append("# HIMES Laravel Application Modules Knowledge Base\n")
    md_content.append(f"> Auto-extracted on demand from `{REMOTE_BASE}`. Contains verified Controllers, Models, Routes, and Database Table Schemas.\n")
    md_content.append("---\n")

    for module, config in TARGET_MODULES.items():
        print(f"\nProcessing Module: [{module}]...")
        keywords = config["keywords"]
        kw_regex = re.compile("|".join([re.escape(k) for k in keywords]), re.IGNORECASE)

        # 1. Match Controllers
        matched_controllers = [
            f.replace(REMOTE_BASE + "/", "") 
            for f in all_controllers 
            if kw_regex.search(os.path.basename(f))
        ][:8]

        # 2. Match Models
        matched_models = [
            f.replace(REMOTE_BASE + "/", "") 
            for f in all_models 
            if kw_regex.search(os.path.basename(f)) or kw_regex.search(f)
        ][:6]

        # 3. Match Services
        matched_services = [
            f.replace(REMOTE_BASE + "/", "") 
            for f in all_services 
            if kw_regex.search(os.path.basename(f)) or kw_regex.search(f)
        ][:4]

        # 4. Match Routes
        matched_routes = scan_routes_for_module(module, keywords)

        # 5. Fetch Table Schemas from MSSQL
        table_schemas = fetch_database_tables_and_columns(config["tables"])

        # Write to Markdown
        md_content.append(f"## 📌 Module: {module}\n")

        # Controllers
        md_content.append("### 1. Controllers")
        if matched_controllers:
            for c in matched_controllers:
                md_content.append(f"- `{c}`")
        else:
            md_content.append("- *No specific controller matching naming pattern directly.*")
        md_content.append("")

        # Models & Services
        md_content.append("### 2. Models & Services")
        if matched_models:
            md_content.append("**Models:**")
            for m in matched_models:
                md_content.append(f"- `{m}`")
        if matched_services:
            md_content.append("**Services:**")
            for s in matched_services:
                md_content.append(f"- `{s}`")
        if not matched_models and not matched_services:
            md_content.append("- *Direct Eloquent models / services not isolated or shared in CommonModel.*")
        md_content.append("")

        # Routes
        md_content.append("### 3. Mapped Web / API Routes")
        if matched_routes:
            for r in matched_routes:
                md_content.append(f"- `{r}`")
        else:
            md_content.append("- *Routes mapped dynamically or in centralized routes.php controller actions.*")
        md_content.append("")

        # Database Schema
        md_content.append("### 4. Database Tables & Columns (MSSQL)")
        if table_schemas:
            for tbl, cols in table_schemas.items():
                md_content.append(f"#### Table: `{tbl}`")
                md_content.append("| Column Name | Data Type | Nullable |")
                md_content.append("| :--- | :--- | :--- |")
                for c in cols:
                    md_content.append(f"| `{c.get('COLUMN_NAME')}` | {c.get('DATA_TYPE')} | {c.get('IS_NULLABLE')} |")
                md_content.append("")
        else:
            md_content.append("- *No matching schema returned from current database.*")
            md_content.append("")

        md_content.append("---\n")

    full_md = "\n".join(md_content)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(full_md)

    print("=" * 65)
    print(f" SUCCESS: Knowledge generated at: {OUTPUT_FILE}")
    print("=" * 65)


if __name__ == "__main__":
    generate_module_knowledge()
