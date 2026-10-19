import sys
import os
import re
import json
import datetime

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

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from ssh_tool import test_ssh_connection, execute_ssh_command
from guardrails import (
    SecurityException,
    validate_sql_query,
    validate_command_directory_safety,
    is_path_inside_allowed_dir
)
from ssh_sandbox import sandboxed_ssh
from git_automation import SafeGitWorkflow
from autonomous_agent import autonomous_agent
from semantic_cache import check_semantic_cache, save_to_semantic_cache, enforce_safety_rules
from memory_manager import search_knowledge_base
from valkey_himes_manager import (
    valkey_manager,
    get_himes_context,
    get_himes_flow,
    save_session_state,
    get_session_state
)

# Load environment variables from .env
load_dotenv(override=True)

# ====================================================================
# STRICT GUARDRAILS & SAFETY SYSTEM PROMPT
# ====================================================================
SAFETY_SYSTEM_PROMPT = """====================================================================
STRICT GUARDRAILS & SAFETY SKILL FOR NAGUL'S AUTONOMOUS AGENT
====================================================================

You are an AI Coding Agent assigned strictly to work on Nagul's environment.
You MUST strictly adhere to the following safety rules at all times. Failure to comply with these rules is forbidden.

1. DATABASE SAFETY RULES:
   - ONLY `SELECT` queries are allowed to be executed on the database.
   - Strictly PROHIBIT executing any `UPDATE`, `DELETE`, `DROP`, `TRUNCATE`, `ALTER`, or `INSERT` queries.
   - If a task requires updating or deleting data, notify the user and ask for manual intervention.

2. SSH & DIRECTORY ACCESS RESTRICTIONS:
   - You are ONLY allowed to operate inside Nagul's directory (/L9/nagul/ or user's designated project path).
   - STRICTLY FORBIDDEN to access, edit, view, or modify any files outside Nagul's folder.
   - DO NOT affect or touch other developers' folders or global system files on the server under any circumstances.

3. GIT BRANCHING & MERGING RULES:
   - NEVER merge any code into the `main`, `master`, or `development` branches directly.
   - ALWAYS create a new sub-branch from the development branch (e.g., `feature/zoho-task-id` or `fix/zoho-bug-id`).
   - Work strictly inside this sub-branch.
   - You are allowed to: Edit Code -> Commit Changes -> Push Branch to Remote -> Create Pull Request (PR).
   - STOP after creating the Pull Request. Merging MUST be done manually by human review.

4. AUTONOMOUS EXECUTION SAFETY:
   - Always run syntax checks (`php -l`) and automated tests (`php artisan test`) inside Nagul's directory before committing.
   - If a command tries to touch paths outside Nagul's directory, abort execution immediately.
===================================================================="""

app = FastAPI(
    title="Autonomous AI Agent Service with Safety Guardrails",
    description="Production-grade AI Agent API for Laravel with Directory Lock, Read-Only SQL Guardrails, and Git PR Automation",
    version="2.0.0"
)

# Enable CORS for web integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AgentRequest(BaseModel):
    task: str
    context: dict = {}

class AgentResponse(BaseModel):
    status: str
    message: str
    result: dict = {}

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default_session"
    preferred_model: str = "auto"  # 'claude-3-5-sonnet', 'gpt-4o', 'gemini'
    context: dict = {}

class ChatResponse(BaseModel):
    status: str
    reply: str
    model_used: str
    action_executed: dict = {}
    guardrails_enforced: list[str] = [
        "Database Guardrail: SELECT queries only (UPDATE/DELETE/DROP blocked)",
        "Directory Lock: Confined strictly within Nagul's folder (/L9/nagul/)",
        "Git Safety: Sub-branch + PR only (Auto-merge forbidden)"
    ]

class SSHCommandRequest(BaseModel):
    command: str

