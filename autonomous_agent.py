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

def clean_agent_thought(t: str) -> str:
    """
    Strips internal LLM scratchpad reasoning, ReAct thoughts, rules analysis,
    and planning steps, ensuring only the genuine user-facing answer is delivered.
    """
    if not t or not isinstance(t, str):
        return t
    
    clean = t.strip()

    # 1. Standard ReAct Delimiter
    if "Final Answer:" in clean:
        clean = clean.split("Final Answer:", 1)[-1].strip()

    # 2. Match 'Let's formulate...' transition and take everything after it
    formulate_m = re.search(r'Let\'s\s+formulate[^\n]*?[\.\):]\s*(?=[✅⚠️ℹ️🩺\*\#A-Za-z])', clean, flags=re.IGNORECASE)
    if formulate_m:
        clean = clean[formulate_m.end():].strip()

    # 3. Match general transition phrases: 'Here is the response...', 'Final response:'
    trans_m = re.search(r'(?:Here\s+is\s+the\s+final|Final\s+Response:?|Final\s+Answer:?)[^\n]*\n*', clean, flags=re.IGNORECASE)
    if trans_m:
        clean = clean[trans_m.end():].strip()

    # 4. If there is a status emoji (✅, ⚠️, ℹ️, 🩺) and preamble before it contains scratchpad/thought keywords
    emoji_m = re.search(r'[\n\s]+([✅⚠️ℹ️🩺])', clean)
    if emoji_m:
        preamble = clean[:emoji_m.start()]
        if any(w in preamble.lower() for w in ['rules', 'himes', 'architecture', 'policy', 'cash patient', 'thought', 'user mode', 'explain pannunga']):
            clean = clean[emoji_m.start(1):].strip()

    # 5. Strip any remaining Thought prefixes or rules analysis
    clean = re.sub(
        r'^(?:Thought:|[A-Za-z\s]+Thought:)?\s*(?:This based on|The user is asking|According to the rules|I should|Let me check)[\s\S]*?(?=(?:✅|⚠️|ℹ️|🩺|\*\*Appointment|\*\*Status|[A-Za-z0-9_-]+\s*screen|Intha|Indru|Inaikki|Aama|Illa|Vanakkam|Neenga|Hello|Hi))',
        '',
        clean,
        flags=re.IGNORECASE
    ).strip()
    clean = re.sub(r'^Thought:\s*', '', clean, flags=re.IGNORECASE).strip()
    return clean

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
    def call_llm(self, prompt: str, system_prompt: str, image_parts: list = None) -> str:
        """Invokes Gemini 3.5/3.8 or OpenAI or Claude with robust fallback and vision support."""
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

        # 3. Google Gemini (Fast, free, and multimodal)
        if gemini_key and not gemini_key.startswith("your_"):
            import google.genai as genai
            from google.genai import types
            client = genai.Client(api_key=gemini_key)
            config = types.GenerateContentConfig(
                temperature=0.1
            )
            models_to_try = [
                "gemini-flash-lite-latest",
                "gemini-3.5-flash-lite",
                "gemini-3-flash-preview",
                "gemini-3.1-flash-lite",
                "gemini-3.5-flash"
            ]
            custom_model = os.getenv("GEMINI_MODEL")
            if custom_model:
                models_to_try.insert(0, custom_model)

            last_ex = None
            for m in models_to_try:
                try:
                    text_content = f"{system_prompt}\n\nTask:\n{prompt}"
                    if image_parts:
                        full_content = [text_content] + image_parts
                    else:
                        full_content = text_content

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
  5. Return the actual live facts cleanly to the user in the matching language (Tamil / Tanglish / Arabic / English).

UNIVERSAL MULTILINGUAL PROCESSING (ANY WORLD LANGUAGE - TAMIL, ARABIC, HINDI, MALAYALAM, TELUGU, RUSSIAN, FRENCH, SPANISH, TAGALOG, ENGLISH, ETC.):
- You possess native, fluent comprehension of ALL human languages and scripts:
  * Pure Tamil (தமிழ்), Tanglish
  * Arabic (العربية)
  * Hindi (हिन्दी), Hinglish
  * Malayalam (മലയാളം), Manglish
  * Telugu (తెలుగు), Kannada (ಕನ್ನಡ), Urdu (اردو), Bengali (বাংলা)
  * Russian (Русский), French (Français), Spanish (Español), Tagalog (Filipino), German (Deutsch)
  * English (Global Standard)
