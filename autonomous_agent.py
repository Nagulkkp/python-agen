import sys
import os
import re
import json
import time
import traceback

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from dotenv import load_dotenv
from ssh_sandbox import sandboxed_ssh
from guardrails import validate_sql_query, validate_command_directory_safety, SecurityException
from git_automation import SafeGitWorkflow

load_dotenv(override=True)

class AutonomousAgent:
    """
    Autonomous Developer & Data Agent for Nagul's HIMES Laravel Application (/L9/nagul/himes-ai).
    Behaves just like Antigravity:
    - Never uses static hardcoded Q&A.
    - Dynamically explores routes, controllers, and models.
    - Understands application business logic and prepares real-time SQL queries.
    - Safely executes queries on the live MSSQL database (SELECT only).
    - Can perform code edits, verify with 'php -l', and push safe Git sub-branches.
    """

    def __init__(self, project_dir: str = "/L9/nagul/himes-ai"):
        self.project_dir = project_dir
        self.git_workflow = SafeGitWorkflow(project_dir=project_dir)

    # ---------------------------------------------------------
    # TOOL 1: Search Codebase
    # ---------------------------------------------------------
    def search_code(self, query: str, subpath: str = "") -> str:
        """Searches the codebase using grep inside /L9/nagul/himes-ai."""
        try:
            clean_query = str(query or "").replace('"', '\\"').replace("'", "")
            if not clean_query:
                return "Error: Search query cannot be empty."
            clean_sub = str(subpath or "").strip().lstrip("/")
            target_dir = f"{self.project_dir}/{clean_sub}".rstrip("/")
            cmd = f'grep -rnI --exclude-dir={{storage,vendor,node_modules,.git}} -m 15 -E "{clean_query}" {target_dir} 2>/dev/null | head -n 25'
            out = sandboxed_ssh.execute_sandboxed_command(cmd, working_dir=self.project_dir)
            return out if out.strip() else f"No matches found for '{query}' in {subpath or 'project'}."
        except Exception as e:
            return f"Error searching code: {str(e)}"

    # ---------------------------------------------------------
    # TOOL 2: Find Route / Controller
    # ---------------------------------------------------------
    def find_route(self, keyword: str) -> str:
        """Finds routes and associated controllers in routes/routes.php or controllers."""
        try:
            clean_kw = str(keyword or "").replace('"', '').replace("'", "").strip()
            if not clean_kw:
                return "Error: Route keyword cannot be empty."
            cmd = f"grep -inE '{clean_kw}' /L9/nagul/himes-ai/routes/routes.php /L9/nagul/himes-ai/routes/*.php 2>/dev/null | head -n 15"
            out = sandboxed_ssh.execute_sandboxed_command(cmd, working_dir=self.project_dir)
            if out.strip():
                return out
            # Fallback to controller search
            cmd2 = f"find /L9/nagul/himes-ai/app/Http/Controllers/ -type f -iname '*{clean_kw}*.php' | head -n 10"
            out2 = sandboxed_ssh.execute_sandboxed_command(cmd2, working_dir=self.project_dir)
            return out2 if out2.strip() else f"No route or controller matching '{keyword}' found."
        except Exception as e:
            return f"Error finding route: {str(e)}"

    def search_in_file(self, file_path: str, keyword: str) -> str:
        """Searches for a keyword or pattern inside a specific file with line numbers."""
        try:
            if not file_path:
                return "Error: file_path must be specified."
            clean_path = str(file_path).strip().lstrip("/")
            if not clean_path.startswith("L9/nagul/himes-ai"):
                full_path = f"{self.project_dir}/{clean_path}"
            else:
                full_path = f"/{clean_path}"
            clean_kw = str(keyword or "").replace("'", "").replace('"', '').strip()
            cmd = f"grep -inC 2 '{clean_kw}' '{full_path}' 2>/dev/null | head -n 30"
            out = sandboxed_ssh.execute_sandboxed_command(cmd, working_dir=self.project_dir)
            return out if out.strip() else f"Keyword '{keyword}' not found in {file_path}."
        except Exception as e:
            return f"Error searching in file: {str(e)}"

    # ---------------------------------------------------------
    # TOOL 3: Read Code File
    # ---------------------------------------------------------
    def read_code(self, file_path: str, start_line: int = 1, line_count: int = 80) -> str:
        """Reads lines from a file in /L9/nagul/himes-ai with line numbers."""
        try:
            if not file_path:
                return "Error: file_path must be specified."
            clean_path = str(file_path).strip().lstrip("/")
            if not clean_path.startswith("L9/nagul/himes-ai"):
                full_path = f"{self.project_dir}/{clean_path}"
            else:
                full_path = f"/{clean_path}"

            start_line = max(1, int(start_line or 1))
            line_count = max(1, int(line_count or 80))
            end_line = start_line + line_count - 1
            cmd = f"awk 'NR>={start_line} && NR<={end_line} {{printf(\"%4d: %s\\n\", NR, $0)}}' '{full_path}'"
            out = sandboxed_ssh.execute_sandboxed_command(cmd, working_dir=self.project_dir)
            return out if out.strip() else f"File {file_path} is empty or does not exist."
        except Exception as e:
            return f"Error reading file: {str(e)}"

    # ---------------------------------------------------------
    # TOOL 4: Execute Safe Database Query (SELECT only)
    # ---------------------------------------------------------
    def execute_select_sql(self, sql_query: str) -> str:
        """
        Executes a SELECT query on MSSQL via Laravel DB connection inside Docker.
        STRICT GUARDRAIL: Only SELECT/WITH allowed. UPDATE/DELETE/DROP are strictly blocked!
        """
        try:
            if not sql_query or not isinstance(sql_query, str) or not sql_query.strip():
                return "Error: No valid SQL query provided to execute."

            clean_sql = sql_query.strip()
            # 1. Enforce SELECT-only guardrail
            validate_sql_query(clean_sql)

            # 2. Escape SQL for tinker execution
            escaped_sql = clean_sql.replace('\\', '\\\\').replace('"', '\\"').replace('$', '\\$')
            tinker_cmd = (
                f'docker exec nagul php /var/www/html/himes-ai/artisan tinker --execute="'
                f'\\$res = DB::select(\\"{escaped_sql}\\"); '
                f'echo json_encode(\\$res);"'
            )
            out = sandboxed_ssh.execute_sandboxed_command(tinker_cmd, working_dir=self.project_dir)
            out_str = str(out or "").strip()
            return out_str if out_str else "[] (Query returned 0 rows)"
        except SecurityException as se:
            return f"SECURITY BLOCKED: {str(se)}"
        except Exception as e:
            return f"Query Execution Error: {str(e)}"

    # ---------------------------------------------------------
    # TOOL 5: Execute Laravel Tinker Expression
    # ---------------------------------------------------------
    def execute_tinker(self, php_code: str) -> str:
        """Runs a safe read-only Laravel expression in tinker."""
        try:
            if not php_code or not isinstance(php_code, str) or not php_code.strip():
                return "Error: No valid PHP code provided to execute."

            # Guard against destructive tinker commands
            lower = php_code.lower()
            for bad in ["delete(", "update(", "drop(", "truncate(", "insert("]:
                if bad in lower:
                    return f"SECURITY BLOCKED: Tinker code contains forbidden operation '{bad}'."

            escaped = php_code.strip().replace('\\', '\\\\').replace('"', '\\"').replace('$', '\\$')
            tinker_cmd = f'docker exec nagul php /var/www/html/himes-ai/artisan tinker --execute="echo json_encode({escaped});"'
            out = sandboxed_ssh.execute_sandboxed_command(tinker_cmd, working_dir=self.project_dir)
            out_str = str(out or "").strip()
            return out_str if out_str else "(Tinker executed with no return value)"
        except Exception as e:
            return f"Tinker Error: {str(e)}"

    # ---------------------------------------------------------
    # TOOL 6: Run Safe Shell Command (Inside Nagul directory)
    # ---------------------------------------------------------
    def run_safe_command(self, command: str) -> str:
        """Runs a safe shell command inside /L9/nagul/himes-ai."""
        try:
            validate_command_directory_safety(command, allowed_dir="/L9/nagul")
            out = sandboxed_ssh.execute_sandboxed_command(command, working_dir=self.project_dir)
            return out.strip() if out.strip() else "(Command executed successfully)"
        except SecurityException as se:
            return f"SECURITY BLOCKED: {str(se)}"
        except Exception as e:
            return f"Shell Error: {str(e)}"

    # ---------------------------------------------------------
    # TOOL 7: Edit Code File (with syntax check & rollback)
    # ---------------------------------------------------------
    def edit_file(self, file_path: str, search_text: str, replacement_text: str) -> str:
        """
        Edits a code file inside /L9/nagul/himes-ai.
        Automatically verifies syntax with 'php -l' and rolls back if an error occurs.
        """
        try:
            clean_path = file_path.strip().lstrip("/")
            if not clean_path.startswith("L9/nagul/himes-ai"):
                full_path = f"{self.project_dir}/{clean_path}"
            else:
                full_path = f"/{clean_path}"

            # Backup original file first
            backup_path = f"{full_path}.bak_agent"
            sandboxed_ssh.execute_sandboxed_command(f"cp '{full_path}' '{backup_path}'")

            # Read current content
            cur_content = sandboxed_ssh.execute_sandboxed_command(f"cat '{full_path}'")
            if search_text not in cur_content:
                sandboxed_ssh.execute_sandboxed_command(f"rm -f '{backup_path}'")
                return f"Error: target search_text was not found in {file_path}."

            new_content = cur_content.replace(search_text, replacement_text, 1)

            # Write updated content safely
            escaped_content = new_content.replace("'", "'\\''")
            sandboxed_ssh.execute_sandboxed_command(f"cat << 'EOF_AGENT' > '{full_path}'\n{new_content}\nEOF_AGENT")

            # Check PHP syntax if it is a php file
            if full_path.endswith(".php"):
                chk = sandboxed_ssh.execute_sandboxed_command(f"php -l '{full_path}'")
                if "No syntax errors detected" not in chk:
                    # Rollback!
                    sandboxed_ssh.execute_sandboxed_command(f"cp '{backup_path}' '{full_path}'")
                    sandboxed_ssh.execute_sandboxed_command(f"rm -f '{backup_path}'")
                    return f"Syntax Error Detected: {chk}. Automatically rolled back file to original state!"

            sandboxed_ssh.execute_sandboxed_command(f"rm -f '{backup_path}'")
            return f"File {file_path} successfully updated and verified (php -l passed)."
        except Exception as e:
            return f"Edit Error: {str(e)}"

    # ---------------------------------------------------------
    # TOOL 8: Git Sub-Branch, Commit, and Push
    # ---------------------------------------------------------
    def git_commit_and_push(self, branch_name: str, commit_message: str) -> str:
        """Creates a sub-branch (fix/...), commits changes, and pushes to remote GitHub."""
        try:
            clean_branch = branch_name if branch_name.startswith(("fix/", "feature/", "task/")) else f"fix/{branch_name}"
            # Check status first
            status = sandboxed_ssh.execute_sandboxed_command("git status --porcelain", working_dir=self.project_dir)
            if not status.strip():
                return "No changes detected to commit."

            # Create branch, commit, and push
            self.git_workflow.create_sub_branch(clean_branch)
            push_out = self.git_workflow.commit_and_push(clean_branch, commit_message)
            return f"Successfully created sub-branch '{clean_branch}', committed with message '{commit_message}', and pushed to remote GitHub!\n{push_out}"
        except SecurityException as se:
            return f"SECURITY BLOCKED: {str(se)}"
        except Exception as e:
            return f"Git Error: {str(e)}"

    # ---------------------------------------------------------
    # LLM Interaction (Claude / GPT-4o / Gemini)
    # ---------------------------------------------------------
    def call_llm(self, prompt: str, system_prompt: str) -> str:
        """Invokes Gemini 3.5/3.8 or OpenAI or Claude with robust fallback."""
        gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        openai_key = os.getenv("OPENAI_API_KEY")
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")

        stop_seqs = ["Observation:", "\nObservation:"]

        # 1. Claude 3.5 Sonnet if available
        if anthropic_key and not anthropic_key.startswith("your_"):
            try:
                import anthropic
                client = anthropic.Anthropic(api_key=anthropic_key)
                res = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=2048,
                    system=system_prompt,
                    stop_sequences=stop_seqs,
                    messages=[{"role": "user", "content": prompt}]
                )
                return res.content[0].text
            except Exception:
                pass

        # 2. OpenAI GPT-4o if available
        if openai_key and not openai_key.startswith("your_"):
            try:
                from openai import OpenAI
                client = OpenAI(api_key=openai_key)
                res = client.chat.completions.create(
                    model=os.getenv("OPENAI_MODEL", "gpt-4o"),
                    stop=stop_seqs,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ]
                )
                return res.choices[0].message.content
            except Exception:
                pass

        # 3. Google Gemini (Fast and free)
        if gemini_key and not gemini_key.startswith("your_"):
            import google.genai as genai
            from google.genai import types
            client = genai.Client(api_key=gemini_key)
            config = types.GenerateContentConfig(
                temperature=0.1
            )
            models_to_try = [
                "gemini-3.1-flash-lite",
                "gemini-3.1-flash-lite-preview",
                "gemini-3.5-flash-lite",
                "gemini-3.7-flash",
                "gemini-flash-lite-latest",
                "gemini-3-flash-preview"
            ]
            custom_model = os.getenv("GEMINI_MODEL")
            if custom_model:
                models_to_try.insert(0, custom_model)

            last_ex = None
            for m in models_to_try:
                try:
                    full_content = f"{system_prompt}\n\nTask:\n{prompt}"
                    res = client.models.generate_content(model=m, contents=full_content, config=config)
                    if res and res.candidates:
                        cand = res.candidates[0]
                        parts_text = "".join([p.text for p in cand.content.parts if hasattr(p, "text") and p.text]).strip()
                        if parts_text:
                            return parts_text
                except Exception as e:
                    last_ex = e
                    err_str = str(e)
                    if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                        time.sleep(1.5)
                    continue

        raise ValueError(f"No working AI LLM connection available: {last_ex}. Please check API keys in .env.")

    # ---------------------------------------------------------
    # AUTONOMOUS AGENTIC LOOP (ReAct Loop)
    # ---------------------------------------------------------
    def run(self, user_task: str, context: dict = None) -> dict:
        """
        Runs an autonomous ReAct reasoning loop.
        Investigates codebase dynamically, runs queries, makes edits, and delivers the answer.
        NO static or hardcoded queries.
        """
        system_prompt = """You are Nagul's Autonomous AI Developer & Database Agent integrated inside HIMES (/L9/nagul/himes-ai).
You operate just like an advanced agentic assistant (like Antigravity):
- When the user asks a question about ANY feature, screen, or data:
  1. DO NOT guess or use hardcoded assumptions.
  2. Use your tools to find the relevant route/controller/model in the codebase or query the database directly.
  3. Formulate the exact SQL query (SELECT ONLY) needed.
  4. Execute the query live on the database using execute_select_sql.
  5. Return the actual live facts cleanly to the user in friendly Tanglish / Tamil + English.
- If the user asks for code changes / bug fixes:
  1. Find the file and inspect the code.
  2. Edit the file using `edit_file`.
  3. Verify syntax with php -l (built into edit_file).
  4. Create a sub-branch (fix/...) and push to git using `git_commit_and_push`.
  5. Never auto-merge into main or development.

STRICT SAFETY RULES:
1. Only SELECT queries are permitted on the database. NEVER execute UPDATE, DELETE, DROP, or INSERT.
HIMES ARCHITECTURE & DATABASE SCHEMA GUIDANCE:
- Project Directory: /L9/nagul/himes-ai
- Database: Microsoft SQL Server (MSSQL).
- HIMES Core Tables & Column Mappings:
  * Patient Details:
    - `Patient_Basic_Details pbd` (MRN column: `pbd.Permanent_MRN_No`, Serial: `pbd.Patient_Basic_Details_Serial_No`)
    - `Patient_Basic_Encript_Details pbed` (Names: `pbed.Patient_First_Name`, `pbed.Patient_Middle_Name`, `pbed.Patient_Last_Name`, Mobile: `pbed.Contact_Phone_Mobile`, Emirates ID: `pbed.Emirates_Id`)
    - Join on: `pbd.Patient_Basic_Details_Serial_No = pbed.Patient_Basic_Details_Serial_No`
  * Patient Visits / Encounters:
    - `Patient_Visit_Basic_Details pvbd`
    - Visit Number column: `pvbd.Permanent_Visit_No` (e.g. 16923) or `pvbd.Patient_Visit_Basic_Details_Serial_No`
    - Patient link: `pvbd.Patient_Basic_Details_Serial_No`
    - Visit Date: `pvbd.Patient_Visit_Registered_Date_Time`
    - Status check: `pvbd.Active_Status = 'A' AND pvbd.Visit_Cancellation_Flag = 'N'`
    - CRITICAL: NEVER rely on `pvbd.Is_Visit_Completely_Billed` to determine billing status! In HIMES, this column is often NULL or not updated.
  * Billing & Invoices (HOW TO CHECK BILLING STATUS):
    - ALWAYS check `Patient_Bill_Header pbh` via `pbh.Patient_Visit_Basic_Details_Serial_No = pvbd.Patient_Visit_Basic_Details_Serial_No AND pbh.Bill_Cancellation_Flag = 'N'`.
    - If a record exists in `Patient_Bill_Header`:
      * If `pbh.Is_Bill_Finalized = 'C'`: The visit is **Billed and Finalized**! (Bill No: `pbh.Bill_No`, Invoice No: `pbh.Permanent_Invoice_No`, Net Value: `pbh.Bill_Net_Value`).
      * If `pbh.Is_Bill_Finalized != 'C'`: Bill created but in progress / pending finalization.
    - If NO record exists in `Patient_Bill_Header`: The visit is Unbilled / Pending.
  * Patient Visit History (e.g. "last 10 visit details" for an MRN):
    - Query `Patient_Visit_Basic_Details pvbd` joining `Patient_Bill_Header pbh` ordered by `pvbd.Patient_Visit_Registered_Date_Time DESC`.
    - If the user asks for "last 10 visit details" but patient only has 1 or fewer visits registered in total, explicitly state: "MRN <MRN>-ku motham 1 visit mattum thaan iruku" (or count found) and display the details.
    - For each visit, clearly show: Visit No, Visit Date, and Billing Status (e.g. Finalized with Bill No and Net Value).
  * Deposits & Receipts (Payment Details in HIMES UI editPatientBilling):
    - Deposits: `Patient_Visit_Deposits pvd` (linked via `pvd.Patient_Visit_Basic_Details_Serial_No = pvbd.Patient_Visit_Basic_Details_Serial_No`, columns: `pvd.Deposit_Amount_Collected`, `pvd.Bill_Amount_Adjusted_Against_Deposit`, `pvd.Balance_Deposit_Amount`). If no records or amounts are 0, tell user deposit ethuvum illa (No records found).
    - Payments Received / Receipt Grid:
      In the HIMES UI screen (`editPatientBilling`):
      * The column header "Receipt No" shows `Patient_Bill_Header_Payments_Received_Serial_No` from `Patient_Bill_Header_Payments_Received pbpr` (e.g. 55875).
      * The column header "Amt Recd" / "Amnt Received" shows `pbpr.Bill_Amount_Paid_By_Patient` (e.g. 20.00 AED) - this is the actual Receipt Amount paid by the patient!
      * Card Details: `rpr.Card_Reference_Details` (e.g. 4534) from `Receipts_For_Payments_Received rpr` where `rpr.Patient_Bill_Header_Payments_Received_Serial_No = pbpr.Patient_Bill_Header_Payments_Received_Serial_No`.
      * Payment Date: `pbpr.Payment_Type_Date` (e.g. 15-10-2026).
    - CRITICAL DISTINCTION:
      * Bill Total Net Value (e.g. 110.00 AED) = Total service cost.
      * Insurance Claim Amount (e.g. 90.00 AED) = `pbh.Bill_Insured_Value`.
      * Patient Share / Receipt Amount (e.g. 20.00 AED) = `pbpr.Bill_Amount_Paid_By_Patient`.
      * When user asks about receipts or bill payment, ALWAYS clearly specify:
        1. Bill Total: Net Value (e.g. 110.00 AED, with Insurance Claim 90.00 AED).
        2. Receipt Details: Receipt No (e.g. 55875, from `pbpr.Patient_Bill_Header_Payments_Received_Serial_No`), Receipt Amount Received (e.g. 20.00 AED paid via Card 4534).
        3. Deposit: Deposit used or No deposit found (0.00 AED).
      NEVER confuse Bill Total (110.00) with Receipt Amount (20.00), and always use the UI Receipt No (`pbpr.Patient_Bill_Header_Payments_Received_Serial_No`).
  * Patient Services (Services ordered / taken in a visit):
    - Table: `Patient_Visit_Services pvs`
    - Links to Visit: `pvs.Patient_Visit_Basic_Details_Serial_No = pvbd.Patient_Visit_Basic_Details_Serial_No`
    - Links to Service Master:
      `JOIN Service_USSDB sussdb ON sussdb.Service_USSDB_Serial_No = pvs.Service_USSDB_Serial_No`
      `JOIN Service s ON s.Service_Serial_No = sussdb.Service_Serial_No`
    - MANDATORY FILTER FOR ACTIVE SERVICES:
      `WHERE pvs.Patient_Visit_Service_Cancellation_Flag = 'N' AND pvs.Active_Status = 'A'`
      CRITICAL: Any rows with `pvs.Patient_Visit_Service_Cancellation_Flag = 'D'` or `pvs.Active_Status = 'N'` are CANCELLED / DELETED services. NEVER count or list cancelled services!
    - Exact SQL Query to get Active Services for a Visit:
      ```sql
      SELECT 
          s.CPT_Code,
          s.Service_Internal_Code,
          s.Service_Description
      FROM Patient_Visit_Basic_Details pvbd
      JOIN Patient_Visit_Services pvs ON pvs.Patient_Visit_Basic_Details_Serial_No = pvbd.Patient_Visit_Basic_Details_Serial_No
      JOIN Service_USSDB sussdb ON sussdb.Service_USSDB_Serial_No = pvs.Service_USSDB_Serial_No
      JOIN Service s ON s.Service_Serial_No = sussdb.Service_Serial_No
      WHERE pvbd.Permanent_Visit_No = '<Visit_No>'
        AND pvs.Patient_Visit_Service_Cancellation_Flag = 'N'
        AND pvs.Active_Status = 'A'
      ```
    - In your answer, state the exact active count and list each service with its CPT Code and Description (matching the Billing screen `addPatientBilling`).
    - NEVER EVER hallucinate service names (like Consultation, CBC, ESR) if a query fails or returns empty. Always execute the exact query above and report the real database facts!
  * Service Price Calculation Logic (How `addPatientBilling` / `PatientBillingGetController.php` Fetches Price):
    - A service can have multiple price records over time; price MUST be determined by the most recent Effective/Start Date (`<= GETDATE()`).
    - 1. CASH / NON-INSURANCE PATIENTS:
      * Table: `Service_Rate_For_Non_Insurance` (`SRFNI`)
      * Rate Column: `SRFNI.Service_Base_Rate`
      * Date Column: `SRFNI.Service_Rate_For_Non_Insurance_Start_Date`
      * Query:
        ```sql
        SELECT TOP 1 SRFNI.Service_Base_Rate
        FROM Service_Rate_For_Non_Insurance SRFNI
        WHERE SRFNI.Service_USSDB_Serial_No = <Service_USSDB_Serial_No>
          AND SRFNI.Is_It_Service_Resource_Drug = 'S'
          AND SRFNI.Active_Status = 'A'
          AND SRFNI.Partner_Company_Serial_No IS NULL
          AND CAST(SRFNI.Service_Rate_For_Non_Insurance_Start_Date AS DATE) <= CAST(GETDATE() AS DATE)
        ORDER BY SRFNI.Service_Rate_For_Non_Insurance_Start_Date DESC
        ```
    - 2. INSURANCE PATIENTS:
      * Table: `Service_Rate_For_Insurance` (`SRFNI`)
      * Rate Column: `SRFNI.Service_Base_Rate`
      * Date Column: `SRFNI.Service_Rate_For_Insurance_Start_Date`
      * Key Filters: `Insurance_Company_Serial_No = <insurance_id>`, `Patient_Income_Network_Universal_Groups_Serial_No = <pinug_id>`, `Patient_Payment_Type_Serial_No = <payment_type_id>`
      * Query:
        ```sql
        SELECT TOP 1 SRFNI.Service_Base_Rate
        FROM Service_Rate_For_Insurance SRFNI
        WHERE SRFNI.Service_USSDB_Serial_No = <Service_USSDB_Serial_No>
          AND SRFNI.Insurance_Company_Serial_No = <Insurance_Company_Serial_No>
          AND SRFNI.Patient_Income_Network_Universal_Groups_Serial_No = <PINUG_Serial_No>
          AND SRFNI.Active_Status = 'A'
          AND SRFNI.Partner_Company_Serial_No IS NULL
          AND CAST(SRFNI.Service_Rate_For_Insurance_Start_Date AS DATE) <= CAST(GETDATE() AS DATE)
        ORDER BY SRFNI.Service_Rate_For_Insurance_Start_Date DESC
        ```
    - 3. DOCTOR / RESOURCE BASE RATE:
      * Table: `Resource_rate_For_Insurance`
      * Column: `Resource_Base_Rate`
      * Date Filter: `CAST(Resource_Rate_For_Insurance_Start_Date AS DATE) <= CAST(GETDATE() AS DATE) ORDER BY Resource_Rate_For_Insurance_Start_Date DESC`
    - SUMMARY: Always check if the visit/patient is CASH or INSURANCE, filter by the relevant company/network, and always select `TOP 1 ... WHERE Start_Date <= GETDATE() ORDER BY Start_Date DESC` to get the current applicable price!
  * Inventory Item Price Calculation Logic (Pharmacy Drugs & Consumables in `addPatientBilling`):
    - Just like services, inventory item prices depend on Cash vs Insurance and MUST be picked using the most recent Effective Date (`<= GETDATE()`).
    - 1. CASH / NON-INSURANCE ITEM PRICE:
      * Table: `Stock_Item_Price`
      * Rate Column: `Selling_Price`
      * Date Column: `Stock_Item_Price_Effective_Date`
      * Query:
        ```sql
        SELECT TOP 1 sip.Selling_Price
        FROM Stock_Item_Price sip
        WHERE sip.Item_Master_Serial_No = <Item_Master_Serial_No>
          AND sip.Active_Status = 'A'
          AND CAST(sip.Stock_Item_Price_Effective_Date AS DATE) <= CAST(GETDATE() AS DATE)
        ORDER BY sip.Stock_Item_Price_Effective_Date DESC
        ```
    - 2. INSURANCE ITEM PRICE:
      * Table: `Stock_Item_Insurance_Price` (and company-based `Company_Based_Inventory_Insurance_Item_Price`)
      * Rate Column: `Insurance_Gross_Amount`
      * Date Column: `Effective_Date`
      * Query:
        ```sql
        SELECT TOP 1 siip.Insurance_Gross_Amount
        FROM Stock_Item_Insurance_Price siip
        WHERE siip.Item_Master_Serial_No = <Item_Master_Serial_No>
          AND siip.Active_Status = 'A'
          AND CAST(siip.Effective_Date AS DATE) <= CAST(GETDATE() AS DATE)
        ORDER BY siip.Effective_Date DESC
        ```
  * Bed Management Price Calculation Logic (IPD Beds / Rooms in `addPatientBilling` / `getBillingBedManagementGrid`):
    - A Bed is tracked in `Patient_Visit_Resources pvr` (Active check: `pvr.Active_Status = 'A' AND pvr.Resource_Allocation_Cancellation_Flag = 'N'`).
    - Bed is linked to its service via:
      `Resource r ON r.Resource_Serial_No = pvr.Resource_Serial_No`
      `Resource_Service rs ON rs.Resource_Serial_No = pvr.Resource_Serial_No`
      `Service s ON s.Service_Serial_No = rs.Service_Serial_No`
      `Service_USSDB sussdb ON sussdb.Service_Serial_No = s.Service_Serial_No`
    - Bed Pricing Rules: `Price_Rule_For_Resources` (`Resource_Type_Category_Flag = 'B'`, `Effective_Start_Date <= GETDATE()`).
    - 1. CASH / NON-INSURANCE BED RATE:
      * Table: `Service_Rate_For_Non_Insurance` (linked via Bed's `Service_USSDB_Serial_No`)
      * Rate Column: `Service_Base_Rate`
      * Query:
        ```sql
        SELECT TOP 1 srfni.Service_Base_Rate
        FROM Service_Rate_For_Non_Insurance srfni
        WHERE srfni.Service_USSDB_Serial_No = <Bed_Service_USSDB_Serial_No>
          AND srfni.Active_Status = 'A'
          AND srfni.Partner_Company_Serial_No IS NULL
          AND CAST(srfni.Service_Rate_For_Non_Insurance_Start_Date AS DATE) <= CAST(GETDATE() AS DATE)
        ORDER BY srfni.Service_Rate_For_Non_Insurance_Start_Date DESC
        ```
    - 2. INSURANCE BED RATE:
      * Table: `Resource_Rate_For_Insurance` (or `Service_Rate_For_Insurance`)
      * Rate Column: `Resource_Base_Rate` / `Service_Base_Rate`
      * Query:
        ```sql
        SELECT TOP 1 rrfi.Resource_Base_Rate
        FROM Resource_Rate_For_Insurance rrfi
        WHERE rrfi.Service_USSDB_Serial_No = <Bed_Service_USSDB_Serial_No>
          AND rrfi.Insurance_Company_Serial_No = <Insurance_Company_Serial_No>
          AND rrfi.Active_Status = 'A'
          AND CAST(rrfi.Resource_Rate_For_Insurance_Start_Date AS DATE) <= CAST(GETDATE() AS DATE)
        ORDER BY rrfi.Resource_Rate_For_Insurance_Start_Date DESC
        ```
- PHARMACY PATIENTS, MRNs, BILLS & OP PHARMACY SCREEN:
  * In HIMES, Pharmacy patients can be registered separately with MRNs starting with 'PHAR' (e.g., PHAR2120, PHAR2119, PHAR2118):
    - Table: `Pharmacy_Patient_Basic_Details`
      * Column: `Pharmacy_Permanent_MRN_No` (e.g., 'PHAR2120') or `Pharmacy_Temporary_MRN_No`
      * Demographic Columns: `Patient_First_Name`, `Patient_Last_Name`, `Contact_Phone_Mobile`
    - Table: `Pharmacy_Patient_Visit_Basic_Details`
      * Column: `Pharmacy_Permanent_Visit_No` (e.g., 3074)
      * Primary Key: `Pharmacy_Patient_Visit_Basic_Details_Serial_No`
    - Table: `Pharmacy_Patient_Bill_Header`
      * Column: `Pharmacy_Patient_Visit_Basic_Details_Serial_No`
      * Invoices: `Permanent_Invoice_No`, `Bill_Net_Value`, `Bill_Gross_Value`, `Bill_Date`
    - Table: `Pharmacy_Patient_Bill_Detail_Items`
      * Linked via `Stock_Item_Price_Serial_No` -> `Stock_Item_Price` -> `Item_Master` (`Item_Description`)
      * Quantities & Amounts: `Service_Quantity`, `Derived_Net_Value`, `Patient_Share_Value`
  * Global View of OP Pharmacy:
    - Route: `/viewGlobalOPPharmacy`
    - Controller: `GlobalViewIPPharmacyController@viewGlobalIPPharmacy` (Data method: `getGlobalFilterIPPharmacy`)
    - Displays both Outpatient Clinic Prescriptions (`type = 'HA'`) and Direct Pharmacy Encounters (`type = 'PH'`).
  * When searching for an MRN:
    - ALWAYS check BOTH `patient_basic_details` (general hospital MRNs) AND `Pharmacy_Patient_Basic_Details` (for Pharmacy MRNs starting with PHAR)!

- Best Strategy for Queries:
  1. Formulate the exact SELECT query based on the core tables above.
  2. You MUST execute the query using `execute_select_sql` to get the real live facts before giving the Final Answer!
  3. State the factual answers (e.g. Patient Name, Bill No, Net Amount, Billed status: pannittaanga / pannala, Deposit status, UI Receipt No, Receipt Amount, Active Services, Inventory Item prices, and Bed rates) clearly in friendly Tanglish.

CONVERSATION CONTINUITY & CONTEXT INHERITANCE:
- Check ACTIVE APPLICATION SCREEN in Context! If the user is on a specific screen (e.g. `/viewGlobalOPPharmacy` - GLOBAL VIEW OF OP PHARMACY), tailor your explanation to that screen and controller.
- IMPORTANT DISTINCTION:
  * If the user is asking about a general HIMES Module, Screen, Menu, or Workflow (e.g., "pharmacy module ah paaru", "billing module pathi sollu", "price list menu enga iruku", "intha screen-a explain pannu", or referring to the ACTIVE APPLICATION SCREEN), do NOT force or assume a past visit_no from an old chat turn! Instead, explain the module, active screen (/viewGlobalOPPharmacy, GlobalViewIPPharmacyController, etc.), or ask what specific patient/visit on that screen they want to check.
  * Only inherit active visit_no / mrn when the user is explicitly asking a visit-level follow-up (e.g., "intha visit-oda bill", "service price", "receipt details", "deposit iruka").
- If the user asks a visit-level follow-up WITHOUT repeating the number, use the active visit_no / MRN from Context immediately.

TOOLS AVAILABLE:
1. `search_code(query="keyword", subpath="")`
2. `find_route(keyword="route_or_controller_keyword")`
3. `search_in_file(file_path="relative_path", keyword="string")`
4. `read_code(file_path="relative_path", start_line=1, line_count=60)`
5. `execute_select_sql(sql_query="SELECT ...")`
6. `execute_tinker(php_code="echo json_encode(...);")`
7. `run_safe_command(command="shell_command")`
8. `edit_file(file_path="relative_path", search_text="old", replacement_text="new")`
9. `git_commit_and_push(branch_name="fix/name", commit_message="summary")`

FORMAT TO FOLLOW:
In each step, respond with:
Thought: <what I need to investigate or do next>
Action: <one of the tool names above>
Action Input: <valid JSON object containing arguments for that tool>

When you have completed all actions and have the live result, output:
Final Answer: <Your clear, friendly response to Nagul in Tanglish / Tamil + English, stating factual numbers and results directly>
"""

        context_guidance = ""
        if context:
            # 1. Screen / Page Awareness
            screen_info = []
            if context.get("page_title"):
                screen_info.append(f"Screen Title: {context.get('page_title')}")
            if context.get("current_path"):
                screen_info.append(f"Route Path: {context.get('current_path')}")
            if context.get("selected_text"):
                screen_info.append(f"User Highlighted Text: '{context.get('selected_text')}'")
            if screen_info:
                context_guidance += f"\nACTIVE APPLICATION SCREEN: {', '.join(screen_info)}."

            # 2. Active conversation entities
            active_ents = context.get("active_entities", {})
            ents_list = [f"{k.upper()}: {v}" for k, v in active_ents.items() if v]
            if ents_list:
                context_guidance += f"\nACTIVE ENTITIES IN RECENT CHAT: {', '.join(ents_list)}."

            # 3. Hybrid knowledge
            vk = context.get("valkey_knowledge")
            if vk:
                vk_str = json.dumps(vk, ensure_ascii=False) if isinstance(vk, (dict, list)) else str(vk)
                context_guidance += f"\nHIMES KNOWLEDGE RETRIEVAL:\n{vk_str[:1200]}"

            # 4. Recent turns
            turns = context.get("previous_chat_turns", [])
            if turns:
                context_guidance += "\nRECENT CHAT HISTORY:\n"
                for t in turns[-2:]:
                    context_guidance += f"- User: {t.get('user')}\n  Assistant: {str(t.get('agent'))[:160]}...\n"

        history = [
            f"User Request: {user_task}\n"
            f"Context: {context_guidance.strip() if context_guidance else json.dumps(context or {})}\n"
            f"Begin your investigation!"
        ]
        actions_taken = []
        max_iterations = 10

        for step in range(max_iterations):
            prompt_input = "\n\n".join(history)
            raw_llm = self.call_llm(prompt_input, system_prompt)
            llm_response = (raw_llm or "").strip()
            if not llm_response.startswith("Thought:") and not llm_response.startswith("Final Answer:") and not llm_response.startswith("Action:"):
                llm_response = f"Thought: {llm_response}"
            try:
                print(f"\n[Agent Step {step+1}]\n{llm_response}\n")
            except Exception:
                try:
                    safe_log = llm_response.encode("ascii", errors="replace").decode("ascii")
                    print(f"\n[Agent Step {step+1}]\n{safe_log}\n")
                except Exception:
                    pass

            # Truncate any hallucinated Observation
            for delim in ["\nObservation:", "Observation:"]:
                if delim in llm_response and not llm_response.startswith(delim):
                    llm_response = llm_response.split(delim, 1)[0].strip()

            # If Action appears before Final Answer, prioritize executing the Action
            if "Action:" in llm_response and "Final Answer:" in llm_response:
                action_idx = llm_response.find("Action:")
                fa_idx = llm_response.find("Final Answer:")
                if action_idx < fa_idx:
                    llm_response = llm_response[:fa_idx].strip()

            # Check if Agent reached Final Answer (with no pending Action)
            if "Final Answer:" in llm_response and "Action:" not in llm_response:
                final_text = llm_response.split("Final Answer:", 1)[-1].strip()
                return {
                    "status": "success",
                    "reply": final_text,
                    "actions_taken": actions_taken,
                    "steps": step + 1
                }

            # Parse Action and Action Input (handles 'Action Input:' and 'ActionInput:' and inline)
            thought_match = re.search(r"Thought:\s*(.*?)(?=Action\s*:|$)", llm_response, re.DOTALL | re.IGNORECASE)
            thought = thought_match.group(1).strip() if thought_match else ""

            action, raw_input = None, "{}"
            action_match = re.search(r"Action:\s*([a-zA-Z0-9_]+)", llm_response, re.IGNORECASE)
            if action_match:
                action = action_match.group(1).strip()
                after_action = llm_response[action_match.end():].strip()

                # Extract JSON block between first { and last }
                fb = after_action.find("{")
                lb = after_action.rfind("}")
                if fb != -1 and lb != -1 and lb > fb:
                    raw_input = after_action[fb:lb+1].strip()
                elif "Action" in llm_response and "Input:" in llm_response:
                    input_split = re.split(r"Action\s*Input:\s*", llm_response, flags=re.IGNORECASE)
                    if len(input_split) > 1:
                        raw_input = input_split[-1].strip()

            if not action:
                if llm_response.strip():
                    return {
                        "status": "success",
                        "reply": llm_response,
                        "actions_taken": actions_taken,
                        "steps": step + 1
                    }
                else:
                    history.append("System: Empty response received. Please decide your next Action or provide Final Answer.")
                    continue

            # Parse Action Arguments
            args = {}
            try:
                clean_json = raw_input
                if "```json" in clean_json:
                    clean_json = clean_json.split("```json", 1)[-1].split("```", 1)[0].strip()
                elif "```" in clean_json:
                    clean_json = clean_json.split("```", 1)[-1].split("```", 1)[0].strip()

                args = json.loads(clean_json)
                if not isinstance(args, dict):
                    args = {"query": str(args)}
            except Exception:
                args = {"query": raw_input.strip("\"'")}

            # Execute Tool
            obs = ""
            action_record = {"step": step + 1, "thought": thought, "tool": action, "args": args}
            actions_taken.append(action_record)

            try:
                if action == "search_code":
                    q = args.get("query") or args.get("arg") or str(raw_input)
                    sub = args.get("subpath", "")
                    obs = self.search_code(q, sub)
                elif action == "find_route":
                    k = args.get("keyword") or args.get("query") or str(raw_input)
                    obs = self.find_route(k)
                elif action == "search_in_file":
                    fp = args.get("file_path") or args.get("path")
                    kw = args.get("keyword") or args.get("query") or ""
                    obs = self.search_in_file(fp, kw)
                elif action == "read_code":
                    fp = args.get("file_path") or args.get("path")
                    sl = int(args.get("start_line", 1))
                    lc = int(args.get("line_count", 60))
                    obs = self.read_code(fp, sl, lc)
                elif action == "execute_select_sql":
                    q = args.get("sql_query") or args.get("query")
                    if not q and args:
                        q = list(args.values())[0]
                    if not q:
                        q = raw_input
                    obs = self.execute_select_sql(str(q or ""))
                elif action == "execute_tinker":
                    c = args.get("php_code") or args.get("code") or str(raw_input)
                    obs = self.execute_tinker(c)
                elif action == "run_safe_command":
                    cmd = args.get("command") or args.get("cmd") or str(raw_input)
                    obs = self.run_safe_command(cmd)
                elif action == "edit_file":
                    fp = args.get("file_path")
                    old = args.get("search_text")
                    new = args.get("replacement_text")
                    obs = self.edit_file(fp, old, new)
                elif action == "git_commit_and_push":
                    b = args.get("branch_name", "fix/agent-task")
                    m = args.get("commit_message", "Autonomous agent update")
                    obs = self.git_commit_and_push(b, m)
                else:
                    obs = f"Unknown tool: {action}. Please choose from the available tools."
            except Exception as ex:
                obs = f"Tool execution failed: {str(ex)}"

            # Append step to history
            history.append(f"Step {step + 1}:\nThought: {thought}\nAction: {action}({json.dumps(args)})\nObservation:\n{obs}\n\nThought:")

        # If max iterations reached, synthesize answer from history
        final_prompt = (
            f"User Task: {user_task}\n\n"
            f"Here is the investigation log:\n" + "\n\n".join(history[-4:]) + "\n\n"
            f"Instructions:\n"
            f"Provide a direct, final answer to Nagul summarizing the findings and factual data in friendly Tanglish / Tamil + English."
        )
        final_summary = self.call_llm(final_prompt, "You are Nagul's autonomous AI assistant.")
        return {
            "status": "success",
            "reply": final_summary,
            "actions_taken": actions_taken,
            "steps": max_iterations
        }

autonomous_agent = AutonomousAgent()