def generate_model_response(prompt: str, system_prompt: str = SAFETY_SYSTEM_PROMPT, preferred_model: str = "auto") -> tuple[str, str]:
    """
    Invokes the requested LLM (Claude 3.5 Sonnet, GPT-4o, or Gemini 3.5 Flash)
    always enforcing Nagul's STRICT GUARDRAILS & SAFETY SYSTEM PROMPT.
    Returns (response_text, model_name).
    """
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

    # 1. Claude 3.5 Sonnet
    if (preferred_model.lower() in ["claude", "claude-3-5-sonnet", "sonnet"] or preferred_model == "auto") and anthropic_key and not anthropic_key.startswith("your_"):
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=anthropic_key)
            msg = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2048,
                system=system_prompt,
                messages=[{"role": "user", "content": prompt}]
            )
            return msg.content[0].text, "Claude 3.5 Sonnet"
        except Exception as e:
            if preferred_model != "auto":
                raise e

    # 2. OpenAI GPT-4o
    if (preferred_model.lower() in ["gpt-4o", "openai"] or preferred_model == "auto") and openai_key and not openai_key.startswith("your_"):
        try:
            from openai import OpenAI
            client = OpenAI(api_key=openai_key)
            completion = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o"),
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            )
            return completion.choices[0].message.content, "OpenAI GPT-4o"
        except Exception as e:
            if preferred_model != "auto":
                raise e

    # 3. Google Gemini (Fast fallback)
    if gemini_key and not gemini_key.startswith("your_"):
        from langchain_google_genai import ChatGoogleGenerativeAI
        models_to_try = [
            "gemini-3.1-flash-lite",
            "gemini-3.7-flash",
            "gemini-flash-lite-latest",
            "gemini-3-flash-preview",
            "gemma-4-31b-it",
            "gemini-3.8-flash",
            "gemini-3.5-flash"
        ]
        last_err = None
        for m in models_to_try:
            try:
                llm = ChatGoogleGenerativeAI(
                    model=m,
                    google_api_key=gemini_key,
                    max_retries=1
                )
                full_prompt = f"{system_prompt}\n\nTask / Question:\n{prompt}"
                res = llm.invoke(full_prompt)
                if isinstance(res.content, list):
                    content = "".join([part.get("text", "") if isinstance(part, dict) else str(part) for part in res.content])
                else:
                    content = str(res.content)
                return content, f"Google Gemini ({m})"
            except Exception as e:
                last_err = e
                continue
        if last_err:
            raise last_err

    raise ValueError("No AI API key found! Please configure GEMINI_API_KEY, OPENAI_API_KEY, or ANTHROPIC_API_KEY in .env.")

def generate_ai_response(prompt: str) -> str:
    """Wrapper for backward compatibility."""
    res, _ = generate_model_response(prompt)
    return res