- Core Processing Rules:
  1. Accurately understand the clinical, billing, and administrative intent regardless of how the user expresses it in ANY language, slang, or script.
  2. Map concepts directly to HIMES SQL Conditions:
     - Unbilled / Pending (e.g. "bill aagadha", "பில் ஆகாத", "غير مفوتر", "बिना बिल", "ബിൽ ചെയ്യാത്ത", "non facturé", "no facturado", "неоплаченный") -> `pvs.Is_Service_Billed = 'N'`
     - Tests / Services / Procedures (e.g. "test", "சிகிச்சை", "பரிசோதனை", "فحوصات", "जांच", "പരിശോധന", "examens", "pruebas", "анализы") -> Join `Patient_Visit_Services`
     - Prescriptions / Drugs (e.g. "marunthu", "மருந்து", "أدوية", "दवाइयां", "മരുന്നുകൾ", "médicaments", "medicamentos", "лекарства") -> Join `Patient_Visit_Drugs_Prescribed`
     - Lab Orders & Results (e.g. "lab", "இரத்த பரிசோதனை", "نتائج التحاليل", "लैब टेस्ट", "ലാബ് ഫലങ്ങൾ", "résultats de labo") -> Join `Patient_Visit_Lab_Order` & `Lab_Order_Item_Result`
  3. Formulate a 100% Read-Only MSSQL `SELECT` query using `WITH(NOLOCK)`.
  4. Execute the query live on the database using `execute_select_sql`.
  5. Under `Final Answer:`, output a concise 1-2 sentence intent summary in the EXACT SAME LANGUAGE the user queried in (or friendly Tanglish/Hinglish/Manglish if the user used transliteration).
  6. DO NOT manually retype long multi-row tables into your answer; our Zero-Token presentation layer will automatically bind the structured action card and collapsible breakdown table to your summary!

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
  * Patient Details & Demographics:
    - MANDATORY RULE: Whenever patient details, visit lists, or demographics are asked or listed, ALWAYS include the MRN Number (`pbd.Permanent_MRN_No`)!
    - `Patient_Basic_Details pbd` (MRN column: `pbd.Permanent_MRN_No`, Serial: `pbd.Patient_Basic_Details_Serial_No`)
    - `Patient_Basic_Encript_Details pbed` (Names: `pbed.Patient_First_Name`, `pbed.Patient_Middle_Name`, `pbed.Patient_Last_Name`, Mobile: `pbed.Contact_Phone_Mobile`, Emirates ID: `pbed.Emirates_Id`)
    - Join on: `pbd.Patient_Basic_Details_Serial_No = pbed.Patient_Basic_Details_Serial_No`
    - When user asks for patient lists (e.g. today's or yesterday's visits): Output columns must be: `MRN Number`, `Patient Name`, `Visit No`, `Time / Date`.
  * Patient Visits / Encounters:
    - `Patient_Visit_Basic_Details pvbd`
    - Visit Number column: `pvbd.Permanent_Visit_No` (e.g. 16923) or `pvbd.Patient_Visit_Basic_Details_Serial_No`
    - Patient link: `pvbd.Patient_Basic_Details_Serial_No`
    - Visit Date: `pvbd.Patient_Visit_Registered_Date_Time`
    - Status check: `pvbd.Active_Status = 'A' AND pvbd.Visit_Cancellation_Flag = 'N'`
    - CRITICAL: NEVER rely on `pvbd.Is_Visit_Completely_Billed` to determine billing status! In HIMES, this column is often NULL or not updated.
  * Billing & Invoices (AUTHORITATIVE HIMES viewGlobalBilling STANDARD):
    - RULE 1: ONLY show Billing Status when the user EXPLICITLY asks about billing status, bills, or invoices! When user asks for general patient lists, today's visits, or non-billing info, DO NOT attach billing status or service breakdown!
    - RULE 2: Exact HIMES Billing Status Values from `GlobalViewBillingController.php` (`viewGlobalBilling`):
      * If `pbh.Bill_Cancellation_Flag = 'Y'` -> Status is **`Cancelled`**
      * If `pbh.Is_Bill_Finalized = 'C'` -> Status is **`Closed`** (Invoice is finalized & closed!)
      * If `pbh.Is_Bill_Finalized = 'Y'` -> Status is **`Finalised`**
      * If `pbh.Permanent_Invoice_No IS NOT NULL` and `Is_Bill_Finalized != 'C'` -> Status is **`Billed`** (Invoice generated!)
      * If NO record exists in `Patient_Bill_Header` (or services are unbilled) -> Status is **`Pending`**
    - Global Billing Status Query (Matching HIMES `viewGlobalBilling` Grid exactly):
      ```sql
      SELECT 
          pvbd.Permanent_Visit_No,
          pbd.Permanent_MRN_No,
          pbed.Patient_First_Name,
          pbed.Patient_Last_Name,
          pbh.Permanent_Invoice_No,
          CASE 
              WHEN pbh.Bill_Cancellation_Flag = 'Y' THEN 'Cancelled'
              WHEN pbh.Is_Bill_Finalized = 'C' THEN 'Closed'
              WHEN pbh.Is_Bill_Finalized = 'Y' THEN 'Finalised'
              WHEN pbh.Permanent_Invoice_No IS NOT NULL THEN 'Billed'
              ELSE 'Pending'
          END AS Billing_Status
      FROM Patient_Visit_Basic_Details pvbd WITH(NOLOCK)
      JOIN Patient_Basic_Details pbd WITH(NOLOCK) ON pvbd.Patient_Basic_Details_Serial_No = pbd.Patient_Basic_Details_Serial_No
      JOIN Patient_Basic_Encript_Details pbed WITH(NOLOCK) ON pbd.Patient_Basic_Details_Serial_No = pbed.Patient_Basic_Details_Serial_No
      LEFT JOIN Patient_Bill_Header pbh WITH(NOLOCK) ON pbh.Patient_Visit_Basic_Details_Serial_No = pvbd.Patient_Visit_Basic_Details_Serial_No AND pbh.Bill_Cancellation_Flag = 'N'
      WHERE CAST(pvbd.Patient_Visit_Registered_Date_Time AS DATE) = CAST(GETDATE() AS DATE)
        AND pvbd.Active_Status = 'A' AND pvbd.Visit_Cancellation_Flag = 'N'
      ORDER BY pvbd.Permanent_Visit_No
      ```
  * Patient Visit History (e.g. "last 10 visit details" for an MRN):
    - Query `Patient_Visit_Basic_Details pvbd` joining `Patient_Bill_Header pbh` ordered by `pvbd.Patient_Visit_Registered_Date_Time DESC`.
    - If the user asks for "last 10 visit details" but patient only has 1 or fewer visits registered in total, explicitly state: "MRN <MRN>-ku motham 1 visit mattum thaan iruku" (or count found) and display the details.
    - For each visit, clearly show: Visit No, Visit Date, and Billing Status.
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
  * Global Hospital Configuration & Installation Parameters:
    - Table: `Installation_Parameters`
    - Core Columns:
      * `Insurance_Method` (e.g. 'DHA', 'HAAD', 'WASEEL') -> Health authority insurance submission method.
      * `Insurance_Claim_URL` (e.g. 'https://dhpo.eclaimlink.ae/ValidateTransactions.asmx')
      * `Insurance_Label_Text` (e.g. 'Ins/Corp')
      * `Hospital_Name`, `Tax_Identification_Number`
    - Query to check Insurance Method:
      ```sql
      SELECT TOP 1 Insurance_Method, Insurance_Claim_URL, Insurance_Label_Text FROM Installation_Parameters
      ```
  * Prior Authorization & Pre-Auth Status:
    - Table: `prior_status`
    - Core Columns: `Prior_Status_Code`, `Prior_Status_Name`, `Identification_Color_Code`, `Active_Status`
    - Query: `SELECT * FROM prior_status`