@app.get("/")
def health_check():
    """Health check endpoint to verify Python agent server and integrations."""
    gemini_key = os.getenv("GEMINI_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    has_key = bool((gemini_key and not gemini_key.startswith("your_")) or (openai_key and not openai_key.startswith("your_")))
    provider = "Google Gemini" if gemini_key else ("OpenAI" if openai_key else "None")
    ssh_configured = bool(os.getenv("SSH_HOST") and os.getenv("SSH_USER"))

    return {
        "status": "online",
        "service": "Python Autonomous AI Agent",
        "ai_brain_configured": has_key,
        "active_provider": provider,
        "ssh_configured": ssh_configured
    }

@app.get("/ssh/test")
def test_ssh():
    """
    Test the SSH connection to the remote server configured in .env.
    Uses the Ed25519/RSA key from ~/.ssh or SSH_KEY_PATH.
    """
    return test_ssh_connection()

@app.post("/ssh/exec")
def exec_ssh_command(payload: SSHCommandRequest):
    """
    Directly execute a shell command on the remote server via SSH.
    Example: {"command": "df -h"} or {"command": "uptime"}
    """
    output = execute_ssh_command.invoke({"command": payload.command})
    return {
        "command": payload.command,
        "output": output
    }

import datetime

def plan_autonomous_action(task: str, context: dict = None) -> tuple[str, str]:
    """
    Determines the exact command to run on the server by mapping the user's intent to the
    real Laravel controllers (GlobalViewBillingController, EMRWaitingListController, etc.),
    ensuring live database queries strictly match the application's code logic.
    """
    task_lower = task.lower()

    # Determine date filter (Yesterday vs Today)
    if any(w in task_lower for w in ["yesterday", "netru", "netruku", "நேற்று"]):
        date_filter = "CAST(DATEADD(day, -1, GETDATE()) AS DATE)"
        date_label = "Yesterday"
    elif any(w in task_lower for w in ["today", "inraikku", "iniku", "இன்று"]):
        date_filter = "CAST(GETDATE() AS DATE)"
        date_label = "Today"
    else:
        date_filter = "CAST(DATEADD(day, -1, GETDATE()) AS DATE)"
        date_label = "Yesterday"

    # 1. BILLING MODULE: Patient Billing Status (viewGlobalBilling / GlobalViewBillingController)
    # Triggered when user asks about bill, billing, invoice, pending invoices, billed count, or global view billing
    if any(w in task_lower for w in ["bill", "billing", "invoice", "invoiced", "viewglobalbilling", "invoices", "pending bill"]):
        cmd = (
            f'docker exec nagul php /var/www/html/himes-ai/artisan tinker --execute="'
            f'echo json_encode(['
            f'  \\"module\\" => \\"Patient Billing Status (viewGlobalBilling)\\",'
            f'  \\"date_period\\" => \\"{date_label}\\",'
            f'  \\"status_counts\\" => DB::select(\\"'
            f'    SELECT '
            f'      CASE '
            f'        WHEN pbh.Patient_Bill_Header_Serial_No IS NOT NULL AND pbh.Bill_Cancellation_Flag = \'N\' THEN \'Billed\' '
            f'        ELSE \'Pending\' '
            f'      END as billing_status, '
            f'      COUNT(DISTINCT pvbd.Patient_Visit_Basic_Details_Serial_No) as cnt '
            f'    FROM Patient_Visit_Basic_Details pvbd '
            f'    JOIN Patient_Visit_Services pvs ON pvs.Patient_Visit_Basic_Details_Serial_No = pvbd.Patient_Visit_Basic_Details_Serial_No '
            f'      AND pvs.Patient_Visit_Service_Cancellation_Flag = \'N\' AND pvs.Active_Status = \'A\' '
            f'    LEFT JOIN Patient_Bill_Detail_Services_Packages_Resources_Drugs pbdsprd ON pbdsprd.Patient_Visit_Services_Serial_No = pvs.Patient_Visit_Services_Serial_No '
            f'      AND pbdsprd.Active_Status = \'A\' AND pbdsprd.Service_Resource_Drug_Cancellation_Flag = \'N\' '
            f'    LEFT JOIN Patient_Bill_Header pbh ON pbh.Patient_Bill_Header_Serial_No = pbdsprd.Bill_Header_Serial_No '
            f'      AND pbh.Bill_Cancellation_Flag = \'N\' '
            f'    WHERE CAST(pvbd.Patient_Visit_Registered_Date_Time AS DATE) = {date_filter} '
            f'      AND pvbd.Active_Status = \'A\' AND pvbd.Visit_Cancellation_Flag = \'N\' '
            f'    GROUP BY '
            f'      CASE '
            f'        WHEN pbh.Patient_Bill_Header_Serial_No IS NOT NULL AND pbh.Bill_Cancellation_Flag = \'N\' THEN \'Billed\' '
            f'        ELSE \'Pending\' '
            f'      END'
            f'  \\"),'
            f'  \\"total_unique_patients\\" => DB::table(\\"Patient_Visit_Basic_Details\\")->whereRaw(\\"CAST(Patient_Visit_Registered_Date_Time AS DATE) = {date_filter}\\")->where(\\"Active_Status\\", \\"A\\")->where(\\"Visit_Cancellation_Flag\\", \\"N\\")->count()'
            f']);"'
        )
        return cmd, "billing_status_query"

    # 2. EMR WORKSTATION / CASELOAD MODULE (viewEMRWaitingList / EMRWaitingListController)
    if any(w in task_lower for w in ["emr", "workstation", "caseload", "waitinglist"]):
        cmd = (
            f'docker exec nagul php /var/www/html/himes-ai/artisan tinker --execute="'
            f'echo json_encode(['
            f'  \\"module\\" => \\"EMR Workstation (viewEMRWaitingList)\\",'
            f'  \\"date_period\\" => \\"{date_label}\\",'
            f'  \\"total_patients\\" => DB::table(\\"Patient_Visit_Basic_Details\\")->whereRaw(\\"CAST(Patient_Visit_Registered_Date_Time AS DATE) = {date_filter}\\")->where(\\"Active_Status\\", \\"A\\")->where(\\"Visit_Cancellation_Flag\\", \\"N\\")->where(\\"Visit_Is_Non_Consultation\\", \\"N\\")->count(),'
            f'  \\"status_breakdown\\" => DB::select(\\"SELECT CASE WHEN Is_EMR_Completed = \'C\' THEN \'EMR Complete\' WHEN Is_EMR_In_Progress = \'Y\' THEN \'EMR In Progress\' ELSE \'Registered / Waiting\' END as status, COUNT(*) as cnt FROM Patient_Visit_Basic_Details WHERE CAST(Patient_Visit_Registered_Date_Time AS DATE) = {date_filter} AND Active_Status = \'A\' AND Visit_Cancellation_Flag = \'N\' AND Visit_Is_Non_Consultation = \'N\' GROUP BY CASE WHEN Is_EMR_Completed = \'C\' THEN \'EMR Complete\' WHEN Is_EMR_In_Progress = \'Y\' THEN \'EMR In Progress\' ELSE \'Registered / Waiting\' END\\"),'
            f'  \\"branch_breakdown\\" => DB::select(\\"SELECT Branch_Code, COUNT(*) as cnt FROM Patient_Visit_Basic_Details WHERE CAST(Patient_Visit_Registered_Date_Time AS DATE) = {date_filter} AND Active_Status = \'A\' AND Visit_Cancellation_Flag = \'N\' AND Visit_Is_Non_Consultation = \'N\' GROUP BY Branch_Code\\")'
            f']);"'
        )
        return cmd, "emr_workstation_query"

    # 3. GENERAL PATIENT REGISTRATIONS / VISITS
    if any(w in task_lower for w in ["patient", "patients", "visit", "visits", "registration"]):
        cmd = (
            f'docker exec nagul php /var/www/html/himes-ai/artisan tinker --execute="'
            f'echo json_encode(['
            f'  \\"module\\" => \\"Patient Registrations\\",'
            f'  \\"date_period\\" => \\"{date_label}\\",'
            f'  \\"total_registrations\\" => DB::table(\\"Patient_Visit_Basic_Details\\")->whereRaw(\\"CAST(Patient_Visit_Registered_Date_Time AS DATE) = {date_filter}\\")->where(\\"Active_Status\\", \\"A\\")->where(\\"Visit_Cancellation_Flag\\", \\"N\\")->count(),'
            f'  \\"by_branch\\" => DB::select(\\"SELECT Branch_Code, COUNT(*) as cnt FROM Patient_Visit_Basic_Details WHERE CAST(Patient_Visit_Registered_Date_Time AS DATE) = {date_filter} AND Active_Status = \'A\' AND Visit_Cancellation_Flag = \'N\' GROUP BY Branch_Code\\")'
            f']);"'
        )
        return cmd, "patient_visit_query"

    # 4. LARAVEL ERROR LOGS / CRASH / BUGS
    if any(w in task_lower for w in ["log", "logs", "error", "exception", "bug", "crash", "trace"]):
        cmd = "tail -n 60 /L9/nagul/himes-ai/storage/logs/laravel.log 2>&1"
        return cmd, "log_inspection"

    # 5. ROUTES / SCREENS INSPECTION
    if any(w in task_lower for w in ["route", "routes", "url"]):
        cmd = "cd /L9/nagul/himes-ai && php artisan route:list | head -n 35"
        return cmd, "route_inspection"

    # 6. SYSTEM METRICS / DOCKER
    if any(w in task_lower for w in ["disk", "storage"]):
        return "df -h -x overlay -x tmpfs", "system_stat"
    if any(w in task_lower for w in ["memory", "ram"]):
        return "free -h", "system_stat"
    if any(w in task_lower for w in ["cpu", "process"]):
        return "ps aux --sort=-%cpu | head -n 10", "system_stat"
    if "docker" in task_lower:
        return "docker ps --filter name=nagul", "docker_stat"
    if "uptime" in task_lower:
        return "uptime", "system_stat"

    # 7. DYNAMIC CODE INVESTIGATOR & QUERY PLANNER
    server_indicators = ["sql", "query", "db", "database", "table", "select", "git", "branch", "code", "controller", "model"]
    if any(w in task_lower for w in server_indicators):
        try:
            planner_prompt = f"""You are the DevOps/Database agent planner for HIMES Laravel (/L9/nagul/himes-ai, Docker: nagul, DB: MSSQL himes_dev_new).
User task: {task}
Determine the exact shell or tinker command to run to retrieve the required data.
Return ONLY the command string, with no markdown formatting. If no command needed, output NONE."""
            ai_cmd = generate_ai_response(planner_prompt).strip()
            if ai_cmd and ai_cmd != "NONE" and not ai_cmd.startswith("Error"):
                return ai_cmd, "ai_planned_command"
        except Exception:
            pass

    return None, "direct_answer"

@app.post("/agent/run", response_model=AgentResponse)
def run_agent_task(payload: AgentRequest):
    """
    Endpoint for Laravel Chat Widget to trigger fully autonomous agent execution.
    Integrates ChromaDB Semantic Cache:
    1. Check ChromaDB cache first (distance < 0.25).
    2. If hit: return cached answer immediately!
    3. If miss: run autonomous_agent.run(...), save to cache, and return.
    """
    try:
        task_query = payload.task or ""
        enforce_safety_rules(task_query)

        # 1. Check ChromaDB Semantic Cache first for instant response
        cached_result = check_semantic_cache(task_query, threshold=0.25)
        if cached_result:
            return AgentResponse(
                status="success",
                message=cached_result["answer"],
                result={
                    "task": task_query,
                    "actions_taken": ["ChromaDB Semantic Cache Hit (Instant)"],
                    "steps": 0,
                    "ai_response": cached_result["answer"]
                }
            )

        # 2. Cache Miss -> Run autonomous agent dynamic execution
        agent_res = autonomous_agent.run(payload.task, payload.context)
        reply = agent_res.get("reply", "Task completed.")

        # 3. Save into ChromaDB cache for future instant queries
        save_to_semantic_cache(task_query, reply)

        return AgentResponse(
            status=agent_res.get("status", "success"),
            message=reply,
            result={
                "task": payload.task,
                "actions_taken": agent_res.get("actions_taken", []),
                "steps": agent_res.get("steps", 1),
                "ai_response": reply
            }
        )
    except SecurityException as se:
        return AgentResponse(
            status="blocked_by_guardrails",
            message=f"Guardrail Protection Triggered: {str(se)}",
            result={"error_details": str(se)}
        )
    except Exception as e:
        return AgentResponse(
            status="error",
            message=f"Error executing AI Agent: {str(e)}",
            result={"error_details": str(e)}
        )

# Persistent session tracking for multi-turn conversations
SESSION_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "session_memory.json")
SESSION_MEMORY: dict[str, dict] = {}

def load_session_memory():
    global SESSION_MEMORY
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    SESSION_MEMORY = json.loads(content)
        except Exception as e:
            print(f"[SessionMemory] Error loading: {e}")
            SESSION_MEMORY = {}

def save_session_memory():
    try:
        data = json.dumps(SESSION_MEMORY, ensure_ascii=False, indent=2)
        with open(SESSION_FILE, "w", encoding="utf-8") as f:
            f.write(data)
    except Exception as e:
        print(f"[SessionMemory] Error saving: {e}")

load_session_memory()

def get_session_context(session_id: str) -> dict:
    load_session_memory()
    if session_id not in SESSION_MEMORY:
        SESSION_MEMORY[session_id] = {
            "turns": [],
            "active_entities": {"visit_no": None, "mrn": None, "bill_no": None}
        }
    return SESSION_MEMORY[session_id]

def extract_entities_from_text(text: str) -> dict:
    entities = {}
    v_m = re.search(r'\b(?:visit|visit\s*no|visit\s*number)[:\s#]*([0-9]{4,8})\b', text, re.IGNORECASE)
    if v_m:
        entities["visit_no"] = v_m.group(1)
        
    m_m = re.search(r'\b(?:mrn|patient\s*id)[:\s#]*([A-Za-z0-9_-]{4,15})\b', text, re.IGNORECASE)
    if not m_m:
        m_m = re.search(r'\b(PHAR[0-9]+)\b', text, re.IGNORECASE)
    if m_m:
        entities["mrn"] = m_m.group(1)
        
    b_m = re.search(r'\b(?:bill|bill\s*no|invoice)[:\s#]*([0-9]{4,8})\b', text, re.IGNORECASE)
    if b_m:
        entities["bill_no"] = b_m.group(1)
    return entities