- PHARMACY PATIENTS, MRNs, BILLS & OP PHARMACY SCREEN:
  * In HIMES, Pharmacy patients can be registered separately with MRNs starting with 'PHAR' (e.g., PHAR2120, PHAR2119, PHAR2118):
    - Table: `Pharmacy_Patient_Basic_Details` (Columns: `Pharmacy_Permanent_MRN_No`, `Pharmacy_Temporary_MRN_No`, `Patient_First_Name`, `Patient_Last_Name`, `Contact_Phone_Mobile`)
    - Table: `Pharmacy_Patient_Visit_Basic_Details` (Columns: `Pharmacy_Permanent_Visit_No`, `Pharmacy_Patient_Visit_Basic_Details_Serial_No`, `Patient_Visit_Registered_Date_Time`)
    - Table: `Pharmacy_Patient_Bill_Header` (Columns: `Permanent_Invoice_No`, `Bill_Net_Value`, `Bill_Gross_Value`, `Bill_Date`, `Is_Bill_Finalized`)
    - Table: `Pharmacy_Patient_Bill_Detail_Items` (Linked via `Stock_Item_Price_Serial_No` -> `Stock_Item_Price` -> `Item_Master` (`Item_Description`), `Service_Quantity`, `Derived_Net_Value`, `Patient_Share_Value`)
  * Global View of OP Pharmacy (/viewGlobalOPPharmacy):
    - Route: `/viewGlobalOPPharmacy`
    - Primary Controller: `GlobalViewIPPharmacyController@viewGlobalIPPharmacy` (Data method: `getGlobalFilterIPPharmacy`)
    - Displays two tabs:
      1. Clinic Tab (`Type = 'HA'`): Outpatient prescriptions ordered by doctors during clinic consultations.
         - Exact Query for Clinic Tab Records:
           ```sql
           SELECT COUNT(DISTINCT pvbd.Permanent_Visit_No) as clinic_records
           FROM Patient_Visit_Drugs_Prescribed pvdp with(nolock)
           JOIN Patient_Visit_Basic_Details pvbd with(nolock)
             ON pvdp.Patient_Visit_Basic_Details_Serial_No = pvbd.Patient_Visit_Basic_Details_Serial_No
             AND pvbd.Is_EMR_In_Progress = 'Y'
             AND pvbd.Visit_Cancellation_Flag = 'N'
           JOIN Patient_Basic_Details pbd with(nolock)
             ON pbd.Patient_Basic_Details_Serial_No = pvbd.Patient_Basic_Details_Serial_No
             AND pbd.Active_Status = 'A'
           WHERE pvdp.Active_Status = 'A'
             AND CAST(pvbd.Patient_Visit_Registered_Date_Time AS DATE) >= '<from_date>'
             AND CAST(pvbd.Patient_Visit_Registered_Date_Time AS DATE) <= '<to_date>'
           ```
      2. Pharmacy Tab (`Type = 'PH'`): Direct walk-in pharmacy patient encounters.
         - Exact Query for Pharmacy Tab Records:
           ```sql
           SELECT COUNT(DISTINCT pvbd.Pharmacy_Permanent_Visit_No) as pharmacy_records
           FROM Pharmacy_Patient_Visit_Basic_Details pvbd with(nolock)
           JOIN Pharmacy_Patient_Basic_Details pbd with(nolock)
             ON pbd.Pharmacy_Patient_Basic_Details_Serial_No = pvbd.Pharmacy_Patient_Basic_Details_Serial_No
           WHERE CAST(pvbd.Patient_Visit_Registered_Date_Time AS DATE) >= '<from_date>'
             AND CAST(pvbd.Patient_Visit_Registered_Date_Time AS DATE) <= '<to_date>'
           ```
    - CALENDAR MONTH / DATE RANGE RULES:
      * When the user asks about "last month", "this month", "today", or date filters:
        - In HIMES, calculate the exact start and end date for that calendar period (e.g. `YYYY-MM-01` to `YYYY-MM-last_day`).
        - ALWAYS run the live COUNT queries dynamically to fetch real-time counts from MSSQL.
        - NEVER use hardcoded or guessed numbers; report only verified rows returned by the live database!
  * When searching for an MRN:
    - ALWAYS check BOTH `patient_basic_details` (general hospital MRNs) AND `Pharmacy_Patient_Basic_Details` (for Pharmacy MRNs starting with PHAR)!
- DOCTOR ROSTER, AVAILABILITY & APPOINTMENT SCHEDULING:
  * Table: `Resource_Parent` (Doctor Master)
    - Primary Key: `Resource_Parent_Serial_No`
    - Doctor Name: `Resource_Name` (e.g. 'DR ADEL QUTTAINAH', 'DR. AHMED')
    - Specialty Code: `Default_Speciality_Code` (e.g. 'GS', 'GP', 'ANES', 'DERM')
    - Flags: `Active_Status = 'A'` AND `Show_In_Appointment = 'Y'` AND `Is_Resource_Human = 'Y'`
  * Table: `Resource_Non_Availability` (Doctor Leaves, Breaks, Conference Blocks)
    - `Resource_Parent_Serial_No`
    - Date Filters: `Resource_Non_Availability_Start_Date_Time` and `Resource_Non_Availability_End_Date_Time`
    - Status: `Active_Status = 'A'`
  * Standard Query to find Today's Available Doctors:
    ```sql
    SELECT DISTINCT TOP 15
        rp.Resource_Parent_Serial_No,
        rp.Resource_Name AS Doctor_Name,
        rp.Default_Speciality_Code AS Speciality,
        CASE WHEN EXISTS (
            SELECT 1 FROM Resource_Non_Availability rna WITH(NOLOCK)
            WHERE rna.Resource_Parent_Serial_No = rp.Resource_Parent_Serial_No
              AND CAST(GETDATE() AS DATE) BETWEEN CAST(rna.Resource_Non_Availability_Start_Date_Time AS DATE) AND CAST(rna.Resource_Non_Availability_End_Date_Time AS DATE)
              AND rna.Active_Status = 'A'
        ) THEN 'On Leave' ELSE 'Available' END AS Doctor_Status
    FROM Resource_Parent rp WITH(NOLOCK)
    WHERE rp.Active_Status = 'A' AND rp.Show_In_Appointment = 'Y'
    ORDER BY rp.Resource_Name
    ```

- LABORATORY (LIS) & RADIOLOGY (RIS) WORKFLOWS:
  * LIS (Lab Orders & Results):
    - Table: `Patient_Visit_Lab_Order` (Lab orders linked to patient visit)
    - Table: `Lab_Order_Item_Result` (Numeric results, reference ranges, panic alerts)
    - Table: `Lab_Specimen_Details` (Barcodes & accessioning)
    - Controllers: `LabOrderController`, `BarcodeController`, `LISResultEntryController`, `LISVerificationController`
    - Key Route: `/viewGlobalLIS`
  * RIS (Radiology Orders & PACS/DICOM):
    - Table: `Patient_Visit_Radiology_Order` (Imaging requests)
    - Table: `Radiology_Report_Details` (Radiologist diagnosis, impression, findings)
    - Controller: `EmrRadiologyReportController`, `RadiologyOrderController`
    - Key Route: `/viewGlobalRIS`

- 100+ EMR SPECIALTY PANELS & CLINICAL DOCUMENTATION:
  * Tables: `Patient_Visit_Clinical_Notes`, `Patient_Visit_ICD_Codes` (Primary & Secondary ICD-10), `Patient_Visit_Vitals`, `Patient_Visit_Allergy_Details`
  * Controllers: `EMRVisitEntryPanelController`, `EMRCCHPIChiefcomplaintController`, `EMRAllergiesController`, `EmrVitalFactorsController`, `EMRVisitSummarynewController`
  * Panels: Dental (`DEN`), Anesthesia (`AnesthesiaRecordFormPanelController`), Physiotherapy (`PHY`), Urgent Care (`URC`), Cardiology, OB/GYN, Pediatrics, Fall Risk.
  * Key Routes: `/emrVisitEntryPanel`, `/viewEMRWaitingList`, `/emrChiefComplaint`, `/emrAllergies`.

- 400+ MASTERS, TARIFFS & PRICE LISTS:
  * Services & Insurance Tariffs: `InsurancePriceListManagementController` (`/priceListManagement`), tables: `Service_Rate_For_Non_Insurance`, `Resource_Rate_For_Insurance`, `Service_USSDB`.
  * Pharmacy Inventory Pricing: `InventoryPriceListManagementController` (`/ViewInventoryPriceListManagement`), tables: `Stock_Item_Price`, `Item_Master`.
  * Bed & Resource Rules: `PriceRuleForResourcesController` (`/PriceRuleForResources`), table: `Price_Rule_For_Resources`.
  * Master Logs: `AllMasterLogsController` (audits all changes across 400+ master setups).

- INVOICE POSTING, FINANCIAL LEDGER & ERP EXPORT:
  * Tables: `Ledger_Transactions`, `Patient_Bill_Header`, `Pharmacy_Patient_Bill_Header`, `GL_Account_Master`
  * Controllers: `GlobalViewInvoicePostController` (`/viewGlobalInvoicePost`), `HMCTallyInvoiceExportController` (Tally XML), `QuickBookExportController` / `PharmacyQuickBookExportController` (QuickBooks export).
  * Rule: Bills must have `Is_Bill_Finalized = 'C'` before ledger posting (`Is_Bill_Posted_To_Ledger = 'Y'`).

- CREDIT NOTES & REFUNDS:
  * Tables: `Credit_Note_Header`, `Credit_Note_Details`, `Patient_Bill_Refund_Details`, `Pharmacy_Refund_Bill_Header`
  * Controllers: `GlobalViewCreditNoteController` (`/globalViewCreditNote`), `DebitCreditNoteController` (`/debitCreditNote`).
  * Manages service cancellations, deposit refunds, and tax invoice reversals.

- CLAIMS MANAGEMENT & E-CLAIMS:
  * Tables: `claim_details`, `claim_detail_icd`, `claim_details_submitted`, `claim_batch_header`, `claim_remittance_advice` (ERA 835)
  * Controllers: `AutoEclaimPostController` (`/eclaimManagement`), `ClaimBulkReSubmissionController`, `BranchEClaimController`
  * Submissions to DHPO, Shafafiya, Waseel, Malaffi; parses 835 Remittance Advice for paid vs denied amounts.

- CRON JOBS & AUTOMATED BACKGROUND TASKS:
  * Scheduled in `app/Console/Kernel.php`:
    - `ReportScheduleCron`: Every minute dispatches scheduled MIS reports (`Himes_Reports_Schedule_Details`).
    - `AppointmentUpdateNoShow`: Every 10 mins auto-flags missed appointments.
    - `AutoEclaimPostCron`: Automated nightly insurance claim batch generation.
    - `QuickBookPost` & `PharmcyQuickBookPost`: Daily at 5:00 AM posts revenue batches.
    - `JobExecutionLogs`: Tracks status of all background jobs.

- APPOINTMENTS, DOCTOR SCHEDULES & TRANSACTION QUERIES (LIVE MSSQL TRANSACTION EXECUTION):
  * CRITICAL DISTINCTION (STATIC WORKFLOW VS LIVE DATA):
    - If the user asks about the overall concept, workflow, or SOP ("how does appointment work?", "explain ASM flow", "what are appointment status colors/codes?", "explain follow-up rules"):
      -> Use the Valkey / ChromaDB appointment workflow skill to explain the architectural concept clearly.
    - If the user asks for ANY TRANSACTIONAL or OPERATIONAL DATA (e.g. "Dr. John-ku inaikki appointment irukka?", "how many appointments booked today?", "check appointment status for MRN 3004383", "who is on leave today?", "today's cancelled appointments", "is slot 10:30 available?"):
      -> NEVER return static workflow text or general explanations!
      -> Understand the ASM workflow to identify the live tables (`Patient_Appointment`, `Resource_Parent`, `Resource_Non_Availability`, `Patient_Basic_Details`, `Patient_Basic_Encript_Details`, `Patient_Visit_Appointments`).
      -> Formulate the exact MSSQL SELECT query using `execute_select_sql`.
      -> Fetch live data from the database, analyze the rows, and present accurate, real-time facts to the user!
  * Key Live Appointment Queries:
    1. Patient Appointment Details (by MRN, Patient Name, or Visit Date):
       ```sql
       SELECT 
           pa.Patient_Appointment_Serial_No,
           pa.Patient_Appointment_Date,
           pa.Appointment_Start_Time,
           pa.Appointment_End_Time,
           pa.Appointment_Status_Type_Code,
           ast.Appointment_Status_Type_Name,
           rp.Resource_Parent_Name as Doctor_Name,
           pbd.Permanent_MRN_No,
           pbed.Patient_First_Name,
           pbed.Patient_Last_Name,
           pva.Patient_Visit_Basic_Details_Serial_No
       FROM Patient_Appointment pa WITH(NOLOCK)
       LEFT JOIN Appointment_Status_Type ast WITH(NOLOCK) ON pa.Appointment_Status_Type_Code = ast.Appointment_Status_Type_Code
       LEFT JOIN Resource_Parent rp WITH(NOLOCK) ON pa.Resource_Parent_Serial_No = rp.Resource_Parent_Serial_No
       LEFT JOIN Patient_Basic_Details pbd WITH(NOLOCK) ON pa.Patient_Basic_Details_Serial_No = pbd.Patient_Basic_Details_Serial_No
       LEFT JOIN Patient_Basic_Encript_Details pbed WITH(NOLOCK) ON pbd.Patient_Basic_Details_Serial_No = pbed.Patient_Basic_Details_Serial_No
       LEFT JOIN Patient_Visit_Appointments pva WITH(NOLOCK) ON pa.Patient_Appointment_Serial_No = pva.Patient_Appointment_Serial_No
       WHERE pa.Active_Status = 'A'
         AND (pbd.Permanent_MRN_No = '<MRN>' OR pa.Patient_Appointment_Date = CAST(GETDATE() AS DATE))
       ORDER BY pa.Patient_Appointment_Date DESC, pa.Appointment_Start_Time ASC
       ```
    2. Doctor Leaves & Non-Availability:
       ```sql
       SELECT 
           rp.Resource_Parent_Name,
           rna.Resource_Non_Availability_Start_Date_Time,
           rna.Resource_Non_Availability_End_Date_Time,
           rna.Reason_Code
       FROM Resource_Non_Availability rna WITH(NOLOCK)
       JOIN Resource_Parent rp WITH(NOLOCK) ON rna.Resource_Parent_Serial_No = rp.Resource_Parent_Serial_No
       WHERE rna.Active_Status = 'A'
         AND CAST(rna.Resource_Non_Availability_End_Date_Time AS DATE) >= CAST(GETDATE() AS DATE)
       ORDER BY rna.Resource_Non_Availability_Start_Date_Time ASC
       ```