def update_session_memory(session_id: str, user_msg: str, agent_reply: str):
    sess = get_session_context(session_id)
    
    # Extract entities from user message only (prevents agent hallucinations from sticking)
    ents = extract_entities_from_text(user_msg)
    for k, v in ents.items():
        if v:
            sess["active_entities"][k] = v

    sess["turns"].append({"user": user_msg, "agent": agent_reply})
    if len(sess["turns"]) > 6:
        sess["turns"] = sess["turns"][-6:]

    save_session_memory()


# ====================================================================
# PROMPT 4: CHATBOX BACKEND CONNECTION (/api/chat) WITH CHROMADB MEMORY
# ====================================================================
@app.post("/api/chat", response_model=ChatResponse)
def chat_with_agent(payload: ChatRequest):
    """
    Endpoint for Application Chatbox UI with ChromaDB Memory Integration & Multi-turn Session Awareness:
    1. Check ChromaDB cache first for instant response (distance <= 0.30, aspect matched).
    2. Inherit active conversation entities (visit_no, mrn, bill_no) from session memory for follow-ups.
    3. Run Autonomous Agent with live database and codebase tools.
    4. Save valid responses into ChromaDB cache and update session memory.
    """
    try:
        # Enforce strict safety rules: SELECT queries only, Nagul's directory lock
        enforce_safety_rules(payload.message)

        # Retrieve and update session context
        sess = get_session_context(payload.session_id)
        # Pre-scan user message for any entity updates
        user_ents = extract_entities_from_text(payload.message)
        for k, v in user_ents.items():
            if v:
                sess["active_entities"][k] = v
        v_m = user_ents.get("visit_no")
        m_m = user_ents.get("mrn")

        # 1. Valkey Fast-Path: Menu Navigation Lookup
        msg_lower = payload.message.lower()
        if any(p in msg_lower for p in ["price list management", "pricelist", "price list"]) and any(w in msg_lower for w in ["menu", "enga", "where", "screen", "location", "path", "open", "iruku"]):
            reply = (
                "**HIMES Price List Management Menu Details:**\n\n"
                "HIMES Application-la Price List Management menu intha path-la irukku:\n\n"
                "1. **Services & Insurance Tariff Price List:**\n"
                "   • **Menu Name:** `PRICE LIST MANAGEMENT`\n"
                "   • **Main Module:** `APPLICATION` (Billing / Tariff Setup)\n"
                "   • **Route / URL:** `/priceListManagement`\n"
                "   • **Controller:** `InsurancePriceListManagementController@viewInsurancePriceListManagement`\n"
                "   • **Function ID:** `PRICELIST`\n\n"
                "2. **Pharmacy & Inventory Items Price List:**\n"
                "   • **Menu Name:** `INVENTORY PRICE LIST MANAGEMENT`\n"
                "   • **Main Module:** `INVENTORY`\n"
                "   • **Route / URL:** `/ViewInventoryPriceListManagement`\n"
                "   • **Function ID:** `INVPRICLST`\n\n"
                "3. **Bed & Doctor Resources Price Rule:**\n"
                "   • **Menu Name:** `PRICE RULE FOR RESOURCES`\n"
                "   • **Main Module:** `APPLICATION`\n"
                "   • **Route / URL:** `/PriceRuleForResources`\n"
                "   • **Function ID:** `PRRULFRRES`\n\n"
                "4. **Bulk Price List Upload & Management:**\n"
                "   • **Route / URL:** `/BulkPriceListManagement`\n\n"
                "*(⚡ Instant response powered by Valkey Menu Index)*"
            )
            update_session_memory(payload.session_id, payload.message, reply)
            valkey_manager.update_session_entities(payload.session_id, sess["active_entities"])
            return ChatResponse(
                status="success",
                reply=reply,
                model_used="Valkey In-Memory Cache (Sub-millisecond)",
                action_executed={
                    "cache_hit": True,
                    "source": "valkey_menu_index",
                    "namespace": "himes:menu:price_list"
                }
            )

        # 1a. Valkey Fast-Path: Active Application Screen Lookup
        current_path = (payload.context or {}).get("current_path", "")
        clean_route = current_path.strip("/").split("/")[-1].lower() if current_path else ""
        refers_to_current_screen = any(w in msg_lower for w in ["intha screen", "this screen", "current screen", "intha page", "this page", "screen ah", "screen-a", "screen pathi", "module ah paaru", "screen ah paaru"]) or (clean_route and clean_route in msg_lower)
        
        if clean_route and refers_to_current_screen and not bool(v_m or m_m):
            screen_data = valkey_manager._get(f"himes:screen:{clean_route}")
            if screen_data:
                tables_str = ", ".join(screen_data.get("tables", [])[:6])
                reply = (
                    f"**HIMES Active Screen Overview: {screen_data.get('title')}**\n\n"
                    f"• **Route Path:** `/{clean_route}`\n"
                    f"• **Primary Controller:** `{screen_data.get('controller')}`\n"
                    f"• **Domain Module:** `{screen_data.get('module').upper()}`\n\n"
                    f"**Screen Purpose & Functionality:**\n"
                    f"{screen_data.get('description')}\n\n"
                    f"**Associated SQL Tables:**\n"
                    f"`{tables_str}`\n\n"
                    f"*(⚡ Instant response powered by Valkey Screen Route Index)*"
                )
                update_session_memory(payload.session_id, payload.message, reply)
                return ChatResponse(
                    status="success",
                    reply=reply,
                    model_used="Valkey In-Memory Cache (Sub-millisecond)",
                    action_executed={
                        "cache_hit": True,
                        "source": "valkey_screen_index",
                        "namespace": f"himes:screen:{clean_route}"
                    }
                )

        # 1b. Valkey Fast-Path: Instant Module Lifecycle & Flow lookup (All 12 HIMES Domains)
        is_module_query = any(phrase in msg_lower for phrase in ["flow", "lifecycle", "process", "explain", "tables", "how does", "steps for", "pathina", "workflow", "eclaim", "claim", "pa_", "module", "paaru"])
        if is_module_query:
            module_map = {
                "lis": ["lis", "lab", "laboratory", "specimen", "pathology", "sample accession"],
                "ris": ["ris", "radiology", "pacs", "dicom", "xray", "mri", "ct scan", "imaging"],
                "emr_panels": ["emr panels", "emr panel", "emr", "clinical panel", "doctor panel", "nursing", "specialty panel", "vitals", "chief complaint"],
                "masters_400": ["masters", "master", "400 master", "masters page", "tariff setup", "service master", "bulk master"],
                "billing": ["billing flow", "billing", "invoice generation", "co-pay", "copay", "deductible", "cashier"],
                "pharmacy": ["pharmacy module", "pharmacy", "drug dispensing", "op pharmacy", "ip pharmacy", "formulary", "medicine"],
                "invoice_posting": ["invoice posting", "posting to ledger", "tally export", "quickbook export", "financial ledger", "ledger"],
                "credit_notes": ["credit note", "credit notes", "refund", "bill cancellation", "credit voucher"],
                "claim_management": ["claim", "claims", "eclaim", "remittance", "era 835", "dhpo", "shafafiya", "waseel", "malaffi", "batch submission"],
                "prior_visit": ["prior visit", "prior_visit", "pa_patient", "pa_insurance", "pre-authorization", "prior auth"],
                "cron_jobs": ["cron", "cron job", "scheduled job", "background job", "kernel schedule", "reportschedulecron"],
                "registration": ["registration flow", "registration", "emirates id", "appointment scheduler", "queue"]
            }

            for mod_k, patterns in module_map.items():
                if any(p in msg_lower for p in patterns):
                    mod_data = valkey_manager._get(f"himes:module:{mod_k}")
                    if mod_data:
                        tables_str = ", ".join(mod_data.get("primary_tables", [])[:6])
                        workflows = "\n".join([f"• {wf}" for wf in mod_data.get("key_workflows", [])])
                        reply = (
                            f"**HIMES {mod_data.get('title')} Lifecycle Details:**\n\n"
                            f"{mod_data.get('description')}\n\n"
                            f"**Key SQL Tables:**\n`{tables_str}`\n\n"
                            f"**Core Workflows:**\n{workflows}\n\n"
                            f"*(⚡ Instant response powered by Valkey In-Memory Index)*"
                        )
                        update_session_memory(payload.session_id, payload.message, reply)
                        valkey_manager.update_session_entities(payload.session_id, sess["active_entities"])
                        return ChatResponse(
                            status="success",
                            reply=reply,
                            model_used="Valkey In-Memory Cache (Sub-millisecond)",
                            action_executed={
                                "cache_hit": True,
                                "source": "valkey_module_index",
                                "namespace": f"himes:module:{mod_k}"
                            }
                        )

        # 2. Check ChromaDB Semantic Cache (distance <= 0.30)
        # Note: Follow-up questions without explicit entities bypass cache to resolve against active session context
        has_entities_in_query = bool(v_m or m_m)
        is_followup = not has_entities_in_query and bool(sess["active_entities"].get("visit_no") or sess["active_entities"].get("mrn"))
        
        if not is_followup:
            cached_result = check_semantic_cache(payload.message, threshold=0.30)
            if cached_result:
                update_session_memory(payload.session_id, payload.message, cached_result["answer"])
                valkey_manager.update_session_entities(payload.session_id, sess["active_entities"])
                return ChatResponse(
                    status="success",
                    reply=cached_result["answer"],
                    model_used="ChromaDB Semantic Cache (Instant Hit)",
                    action_executed={
                        "cache_hit": True,
                        "matched_query": cached_result.get("matched_query"),
                        "distance": cached_result.get("distance")
                    }
                )

        # Build enriched context with session memory and Valkey Hybrid Search
        full_context = dict(payload.context or {})

        # Determine if query is a general module or screen inquiry rather than a visit follow-up
        is_module_or_screen_query = any(w in msg_lower for w in ["module", "screen", "menu", "workflow", "lifecycle", "page", "viewglobal", "view"]) and not bool(v_m)
        active_ents_to_pass = dict(sess["active_entities"])
        if is_module_or_screen_query:
            active_ents_to_pass["visit_no"] = None  # Prevent old visit from hijacking module questions

        full_context["active_entities"] = active_ents_to_pass
        full_context["previous_chat_turns"] = list(sess["turns"][-3:])

        # Valkey Smart Hybrid Context enrichment
        valkey_ctx = get_himes_context(payload.message, limit=2)
        if valkey_ctx.get("context"):
            full_context["valkey_knowledge"] = valkey_ctx["context"]

        # Sync active session state into Valkey
        valkey_manager.update_session_entities(payload.session_id, sess["active_entities"])

        # 3. Run Autonomous Agent with live database and codebase tools
        agent_res = autonomous_agent.run(payload.message, full_context)
        reply_text = agent_res.get("reply", "No response generated.")
        actions_taken = agent_res.get("actions_taken", [])

        # Update session memory
        update_session_memory(payload.session_id, payload.message, reply_text)
        valkey_manager.update_session_entities(payload.session_id, sess["active_entities"])

        # 3. Save into ChromaDB Semantic Cache for future instant lookups (skip follow-ups lacking standalone context)
        if not is_followup:
            save_to_semantic_cache(payload.message, reply_text)

        return ChatResponse(
            status=agent_res.get("status", "success"),
            reply=reply_text,
            model_used="Autonomous Agent (Live MSSQL Engine)",
            action_executed={
                "cache_hit": False,
                "actions_taken": actions_taken,
                "steps": agent_res.get("steps", 1)
            }
        )

    except SecurityException as se:
        return ChatResponse(
            status="blocked_by_guardrails",
            reply=f"⚠️ Guardrail Protection Triggered: {str(se)}",
            model_used="Security Guardrail",
            action_executed={"error": str(se)}
        )
    except Exception as e:
        return ChatResponse(
            status="error",
            reply=f"⚠️ Error processing query: {str(e)}",
            model_used="Error Handler",
            action_executed={"error": str(e)}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