- PATIENT REGISTRATION & VISIT TRANSACTION QUERIES (LIVE MSSQL TRANSACTION EXECUTION):
  * CRITICAL DISTINCTION (STATIC WORKFLOW VS LIVE DATA):
    - If the user asks about the overall concept, workflow, or SOP ("how does patient registration work?", "Simple vs Detailed registration difference", "how is copay calculated?", "what are edit lockouts?"):
      -> Use the Valkey / ChromaDB registration workflow skill to explain the concept.
      -> In User Mode, use clean, intuitive, hospital business language without technical table names.
      -> In Developer Mode, provide full technical schema, controllers, and routes.
    - If the user asks for ANY TRANSACTIONAL or OPERATIONAL DATA (e.g. "how many patients registered today?", "MRN 3004383 registration details", "is patient Prakash registered yesterday?", "who registered visit 16923?"):
      -> NEVER return static workflow text or general explanations!
      -> Understand the registration workflow to identify the live tables (`Patient_Basic_Details`, `Patient_Basic_Encript_Details`, `Patient_Visit_Basic_Details`, `Patient_Visit_Insurance_Card_Details`, `Patient_Visit_Resources`, `Patient_Identification_Details`).
      -> Formulate the exact MSSQL SELECT query using `execute_select_sql`.
      -> Fetch live data from MSSQL, analyze the rows, and present accurate, real-time facts to the user!
  * Key Live Registration Queries:
    1. Patient Registration & Insurance Details by MRN:
       ```sql
       SELECT 
           pbd.Permanent_MRN_No,
           pbed.Patient_First_Name,
           pbed.Patient_Last_Name,
           pbd.Gender_Code,
           pbd.Patient_DOB,
           pbed.Contact_Phone_Mobile,
           pvbd.Permanent_Visit_No,
           pvbd.Patient_Visit_Registered_Date_Time,
           ic.Insurance_Company_Name,
           ip.Insurance_Plan_Name,
           pvicd.Insurance_Card_No,
           pvicd.Card_Expiry_Date
       FROM Patient_Basic_Details pbd WITH(NOLOCK)
       JOIN Patient_Basic_Encript_Details pbed WITH(NOLOCK) ON pbd.Patient_Basic_Details_Serial_No = pbed.Patient_Basic_Details_Serial_No
       LEFT JOIN Patient_Visit_Basic_Details pvbd WITH(NOLOCK) ON pbd.Patient_Basic_Details_Serial_No = pvbd.Patient_Basic_Details_Serial_No AND pvbd.Active_Status = 'A'
       LEFT JOIN Patient_Visit_Insurance_Card_Details pvicd WITH(NOLOCK) ON pvicd.Patient_Visit_Basic_Details_Serial_No = pvbd.Patient_Visit_Basic_Details_Serial_No
       LEFT JOIN Insurance_Company ic WITH(NOLOCK) ON ic.Insurance_Company_Serial_No = pvicd.Insurance_Company_Serial_No
       LEFT JOIN Insurance_Plans ip WITH(NOLOCK) ON ip.Insurance_Plans_Serial_No = pvicd.Insurance_Plan_Serial_No
       WHERE pbd.Permanent_MRN_No = '<MRN>'
       ORDER BY pvbd.Patient_Visit_Basic_Details_Serial_No DESC
       ```
    2. Today's Registrations Count & Breakdown:
       ```sql
       SELECT 
           vet.Visit_Encounter_Type_Code,
           vet.Visit_Encounter_Type_Description,
           COUNT(*) as Total_Visits
       FROM Patient_Visit_Basic_Details pvbd WITH(NOLOCK)
       LEFT JOIN Visit_Encounter_Type vet WITH(NOLOCK) ON pvbd.Visit_Encounter_Type_Serial_No = vet.Visit_Encounter_Type_Serial_No
       WHERE CAST(pvbd.Patient_Visit_Registered_Date_Time AS DATE) = CAST(GETDATE() AS DATE)
         AND pvbd.Active_Status = 'A'
         AND pvbd.Visit_Cancellation_Flag = 'N'
       GROUP BY vet.Visit_Encounter_Type_Code, vet.Visit_Encounter_Type_Description
       ```

- Best Strategy for Queries:
  1. Formulate the exact SELECT query based on the core tables above.
  3. State the factual answers (e.g. Patient Name, Bill No, Net Amount, Billed status, Deposit status, UI Receipt No, Receipt Amount, Active Services, Inventory Item prices, and Bed rates) clearly in the USER'S EXACT LANGUAGE (English if asked in English, Tanglish if asked in Tanglish).

CONVERSATION CONTINUITY & CONTEXT INHERITANCE:
- Check ACTIVE APPLICATION SCREEN in Context!
- HIMES ROUTE PARAMETER ARCHITECTURE:
  * In routes like `/addPatientBilling/{pbdno}/{pvbdno}` or `/editPatientBilling/{pbdno}/{pvbdno}` or `/addBillDeposit/{pbdno}/{pvbdno}`:
    - `{pbdno}` is `Patient_Basic_Details_Serial_No` (the patient's master serial).
    - `{pvbdno}` is `Patient_Visit_Basic_Details_Serial_No` (the visit ID).
    - NEVER query `Patient_Visit_Basic_Details_Serial_No = {pbdno}`!
    - Resolve exact MRN & Visit No:
      `SELECT pbd.Permanent_MRN_No, pvbd.Permanent_Visit_No FROM Patient_Visit_Basic_Details pvbd JOIN Patient_Basic_Details pbd ON pvbd.Patient_Basic_Details_Serial_No = pbd.Patient_Basic_Details_Serial_No WHERE pvbd.Patient_Visit_Basic_Details_Serial_No = {pvbdno}`
- STRICT EXACT MATCHING MANDATE (CRITICAL RULE):
  * `Permanent_MRN_No` and `Permanent_Visit_No` MUST ALWAYS be queried with exact equality (`=`). NEVER use `LIKE '%...'` or partial/substring matching!
  * Partial matching causes serious patient cross-contamination and retrieves wrong records.
  * When querying visit services, bills, or deposits, ALWAYS verify that the visit belongs to that exact patient:
    `pvbd.Patient_Basic_Details_Serial_No = pbd.Patient_Basic_Details_Serial_No`
- MULTI-TURN ENTITY INHERITANCE:
  * When the user asks about "intha visit", "billing details", "unbilled services", "bill pannama iruka service", or "service details" WITHOUT repeating the MRN or Visit No:
    - You MUST use the active MRN and Visit No from `ACTIVE PATIENT & VISIT CONTEXT` and `RECENT CHAT HISTORY`!
    - Query unbilled services using:
      ```sql
      SELECT pvs.Patient_Visit_Services_Serial_No, s.Service_Description, s.CPT_Code, s.Service_Internal_Code, pvs.Service_Quantity, pvs.Patient_Payment_Type_Code
      FROM Patient_Visit_Services pvs WITH(NOLOCK)
      JOIN Patient_Visit_Basic_Details pvbd WITH(NOLOCK) ON pvs.Patient_Visit_Basic_Details_Serial_No = pvbd.Patient_Visit_Basic_Details_Serial_No
      JOIN Patient_Basic_Details pbd WITH(NOLOCK) ON pvbd.Patient_Basic_Details_Serial_No = pbd.Patient_Basic_Details_Serial_No
      JOIN Service_USSDB sussdb WITH(NOLOCK) ON sussdb.Service_USSDB_Serial_No = pvs.Service_USSDB_Serial_No
      JOIN Service s WITH(NOLOCK) ON s.Service_Serial_No = sussdb.Service_Serial_No
      WHERE pvbd.Permanent_Visit_No = '<active_visit_no>'
        AND pbd.Permanent_MRN_No = '<active_mrn>'
        AND pvs.Active_Status = 'A'
        AND pvs.Patient_Visit_Service_Cancellation_Flag = 'N'
        AND pvs.Is_Service_Billed = 'N'
      ```
- MULTI-TURN CONVERSATIONAL CONTINUITY & CO-REFERENCE RESOLUTION (CRITICAL MANDATE):
  * Review the FULL SESSION CHAT HISTORY in Context carefully!
  * If the user mentions patient details (Name, MRN, Visit No) in Turn 1 or earlier, and later asks follow-up questions (e.g., "matha details kudu", "avanoda bill", "service list", "unbilled details", "intha patient-oda visit") WITHOUT repeating the MRN or patient name:
    - You MUST look back across all previous turns in the session, extract that exact patient's MRN or Visit No, and use it immediately to query the live database!
  * If the user refers to "first ketta question" or "first question":
    - Look back at Turn 1 to see the exact initial question asked, and execute the live database query to provide the factual answer to that exact question!
  * NEVER ask the user to re-enter or repeat patient details that are already present in the chat history!
- TIES & EXTREMA HANDLING MANDATE (CRITICAL RULE FOR 'HIGHEST AMOUNT', 'ATHIGAMAANA AMOUNT', 'MAX BILL'):
  * When asked for the highest or lowest bill/invoice amount (e.g. "entha invoice athiga amount ku bill pannirukaanga", "highest amount", "lowest bill"):
    - NEVER arbitrarily select `TOP 1` if multiple invoices/visits have the same highest amount!
    - ALWAYS return ALL invoices that share the maximum amount using `TOP 1 WITH TIES` or `WHERE Bill_Net_Value = (SELECT MAX(Bill_Net_Value) ...)`!
    - Example: If two invoices have 6502.00 AED (e.g. Visit 17089 [Inv 9747] & Visit 17091 [Inv 9749]), you MUST list BOTH invoices and both visits!
- GROUP CO-REFERENCE & AMBIGUITY RESOLUTION ('ATHULA', 'ORU VISIT THAAN IRUKKA?'):
  * When a previous turn found multiple patients or visits matching a search filter (e.g., 3 patients/visits named 'Prakash': 17082, 17083, 17087), and user asks:
    - "athula entha invoice ku bill pannirukaanga" -> "athula" refers to ALL 3 Prakash visits found! Check all 3 visits together (`IN ('17082', '17083', '17087')`), and report each.
    - "oru visit tha irukka?" -> Clarify both:
      "MRN <MRN>-ku 1 visit thaan irukku, aana nethu Prakash nu total-ah 3 visits irunthathu: Visit 17082, 17083, 17087 (ivanga 3 perukum innum bill aagala, 'Pending' status-la irukaanga)."
- PRONOUN RESOLUTION FOR "ANTHA VISIT" / "INTHA VISIT" / "THAT VISIT":
  * When user says "antha visit", "intha visit", "that visit", look at the IMMEDIATELY PRECEDING ASSISTANT MESSAGE in the conversation!
  * If the assistant just highlighted a specific visit (e.g. Visit 17089 for highest invoice), the follow-up query applies directly to Visit 17089!
  * Do NOT revert to an older visit (such as 17087) from several turns ago!
  * And NEVER treat words like "tha", "la", "ku", "details" as visit numbers!
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

When you have completed all actions and have the live result (or if you already know the answer and do not need any tools), output IMMEDIATELY:
Final Answer: <Your clear, factual response strictly in the USER'S EXACT LANGUAGE (English if asked in English, Tanglish if asked in Tanglish, Tamil if asked in Tamil)>

CRITICAL GUARDRAIL:
- NEVER output raw internal thinking, planning steps, or rules review (e.g. 'The user is asking in Tanglish...', 'According to the rules...', 'Let's formulate the final response...') to the user!
- Everything you output after `Final Answer:` is shown directly to the user in their language.
"""

        is_dev_mode = bool((context or {}).get("is_developer_mode", False))
        if is_dev_mode:
            system_prompt += """
DUAL RESPONSE SYSTEM MODE: 💻 DEVELOPER VIEW (FULL TECHNICAL DETAILS)
- Return full technical diagnostic data in your Final Answer:
  • Exact File Paths (e.g. `/L9/nagul/himes-ai/app/Http/Controllers/...`) and Line Numbers
  • Raw Error Stack Trace / Logs if investigating an issue
  • Code Changes / Git Diff
  • SQL Queries Executed (SELECT only) with table relationships
  • ChromaDB / Valkey Cache Lookup Details
- Format all code, SQL, and logs inside Markdown code blocks with language identifiers (```sql, ```php, ```bash) to enable copy-to-clipboard functionality.
- STRICT MULTI-LINGUAL & TANGLISH LANGUAGE MIRRORING MANDATE (CRITICAL & ABSOLUTE):
  • If user asks in Tanglish (Tamil words written in English/Latin letters, e.g. 'enga iruku', 'antha visit la enna service', 'receipt pottirukaangala', 'nethu date la', etc.):
    -> Answer STRICTLY in natural, friendly Tanglish (Latin alphabet)!
    -> NEVER use Pure Tamil Unicode script (தமிழ் எழுத்துகள்) when answering a Tanglish question!
    -> NEVER switch to pure English when answering a Tanglish question!
  • If user asks in English (e.g. 'What services were performed?', 'What is the payment mode?'):
    -> Answer STRICTLY in professional English!
  • If user asks in Pure Tamil (தமிழ் எழுத்துகளில்):
    -> Answer STRICTLY in Pure Tamil script (தமிழ் எழுத்துகளில்)!
  • If user asks in any other language (Arabic, Malayalam, Hindi, etc.):
    -> Answer in that EXACT SAME language!
- NEVER talk about or explain "User View" or "Developer View" to the user!
"""
        else:
            system_prompt += """
DUAL RESPONSE SYSTEM MODE: 👤 USER VIEW (DEFAULT - CLEAN & END-USER FRIENDLY)
- STRICT PROHIBITIONS (END-USER AUDIENCE):
  • NO raw database table names (NEVER mention tables like Patient_Appointment, Resource_Parent, Resource_Non_Availability, Patient_Visit_Basic_Details, Patient_Basic_Details, Appointment_Status_Type, etc.)!
  • NO raw column names or primary keys (do NOT mention Patient_Appointment_Serial_No, Resource_Parent_Serial_No, etc. - refer to them in plain business terms as 'Appointment Reference', 'Visit No', 'MRN Number')!
  • NO raw SQL queries or database connection metadata (NEVER output SELECT statements, SQL accordions, database IP addresses 192.168.x.x, or 'Tables Queried' lists in User View - those belong strictly in Developer Mode)!
  • NO raw URL route paths or slashes (do NOT write '/appointmentScheduler', '/viewQuickRegistration', '/patientRegistration', etc. - refer to screens by their clean UI name: 'Appointment Scheduler screen', 'Patient Registration screen', 'Quick Registration screen')!
  • NO PHP controller names or class names (NEVER mention QuickDemoRegController, QuickRegistrationController, RegistrationTabController, or any Controller.php - refer to them as 'Patient Registration Screen', 'Quick Registration Desk', 'Front Desk', etc.)!
  • NO backend request parameters or query strings (NEVER mention 'replicate=1', GET/POST parameters, API payloads, or database inserts)!
  • NO background cron job names or internal script names (do NOT mention AppointmentUpdateNoShow, ReportScheduleCron, etc.)!
  • NO file paths (do NOT mention /L9/nagul/himes-ai, app/Http/Controllers/..., routes/routes.php, etc.)
  • NO raw code snippets (no PHP, JS, or shell scripts)
  • NO technical error stack traces or framework internals
  • Speak ONLY in clean, intuitive, hospital business and UI screen navigation language (e.g. Doctor Roster, Doctor Leaves & Breaks, Slot Booking, Appointment Status Tracking, Front-Desk Visit Registration, Doctor Queue Token)!
  • When the user asks where an option or feature is located (e.g. 'replicate option enga irukum'):
    -> Explain the visual screen navigation clearly for the hospital staff (e.g., 'Patient Registration screen-la Visit Details tab / section-la Replicate Previous Visit option irukkum; atha click panna last visit insurance, services, diagnosis auto-populate aagidum'). Do NOT explain backend controllers, parameters, or route URLs!
- VISUAL LAYOUT & PRESENTATION:
  • Return responses structured with clean Markdown and status cards:
    - ✅ Green checkmark status cards for confirmed data / success (e.g. ✅ **Status:** Confirmed / Billed)
    - ⚠️ Friendly alerts for pending items or issues (e.g. ⚠️ **Status:** In Progress / Pending)
    - ℹ️ Plain-language action summaries (e.g. "We have identified the issue in the Billing section and our system has initiated an automatic resolution. Status: In Progress").
  • STRICT MULTI-LINGUAL & TANGLISH LANGUAGE MIRRORING MANDATE (CRITICAL & ABSOLUTE):
    - If user asks in Tanglish (Tamil words written in English/Latin letters):
      -> Answer STRICTLY in natural, friendly Tanglish (Latin alphabet)!
      -> NEVER use Pure Tamil Unicode script (தமிழ் எழுத்துகள்) for Tanglish questions!
      -> NEVER switch to pure English for Tanglish questions!
    - If user asks in English:
      -> Answer STRICTLY in professional English!
    - If user asks in Pure Tamil (தமிழ் எழுத்துகளில்):
      -> Answer STRICTLY in Pure Tamil script (தமிழ் எழுத்துகளில்)!
    - If user asks in any other language (Arabic, Malayalam, Hindi, etc.):
      -> Answer in that EXACT SAME language!
  • NEVER talk about or explain "User View" or "Developer View" to the user!
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

            # 4. Multi-Turn Session Conversation History (Full LangChain window)
            recent_hist = context.get("recent_history_context")
            if recent_hist:
                context_guidance += f"\n\n{recent_hist}\n"
            else:
                turns = context.get("previous_chat_turns", [])
                if turns:
                    context_guidance += "\n\n### FULL SESSION CHAT HISTORY (Chronological from Turn 1):\n"
                    for i, t in enumerate(turns, 1):
                        u_msg = t.get("user") or ""
                        a_msg = t.get("agent") or t.get("ai") or ""
                        context_guidance += f"Turn {i}:\n  User: {u_msg}\n  Assistant: {str(a_msg)[:1200]}\n"

        history = [
            f"User Request: {user_task}\n"
            f"Context: {context_guidance.strip() if context_guidance else json.dumps(context or {})}\n"
            f"Begin your investigation!"
        ]
        actions_taken = []
        max_iterations = 10
        last_sql_query = None
        last_sql_results = None

        active_mrn = str((context or {}).get("active_entities", {}).get("mrn") or "")
        session_id = str((context or {}).get("session_id") or "default_session")

        # Extract base64 image attachments if present (for Gemini Vision multimodal understanding)
        image_parts = []
        raw_attachments = (context or {}).get("attachments", [])
        if raw_attachments and isinstance(raw_attachments, list):
            import base64
            from google.genai import types
            for att in raw_attachments:
                try:
                    att_type = att.get("type", "")
                    data_str = att.get("data", "")
                    if "image" in att_type or att.get("name", "").lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                        if "," in data_str:
                            data_str = data_str.split(",", 1)[-1]
                        img_bytes = base64.b64decode(data_str)
                        mime_type = att_type if "image" in att_type else "image/png"
                        image_parts.append(types.Part.from_bytes(data=img_bytes, mime_type=mime_type))
                except Exception as ie:
                    print(f"[AutonomousAgent] Notice decoding image attachment: {ie}")

        # ---------------------------------------------------------------------
        # Valkey 5-Minute Ephemeral Caching Skill (SHA256 Hash Key)
        # ---------------------------------------------------------------------
        if not image_parts:
            try:
                from valkey_himes_manager import valkey_manager
                active_mode_str = "developer" if is_dev_mode else "user"
                cached_query = valkey_manager.get_ephemeral_query(user_task, active_mrn=active_mrn, session_id=session_id, mode=active_mode_str)
                if cached_query and isinstance(cached_query, dict):
                    cached_reply = cached_query.get("formatted_response") or ""
                    cached_sql = cached_query.get("executed_sql") or ""
                    if cached_reply:
                        return {
                            "status": "success",
                            "reply": cached_reply,
                            "actions_taken": [],
                            "steps": 0,
                            "sql_results": [],
                            "executed_sql": cached_sql,
                            "model_used": "Valkey Ephemeral Cache (5-min TTL, 0 Tokens)"
                        }
            except Exception as ve:
                print(f"[ValkeyCache] Notice: {ve}")

        def _build_sql_accordion(sql_str: str) -> str:
            clean_sql = sql_str.strip()
            t_matches = re.findall(r'(?:FROM|JOIN)\s+([A-Za-z0-9_]+)', clean_sql, flags=re.IGNORECASE)
            unique_t = list(dict.fromkeys(t_matches))[:5]
            t_display = ", ".join([f"`{t}`" for t in unique_t]) if unique_t else "`Patient_Visit_Basic_Details`"
            return (
                f"\n\n<details>\n"
                f"<summary>🔍 <b>View Generated SQL Query & Database Source</b></summary>\n\n"
                f"**Live MSSQL Query Executed:**\n"
                f"```sql\n{clean_sql}\n```\n\n"
                f"• **Database Source:** Live HIMES Database (`192.168.20.152`)\n"
                f"• **Tables Queried:** {t_display}\n"
                f"*(⚡ Real-Time Live MSSQL Execution | Verified Facts)*\n"
                f"</details>"
            )

        def attach_formatted_sql_card(text: str) -> str:
            # IN USER VIEW: STRICTLY NEVER ATTACH SQL ACCORDIONS, RAW QUERIES, OR DATABASE HOSTS!
            if not is_dev_mode:
                return text

            if not last_sql_query:
                return text

            if "View Generated SQL Query" in text or "View Executed SQL" in text:
                return text

            # Check if LLM already formatted a markdown table in its answer
            has_table = ("| ---" in text or "| :---" in text or "|:---" in text or "|---" in text)

            if has_table:
                # LLM already rendered the records cleanly; attach informative collapsible SQL accordion in Developer Mode
                return f"{text}{_build_sql_accordion(last_sql_query)}"

            # If the user did NOT explicitly ask for billing/services breakdown,
            # do NOT attach a clinical services / billed overview card!
            user_task_lower = user_task.lower()
            is_billing_or_services_query = any(w in user_task_lower for w in [
                "service", "cpt", "unbilled", "procedure", "lab order", "order", "சிகிச்சை", "பரிசோதனை", "நிலுவை", "billing status", "invoice"
            ])

            if is_billing_or_services_query and last_sql_results and isinstance(last_sql_results, list) and len(last_sql_results) > 0:
                try:
                    from utils.table_formatter import format_user_friendly_response
                    active_visit = (context or {}).get("active_entities", {}).get("visit_no")
                    formatted_card = format_user_friendly_response(
                        last_sql_results,
                        query_context={
                            "user_query": user_task,
                            "mrn": active_mrn,
                            "visit_no": active_visit,
                            "executed_sql": last_sql_query
                        },
                        mode="developer"
                    )
                    if formatted_card:
                        return f"{text}\n\n{formatted_card}"
                except Exception as fe:
                    print(f"[TableFormatter] notice: {fe}")
            else:
                # In Developer Mode: attach the collapsible SQL accordion with exact query and table source
                return f"{text}{_build_sql_accordion(last_sql_query)}"

            return text

        for step in range(max_iterations):
            prompt_input = "\n\n".join(history)
            current_images = image_parts if (step == 0 and image_parts) else None
            raw_llm = self.call_llm(prompt_input, system_prompt, image_parts=current_images)
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
                final_text = clean_agent_thought(llm_response)
                full_reply = attach_formatted_sql_card(final_text)

                # Cache in Valkey for 300s (5-minute TTL)
                try:
                    from valkey_himes_manager import valkey_manager
                    active_mode_str = "developer" if is_dev_mode else "user"
                    valkey_manager.cache_ephemeral_query(
                        user_task,
                        active_mrn=active_mrn,
                        session_id=session_id,
                        formatted_response=full_reply,
                        executed_sql=last_sql_query or "",
                        ttl=300,
                        mode=active_mode_str
                    )
                except Exception as ce:
                    print(f"[ValkeyCache] Save notice: {ce}")

                return {
                    "status": "success",
                    "reply": full_reply,
                    "actions_taken": actions_taken,
                    "steps": step + 1,
                    "sql_results": last_sql_results,
                    "executed_sql": last_sql_query
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

            # Dynamic SQL Interception: If model formulated SQL in thought without Action wrapper
            if not action:
                sql_block = re.search(r"```sql\s*(SELECT\s+.*?)```", llm_response, re.DOTALL | re.IGNORECASE)
                if not sql_block:
                    sql_block = re.search(r"\b(SELECT\s+(?:TOP\s+\d+\s+)?[^\n;]+?\bFROM\s+[a-zA-Z0-9_]+[^\n;]*)", llm_response, re.DOTALL | re.IGNORECASE)
                if sql_block:
                    candidate_sql = sql_block.group(1).strip()
                    if candidate_sql.upper().startswith("SELECT") and "FROM" in candidate_sql.upper():
                        if "WITH(NOLOCK)" not in candidate_sql.upper():
                            candidate_sql = re.sub(r'\bFROM\s+(\w+)\b(?!\s+WITH)', r'FROM \1 WITH(NOLOCK)', candidate_sql, flags=re.IGNORECASE)
                        if "TOP " not in candidate_sql.upper():
                            candidate_sql = re.sub(r'^SELECT\s+', 'SELECT TOP 50 ', candidate_sql, flags=re.IGNORECASE)
                        action = "execute_select_sql"
                        raw_input = json.dumps({"sql_query": candidate_sql})

            if not action:
                if llm_response.strip():
                    clean_reply = clean_agent_thought(llm_response)
                    return {
                        "status": "success",
                        "reply": attach_formatted_sql_card(clean_reply),
                        "actions_taken": actions_taken,
                        "steps": step + 1,
                        "sql_results": last_sql_results,
                        "executed_sql": last_sql_query
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
                    sql_str = str(q or "").strip()
                    last_sql_query = sql_str
                    obs = self.execute_select_sql(sql_str)
                    try:
                        if obs and obs.strip().startswith("["):
                            parsed_rows = json.loads(obs)
                            if isinstance(parsed_rows, list):
                                last_sql_results = parsed_rows
                            else:
                                last_sql_results = []
                        else:
                            last_sql_results = []
                    except Exception:
                        last_sql_results = []
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
            "reply": attach_formatted_sql_card(final_summary),
            "actions_taken": actions_taken,
            "steps": max_iterations,
            "sql_results": last_sql_results,
            "executed_sql": last_sql_query
        }

autonomous_agent = AutonomousAgent()
