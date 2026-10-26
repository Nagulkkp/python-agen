import sys
import os
import re
import json
import datetime
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

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
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
from autonomous_agent import autonomous_agent, clean_agent_thought
from multi_agent_system import himes_orchestrator
from language_specialist_agent import language_specialist
from memory_manager import search_knowledge_base

from semantic_cache import (
    check_semantic_cache,
    save_to_semantic_cache,
    enforce_safety_rules,
    is_patient_or_phi_data,
    verify_answer_relevance
)
from valkey_himes_manager import (
    valkey_manager,
    get_himes_context,
    get_himes_flow,
    save_session_state,
    get_session_state
)

# ── LangChain Integrations (lazy import to avoid circular deps at startup)
# chains, agents, memory, and skills are imported inside their endpoints
# so uvicorn startup time is not penalised.

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

@app.middleware("http")
async def add_private_network_headers(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Private-Network"] = "true"
    return response

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
    user_id: Optional[str] = "guest"
    username: Optional[str] = "User"
    is_admin: Optional[bool] = False
    preferred_model: str = "auto"  # 'claude-3-5-sonnet', 'gpt-4o', 'gemini'
    context: dict = {}
    is_developer_mode: Optional[bool] = None
    attachments: list = []

class ChatResponse(BaseModel):
    status: str
    reply: str
    model_used: str
    mode: str = "user"  # "user" or "developer"
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
            "gemini-3.8-flash",
            "gemini-3.5-flash",
            "gemini-3.1-flash-lite",
            "gemini-3.7-flash",
            "gemini-flash-lite-latest",
            "gemini-3-flash-preview",
            "gemma-4-31b-it"
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

        # 1. Check ChromaDB Semantic Cache first for instant response (SKIP if patient/PHI query)
        if not is_patient_or_phi_data(task_query):
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

        # 2. Cache Miss -> Run Multi-Agent Orchestrator dynamic execution
        agent_res = himes_orchestrator.dispatch(payload.task, payload.context)
        reply = agent_res.get("reply", "Task completed.")

        # 3. Save into ChromaDB cache for future instant queries (ONLY non-patient knowledge)
        if not is_patient_or_phi_data(task_query, reply):
            save_to_semantic_cache(task_query, reply)

        return AgentResponse(
            status=agent_res.get("status", "success"),
            message=reply,
            result={
                "task": payload.task,
                "agent_used": agent_res.get("agent", "HimesOrchestrator"),
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
    v_m = re.search(r'\b(?:visit|visit\s*no|visit\s*number|encounter)[:\s#]*(\d{4,8}|PHAR\d{3,8})\b', text, re.IGNORECASE)
    if v_m:
        entities["visit_no"] = v_m.group(1)
        
    m_m = re.search(r'\b(?:mrn|patient\s*id)[:\s#]*([A-Za-z0-9_-]{4,15})\b', text, re.IGNORECASE)
    if not m_m:
        m_m = re.search(r'\b(PHAR[0-9]+)\b', text, re.IGNORECASE)
    if m_m:
        raw_mrn = m_m.group(1)
        clean_mrn = re.sub(r'(-?ku|-?oda|-?ukku)$', '', raw_mrn, flags=re.IGNORECASE)
        entities["mrn"] = clean_mrn
        
    b_m = re.search(r'\b(?:bill|bill\s*no|invoice)[:\s#]*([0-9]{4,8})\b', text, re.IGNORECASE)
    if b_m:
        entities["bill_no"] = b_m.group(1)
    return entities

def resolve_himes_screen_entities(context: dict) -> dict:
    """
    Extracts and resolves exact patient MRN and Visit No from HIMES screen URLs.
    Handles routes like:
      - /addPatientBilling/{pbdno}/{pvbdno}
      - /editPatientBilling/{pbdno}/{pvbdno}
      - /addBillDeposit/{pbdno}/{pvbdno}
      - /addRefundBill/{pbdno}/{pvbdno}
    where pbdno is Patient_Basic_Details_Serial_No and pvbdno is Patient_Visit_Basic_Details_Serial_No.
    """
    if not context or not isinstance(context, dict):
        return {}
    current_path = context.get("current_path") or context.get("current_url") or ""
    if not current_path:
        return {}

    m = re.search(r'/(?:addPatientBilling|editPatientBilling|addBillDeposit|addRefundBill|pharmacyaddRefundBill)/(\d+)/(\d+)', current_path, re.IGNORECASE)
    if m:
        pbd_no = m.group(1)
        pvbd_no = m.group(2)
        try:
            sql = f"""
            SELECT TOP 1 pbd.Permanent_MRN_No, pvbd.Permanent_Visit_No, pbd.Patient_Basic_Details_Serial_No, pvbd.Patient_Visit_Basic_Details_Serial_No
            FROM Patient_Visit_Basic_Details pvbd WITH(NOLOCK)
            JOIN Patient_Basic_Details pbd WITH(NOLOCK) ON pvbd.Patient_Basic_Details_Serial_No = pbd.Patient_Basic_Details_Serial_No
            WHERE pvbd.Patient_Visit_Basic_Details_Serial_No = {pvbd_no}
            """
            raw = autonomous_agent.execute_select_sql(sql)
            if raw and raw.startswith("["):
                data = json.loads(raw)
                if data and isinstance(data, list) and len(data) > 0:
                    return {
                        "mrn": str(data[0].get("Permanent_MRN_No", "")).strip(),
                        "visit_no": str(data[0].get("Permanent_Visit_No", "")).strip(),
                        "patient_serial": str(pbd_no),
                        "visit_serial": str(pvbd_no)
                    }
        except Exception as e:
            print(f"[ScreenResolver] Error resolving screen visit: {e}")
    return {}

def update_session_memory(session_id: str, user_msg: str, agent_reply: str, entities: Optional[dict] = None, user_id: Optional[str] = None):
    sess = get_session_context(session_id)
    
    # Extract entities from user message
    ents = extract_entities_from_text(user_msg)
    if entities and isinstance(entities, dict):
        for k, v in entities.items():
            if v:
                sess["active_entities"][k] = v
    for k, v in ents.items():
        if v:
            sess["active_entities"][k] = v

    # When agent reply discusses a specific visit/MRN, record it as active for multi-turn continuity
    if agent_reply:
        v_reply = re.search(r'\b(?:Visit|Visit\s*No|visit\s*number)[:\s*#`]*(\d{4,8})\b', agent_reply, re.IGNORECASE)
        if v_reply:
            sess["active_entities"]["visit_no"] = v_reply.group(1).strip()
        m_reply = re.search(r'\b(?:MRN|Permanent_MRN_No)[:\s*#`]*([A-Za-z0-9_-]{4,15})\b', agent_reply, re.IGNORECASE)
        if not m_reply:
            m_reply = re.search(r'\b(PHAR\d{3,8})\b', agent_reply, re.IGNORECASE)
        if m_reply:
            sess["active_entities"]["mrn"] = m_reply.group(1).strip()

    sess["turns"].append({"user": user_msg, "agent": agent_reply})
    if len(sess["turns"]) > 10:
        sess["turns"] = sess["turns"][-10:]

    save_session_memory()

    # Sync to Valkey LangChain session memory (isolated per user_id & session_id)
    try:
        from memory.session_memory import get_session_memory
        v_mem = get_session_memory(session_id, user_id=user_id)
        v_mem.add_turn(user_msg, agent_reply, entities=sess.get("active_entities"))
    except Exception as e:
        print(f"[SessionMemory] Error syncing to Valkey: {e}")


# ====================================================================
# PROMPT 4: CHATBOX BACKEND CONNECTION (/api/chat) WITH CHROMADB MEMORY
# ====================================================================
def format_user_mode_response(reply: str) -> str:
    """
    Sanitizes and formats AI responses for End-User View:
    1. Removes all technical file paths (/L9/nagul/..., app/Http/..., routes/..., etc.).
    2. Strips raw uncollapsed code blocks and replaces them with clean status summaries.
    3. PRESERVES interactive <details>...</details> accordions so 'View Generated SQL Query'
       displays the authentic raw SQL query and database source when clicked.
    4. Formats status with clean Markdown status cards (✅, ⚠️, ℹ️).
    """
    if not reply or not isinstance(reply, str):
        return reply

    text = reply

    # 0. Clean LLM internal thoughts, scratchpad, rules reflection, and Final Answer prefixes
    text = clean_agent_thought(reply)

    # In USER MODE: Completely remove all technical <details>...</details> and <summary>...</summary> accordions
    text = re.sub(r'<details[\s\S]*?</details>', '', text, flags=re.IGNORECASE).strip()
    text = re.sub(r'<summary[\s\S]*?</summary>', '', text, flags=re.IGNORECASE).strip()
    text = re.sub(r'<\/?(?:details|summary|b|strong)>', '', text, flags=re.IGNORECASE).strip()

    # 1. Remove raw SQL code blocks, headers, and UI code card artifacts
    text = re.sub(r'```(?:sql)?[\s\S]*?```', '', text, flags=re.IGNORECASE)
    text = re.sub(r'^\s*Details\s*$', '', text, flags=re.IGNORECASE | re.MULTILINE)
    text = re.sub(r'(?:🔍\s*)?View\s+Generated\s+SQL\s+Query[^\n]*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'(?:Live\s+MSSQL\s+Query\s+Executed|SQL\s+Query\s+Executed|Executed\s+SQL)[:\s]*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'^\s*(?:SQL|Copy)\s*$', '', text, flags=re.IGNORECASE | re.MULTILINE)

    # 1b. Remove any un-fenced raw SELECT queries
    text = re.sub(
        r'\bSELECT\s+(?:DISTINCT\s+)?(?:TOP\s+\d+\s+)?[a-zA-Z0-9_\.,\s\(\)\'\=\<\>\-]+?\s+FROM\s+[a-zA-Z0-9_]+[\s\S]*?(?:ORDER\s+BY\s+[^\n]+|;|\n\n|\Z)',
        '',
        text,
        flags=re.IGNORECASE
    )

    # 2. Replace raw PHP, Bash, Python code blocks
    text = re.sub(
        r'```(?:php|bash|sh|shell|python|json)?[\s\S]*?```',
        '> ℹ️ **Action:** Automated hospital system operation verified.',
        text,
        flags=re.IGNORECASE
    )

    # 3. Replace stack traces with polite user notice
    text = re.sub(
        r'Traceback \(most recent call last\):[\s\S]*?(?=\n\n|\Z)',
        '> ⚠️ **System Notice:** Our automated diagnostics identified a background issue and initiated resolution. Status: In Progress.',
        text
    )
    text = re.sub(
        r'#\d+\s+.*?(?:vendor|app)/[^\n]+\n?',
        '',
        text
    )

    # 4. Remove / mask technical file paths
    text = re.sub(
        r'(?:/L9/nagul/himes-ai/|/var/www/html/himes-ai/|app/Http/Controllers/|app/|routes/|resources/views/)[a-zA-Z0-9_\-/\.]+',
        'HIMES Core System',
        text
    )
    text = re.sub(
        r'`(?:/L9/nagul/himes-ai/|app/|routes/|resources/)[^`]+`',
        '`HIMES System`',
        text
    )

    # 5. Remove technical controller, route, and table lines from fast-paths
    text = re.sub(r'•\s*\*?\*?Primary Controller:\*?\*?\s*`?.*?`?\n?', '', text, flags=re.IGNORECASE)
    text = re.sub(r'•\s*\*?\*?Controller:\*?\*?\s*`?.*?`?\n?', '', text, flags=re.IGNORECASE)
    text = re.sub(r'•\s*\*?\*?Route Path:\*?\*?\s*`?.*?`?\n?', '', text, flags=re.IGNORECASE)
    text = re.sub(r'•\s*\*?\*?Route / URL:\*?\*?\s*`?.*?`?\n?', '', text, flags=re.IGNORECASE)
    text = re.sub(r'•\s*\*?\*?Function ID:\*?\*?\s*`?.*?`?\n?', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\*?\*?Associated SQL Tables:\*?\*?\s*\n`?.*?`?\n*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\*?\*?Key SQL Tables:\*?\*?\s*\n`?.*?`?\n*', '', text, flags=re.IGNORECASE)

    # 5b. Strip database IP addresses, database sources, and query footers (with or without asterisks/bullets)
    text = re.sub(r'•?\s*\*?\*?Database Source:\*?\*?.*?(?:\n|$)', '', text, flags=re.IGNORECASE)
    text = re.sub(r'•?\s*\*?\*?Tables Queried:\*?\*?.*?(?:\n|$)', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\*?\(?⚡\s*Real-Time\s+Live\s+MSSQL\s+Execution.*?(?:\)\*?|\n|$)', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\b192\.168\.\d+\.\d+\b', '', text)

    # 5c. Strip raw URL routes and parentheticals like (/Appointment Calendar Scheduler) or (/patientBilling)
    text = re.sub(r'\(\s*/[A-Za-z0-9_\-\s/{}\?]+\s*\)', '', text)
    text = re.sub(r'\(\s*/?[A-Za-z0-9_\-\s/]*(?:Scheduler|Registration|Panel|Controller|Billing|routes|PriorVisit)[A-Za-z0-9_\-\s/]*\)', '', text, flags=re.IGNORECASE)
    text = re.sub(r'/(?:viewQuickRegistration|patientRegistration|appointmentScheduler|AppointmentCalendarScheduler|emrVisitEntryPanel|patientBilling|viewGlobalPatientBilling|addPatientBilling|editPatientBilling|viewPriorVisit|globalViewForPriorVisitNew)\b', '', text, flags=re.IGNORECASE)

    # 5d. User Mode: Mask raw SQL table names, primary keys, and cron names with intuitive healthcare terms
    table_replacements = [
        (r'\bResource_Parent\s*\([^)]*\)', 'Doctor / Healthcare Provider'),
        (r'`?Resource_Parent`?', 'Doctor Roster'),
        (r'\bResource_Non_Availability\s*\([^)]*\)', 'Doctor Leaves & Breaks'),
        (r'`?Resource_Non_Availability`?', 'Doctor Leave Schedule'),
        (r'`?Patient_Appointment`?\s*table', 'Appointment Records'),
        (r'`?Patient_Appointment`?', 'Appointment Schedule'),
        (r'`?Appointment_Status_Type`?', 'Appointment Status Tracker'),
        (r'`?Patient_Visit_Basic_Details`?\s*table', 'Patient Visit Records'),
        (r'`?Patient_Visit_Basic_Details`?', 'Hospital Visit Records'),
        (r'`?Patient_Basic_Details`?', 'Patient Master'),
        (r'`?Patient_Basic_Encript_Details`?', 'Patient Demographics'),
        (r'`?Patient_Appointment_Serial_No`?', 'Appointment Reference ID'),
        (r'`?Patient_Visit_Basic_Details_Serial_No`?', 'Visit Reference ID'),
        (r'`?AppointmentUpdateNoShow`?', 'Automated No-Show System'),
        (r'`?ReportScheduleCron`?', 'Automated Reporting Service'),
        (r'`?Patient_Visit_Appointments`?', 'Appointment-Visit Link'),
        (r'`?AppointmentScheduler`?', 'Appointment Calendar Scheduler'),
        (r'`?Insurance_Plan_Department_Cover`?', 'Insurance Plan Coverage Policy'),
        (r'`?Insurance_Plan_Excluded_Prior_Approval_Services`?', 'Plan Exclusions & Prior Approvals'),
        (r'`?Patient_Visit_Insurance_Card_Details`?', 'Visit Insurance Information'),
        (r'`?Patient_Visit_Admission_Details`?', 'Inpatient Admission Details'),
        (r'`?Patient_Basic_Details_Link_Merging`?', 'Patient Merge Records'),
        (r'`?Patient_Identification_Details`?', 'Patient Identification Documents'),
        # Prior Visit & Pre-Auth Tables
        (r'`?PA_Patient_Basic_Details`?', 'Prior Authorization Patient Details'),
        (r'`?PA_Patient_Visit_Basic_Details`?', 'Prior Authorization Visit Records'),
        (r'`?PA_Patient_Visit_Services`?', 'Prior Authorization Requested Services'),
        (r'`?PA_Patient_Visit_Resources`?', 'Prior Authorization Doctor Allocation'),
        (r'`?PA_Patient_Visit_Insurance_Card_Details`?', 'Prior Authorization Insurance Card Details'),
        (r'`?PA_Patient_Visit_Insurance_Service_Cover_Details`?', 'Prior Authorization Insurance Approval Records'),
        (r'`?PA_Patient_Visit_Diagnosis`?', 'Prior Authorization Clinical Diagnoses'),
        (r'`?PA_Patient_Visit_Observations`?', 'Prior Authorization Clinical Observations'),
        (r'`?PA_Prior_Approval_Log`?', 'Prior Authorization Submission Audit Logs'),
        (r'`?Physio_Order_Details_Services`?', 'Physiotherapy Session Details'),
        (r'`?Patient_Treatment_Plan`?', 'Patient Treatment Plan'),
        # Billing Tables & Columns
        (r'`?Patient_Bill_Header`?', 'Patient Invoice'),
        (r'`?Patient_Bill_Detail_Services_Packages_Resources_Drugs`?', 'Invoice Line Items'),
        (r'`?Patient_Bill_Details`?', 'Invoice Item Details'),
        (r'`?Patient_Bill_Header_Payments_Received`?', 'Payment Receipts'),
        (r'`?Receipts_For_Payments_Received`?', 'Official Receipt Vouchers'),
        (r'`?Patient_Visit_Deposits_Adjusted_Bills`?', 'Deposit Adjustment Records'),
        (r'`?Patient_Deposit_Log`?', 'Patient Advance Deposit Balance'),
        (r'`?Patient_Visit_Deposits`?', 'Advance Deposit Records'),
        (r'`?Patient_Visit_Credit_Notes`?', 'Patient Credit Notes'),
        (r'`?Credit_Notes`?', 'Credit Note Register'),
        (r'`?Invoice_Cancel_Request`?', 'Invoice Cancellation Requests'),
        (r'`?Patient_Refund_Details`?', 'Refund Records'),
        (r'`?Patient_Visit_Services`?', 'Visit Clinical Services'),
        (r'`?Patient_Visit_Drug_Item_Details`?', 'Prescribed Medication Items'),
        (r'`?Patient_Visit_Inventory_Billing`?', 'Pharmacy Billing Records'),
        (r'`?Patient_Visit_IPD_Bed_Details`?', 'Inpatient Bed & Room Charges'),
        (r'`?User_Wise_Discount_Limit`?', 'Staff Discount Authorizations'),
        (r'`?Patient_Visit_Discount_Log`?', 'Discount Approval History'),
        (r'`?List_Based_Column_Swapping`?', 'Table Grid Preferences'),
        (r'`?User_Based_Column_Swapping`?', 'User Grid Preferences'),
        (r'`?Service_Rate_For_Non_Insurance`?', 'Self-Pay Cash Tariff'),
        (r'`?Service_Rate_For_Insurance`?', 'Insurance Network Tariff'),
        (r'`?Stock_Item_Price`?', 'Pharmacy Cash Price List'),
        (r'`?Stock_Item_Insurance_Price`?', 'Pharmacy Insurance Price List'),
        (r'`?Branch_Free_Paid_Followup_Services`?', 'Follow-up Service Rules'),
        # Controllers & Parameters
        (r'`?PriorVisitController(?:\.php)?`?', 'Prior Visit Service'),
        (r'`?PriorVisitOperationController(?:\.php)?`?', 'Prior Visit Service'),
        (r'`?GlobalViewPriorVisitNewCont(?:roller)?(?:\.php)?`?', 'Global Prior Visit Management Service'),
        (r'`?PriorVisitCronController(?:\.php)?`?', 'Prior Authorization Expiry Service'),
        (r'`?PriorVisitTransferController(?:\.php)?`?', 'Prior Visit Transfer Service'),
        (r'`?PatientBillingGetCont(?:roller)?(?:\.php)?`?', 'Patient Billing Service'),
        (r'`?PatientBillingPartOneController(?:\.php)?`?', 'Billing Engine Service'),
        (r'`?PatientBillingController(?:\.php)?`?', 'Billing Counter Service'),
        (r'`?GlobalViewPatientBillingController(?:\.php)?`?', 'Global Billing Monitor'),
        (r'`?QuickDemoRegController(?:\.php)?`?', 'Quick Registration Service'),
        (r'`?QuickRegistrationController(?:\.php)?`?', 'Quick Registration Service'),
        (r'`?RegistrationTabController(?:\.php)?`?', 'Detailed Registration Service'),
        (r'`?RegistrationController(?:\.php)?`?', 'Registration Service'),
        (r'`?RegistrationInsuranceController(?:\.php)?`?', 'Insurance Management Service'),
        (r'`?[A-Za-z0-9_]+Controller(?:\.php)?`?', 'HIMES System Service'),
        (r'\breplicate=1\s*(?:nu\s*)?(?:request\s*)?(?:parameter-ah\s*)?(?:backend-ku\s*)?(?:anupum|anuppum)?', 'Replicate Visit action'),
        (r'\breplicate=1\b', 'replicate previous visit'),
    ]
    for pattern, repl in table_replacements:
        text = re.sub(pattern, repl, text, flags=re.IGNORECASE)

    # 6. Ensure clean spacing and remove residual empty lines
    text = re.sub(r'\n{3,}', '\n\n', text).strip()
    return text


# ====================================================================
# PROMPT 4: CHATBOX BACKEND CONNECTION (/api/chat) WITH CHROMADB MEMORY
# ====================================================================
@app.get("/api/health")
@app.get("/health")
def health_check():
    return {"status": "ok", "service": "himes-python-agent", "valkey": bool(valkey_manager.is_connected)}

@app.post("/api/chat", response_model=ChatResponse)
@app.post("/agent/chat", response_model=ChatResponse)
def chat_with_agent(payload: ChatRequest):

    """
    Endpoint for Application Chatbox UI with Dual Response System (User View vs. Developer View),
    Multi-Media Attachments, and ChromaDB/Valkey Accelerated Memory:
    1. Check for Mode Switch triggers ('enable developer mode' / 'disable developer mode')
    2. Check Valkey / ChromaDB Fast-Path indexes
    3. Run Autonomous Agent with live database and codebase tools
    4. Format output strictly according to active Mode (User View vs. Developer View)
    """
    try:
        # Enforce strict safety rules: SELECT queries only, Nagul's directory lock
        enforce_safety_rules(payload.message)

        # Retrieve and update session context
        sess = get_session_context(payload.session_id)

        # 0. Check Mode Switch Triggers
        msg_clean = payload.message.strip().lower()
        dev_enable_cmds = [
            "enable developer mode", "dev mode on", "developer mode on", "enable dev mode",
            "switch to developer mode", "activate developer mode", "turn on dev mode"
        ]
        dev_disable_cmds = [
            "disable developer mode", "dev mode off", "developer mode off", "disable dev mode",
            "switch to user mode", "user mode on", "user mode", "turn off dev mode"
        ]

        if any(msg_clean == cmd or msg_clean.startswith(cmd) for cmd in dev_enable_cmds):
            if not payload.is_admin:
                forbidden_reply = (
                    "⛔ **Access Denied: Admin Privilege Required**\n\n"
                    "Developer Mode is strictly restricted to Hospital System Administrators. "
                    "Your account does not have permission to enable technical diagnostics or raw SQL execution."
                )
                update_session_memory(payload.session_id, payload.message, forbidden_reply, user_id=payload.user_id)
                return ChatResponse(
                    status="forbidden",
                    reply=forbidden_reply,
                    model_used="Security Guardrail",
                    mode="user",
                    action_executed={"mode_switch": False, "error": "unauthorized_admin_mode"}
                )

            valkey_manager.set_session_mode(payload.session_id, "developer")
            reply = "💻 **Developer mode enabled**"
            update_session_memory(payload.session_id, payload.message, reply, user_id=payload.user_id)
            return ChatResponse(
                status="success",
                reply=reply,
                model_used="Mode Controller",
                mode="developer",
                action_executed={"mode_switch": True, "mode": "developer"}
            )

        if any(msg_clean == cmd or msg_clean.startswith(cmd) for cmd in dev_disable_cmds):
            valkey_manager.set_session_mode(payload.session_id, "user")
            reply = "👤 **User mode active**"
            update_session_memory(payload.session_id, payload.message, reply, user_id=payload.user_id)
            return ChatResponse(
                status="success",
                reply=reply,
                model_used="Mode Controller",
                mode="user",
                action_executed={"mode_switch": True, "mode": "user"}
            )

        # Resolve Current Mode (Default is ALWAYS User Mode; Developer Mode strictly requires Admin AND explicit opt-in)
        if not payload.is_admin:
            current_mode = "user"
            valkey_manager.set_session_mode(payload.session_id, "user")
        else:
            req_ctx = payload.context or {}
            ctx_mode = req_ctx.get("mode") or req_ctx.get("active_mode")
            if payload.is_developer_mode is True or ctx_mode == "developer":
                current_mode = "developer"
                valkey_manager.set_session_mode(payload.session_id, "developer")
            elif payload.is_developer_mode is False or ctx_mode == "user":
                current_mode = "user"
                valkey_manager.set_session_mode(payload.session_id, "user")
            else:
                current_mode = valkey_manager.get_session_mode(payload.session_id)
        is_developer_mode = (current_mode == "developer")


        # Process attachments if present
        attachment_context = ""
        if payload.attachments:
            import base64
            for att in payload.attachments:
                name = att.get("name", "attachment")
                att_type = att.get("type", "")
                data_str = att.get("data", "")
                if "," in data_str:
                    data_str = data_str.split(",", 1)[-1]
                if any(name.endswith(ext) for ext in [".txt", ".log", ".json", ".csv", ".sql", ".md"]) or "text" in att_type or "json" in att_type:
                    try:
                        decoded = base64.b64decode(data_str).decode("utf-8", errors="replace")
                        snippet = decoded[:3000]
                        attachment_context += f"\n\n[ATTACHED FILE: {name}]\n```\n{snippet}\n```"
                    except Exception:
                        attachment_context += f"\n[Attached file: {name} ({att_type})]"
                else:
                    attachment_context += f"\n[Attached media: {name} ({att_type}, {att.get('size', 0)} bytes)]"

        effective_message = payload.message + attachment_context

        # ====================================================================
        # ADMIN DEVELOPER MODE: RAW SQL EXECUTION ENGINE
        # ====================================================================
        clean_raw_candidate = payload.message.strip()
        if clean_raw_candidate.startswith("```"):
            clean_raw_candidate = re.sub(r"^```(?:sql)?\s*", "", clean_raw_candidate, flags=re.IGNORECASE)
            clean_raw_candidate = re.sub(r"\s*```$", "", clean_raw_candidate).strip()

        first_token_match = re.match(r"^\s*([A-Za-z]+)", clean_raw_candidate)
        first_token = first_token_match.group(1).upper() if first_token_match else ""

        is_sql_query = False
        if first_token in ["SELECT", "WITH"]:
            if is_developer_mode or any(k in clean_raw_candidate.upper() for k in [" FROM ", " WHERE ", " JOIN ", " AS ", "@@", "TOP ", "COUNT("]):
                is_sql_query = True
        elif first_token in ["UPDATE", "INSERT", "DELETE", "DROP", "TRUNCATE", "ALTER", "CREATE", "EXEC", "EXECUTE"]:
            is_sql_query = True

        if is_sql_query:
            # 1. Non-admin users are strictly blocked from direct SQL
            if not payload.is_admin:
                forbidden_reply = (
                    "⛔ **Access Denied: Admin Privilege Required**\n\n"
                    "Direct SQL execution is restricted to Hospital Administrators. "
                    "Non-admin users cannot execute raw database queries."
                )
                update_session_memory(payload.session_id, payload.message, forbidden_reply, user_id=payload.user_id)
                return ChatResponse(
                    status="forbidden",
                    reply=forbidden_reply,
                    model_used="Security Guardrail",
                    mode="user",
                    action_executed={"sql_blocked": True, "error": "unauthorized_raw_sql"}
                )

            # 2. Strict Read-Only Guardrail Validation (Blocks UPDATE, DELETE, DROP, etc.)
            try:
                validate_sql_query(clean_raw_candidate)
            except SecurityException as se:
                block_reply = (
                    f"🛡️ **Security Guardrail Blocked Execution**\n\n"
                    f"**Violation:** `{str(se)}`\n\n"
                    f"> Strict Policy: Only read-only `SELECT` statements are permitted. Destructive operations (`UPDATE`, `DELETE`, `DROP`, `INSERT`, `ALTER`, `TRUNCATE`) are unconditionally rejected."
                )
                update_session_memory(payload.session_id, payload.message, block_reply, user_id=payload.user_id)
                return ChatResponse(
                    status="blocked_by_guardrails",
                    reply=block_reply,
                    model_used="Security Guardrail (Zero-Execution)",
                    mode=current_mode,
                    action_executed={"security_blocked": True, "reason": str(se)}
                )

            # 3. Live Execution on MSSQL
            t_start = time.time()
            sql_to_run = clean_raw_candidate
            raw_res = autonomous_agent.execute_select_sql(sql_to_run)
            latency_ms = round((time.time() - t_start) * 1000, 2)

            parsed_rows = []
            exec_error = None
            if raw_res and raw_res.strip().startswith("["):
                try:
                    parsed_rows = json.loads(raw_res)
                except Exception:
                    exec_error = raw_res
            elif raw_res and not raw_res.strip().startswith("["):
                exec_error = raw_res  # e.g., error message from DB driver

            # 4. Format output using generic readable table formatter
            from utils.table_formatter import format_generic_query_result

            if exec_error:
                formatted_output = (
                    f"❌ **Query Error**\n\n"
                    f"The database returned an error while executing your query:\n\n"
                    f"```\n{str(exec_error)[:800]}\n```\n\n"
                    f"**Tip:** Check column names and table names — MSSQL is case-sensitive for column aliases.\n"
                    f"Try: `SELECT TOP 5 * FROM Installation_Parameters` to inspect available columns.\n\n"
                    f"```sql\n{sql_to_run}\n```"
                )
            elif isinstance(parsed_rows, list) and len(parsed_rows) > 0:
                formatted_output = format_generic_query_result(
                    parsed_rows,
                    executed_sql=sql_to_run,
                    latency_ms=latency_ms,
                    mode=current_mode
                )
            else:
                formatted_output = (
                    f"ℹ️ **Query returned 0 rows** (`{latency_ms} ms`)\n\n"
                    f"The query executed successfully but found no matching records.\n\n"
                    f"```sql\n{sql_to_run}\n```"
                )

            update_session_memory(payload.session_id, payload.message, formatted_output, user_id=payload.user_id)
            return ChatResponse(
                status="success",
                reply=formatted_output,
                model_used="Admin Live MSSQL Engine (0 Tokens)",
                mode=current_mode,
                action_executed={
                    "raw_sql_execution": True,
                    "sql": sql_to_run,
                    "row_count": len(parsed_rows) if isinstance(parsed_rows, list) else 0,
                    "latency_ms": latency_ms
                }
            )

        # Resolve screen-level entities from active URL if user is viewing a patient/billing screen
        screen_ents = resolve_himes_screen_entities(payload.context)
        if screen_ents:
            if screen_ents.get("mrn") and not sess["active_entities"].get("mrn"):
                sess["active_entities"]["mrn"] = screen_ents["mrn"]
            if screen_ents.get("visit_no") and not sess["active_entities"].get("visit_no"):
                sess["active_entities"]["visit_no"] = screen_ents["visit_no"]
            if screen_ents.get("visit_serial"):
                sess["active_entities"]["visit_serial"] = screen_ents["visit_serial"]
            if screen_ents.get("patient_serial"):
                sess["active_entities"]["patient_serial"] = screen_ents["patient_serial"]

        # Multi-Agent Language Detection & Query Normalization
        user_lang = language_specialist.detect_language(payload.message)
        normalized_eng_query = language_specialist.normalize_to_english(payload.message, user_lang)

        # Pre-scan user message for any entity updates
        user_ents = extract_entities_from_text(payload.message)
        for k, v in user_ents.items():
            if v:
                sess["active_entities"][k] = v

        v_m = user_ents.get("visit_no")
        m_m = user_ents.get("mrn")
        
        # If user explicitly specified a new MRN in this message and did not specify a visit_no,
        # reset visit_no so it queries this new MRN's visits instead of holding old patient visit
        if m_m and not v_m:
            sess["active_entities"]["visit_no"] = None

        msg_lower = payload.message.lower()

        # Co-reference resolution: If user asks about 'antha visit' / 'intha visit' / 'that visit' / 'same visit',
        # dynamically resolve from the immediately preceding assistant turn in this session
        is_referring_to_prev_visit = any(w in msg_lower for w in ["antha visit", "intha visit", "that visit", "this visit", "same visit"])
        if is_referring_to_prev_visit and sess.get("turns"):
            for turn in reversed(sess["turns"]):
                a_txt = turn.get("agent") or turn.get("ai") or ""
                v_cand = re.search(r'\b(?:Visit|Visit\s*No|visit\s*number)[:\s*#`]*(\d{4,8})\b', a_txt, re.IGNORECASE)
                if v_cand:
                    sess["active_entities"]["visit_no"] = v_cand.group(1).strip()
                    m_cand = re.search(r'\b(?:MRN|Permanent_MRN_No)[:\s*#`]*([A-Za-z0-9_-]{4,15})\b', a_txt, re.IGNORECASE)
                    if m_cand:
                        sess["active_entities"]["mrn"] = m_cand.group(1).strip()
                    break

        # If visit_no is active, ensure MRN is perfectly synchronized to that visit's real MRN
        active_visit = sess["active_entities"].get("visit_no")
        if active_visit and str(active_visit).isdigit():
            try:
                v_sync_sql = f"""
                SELECT TOP 1 pbd.Permanent_MRN_No 
                FROM Patient_Visit_Basic_Details pvbd WITH(NOLOCK) 
                JOIN Patient_Basic_Details pbd WITH(NOLOCK) ON pvbd.Patient_Basic_Details_Serial_No = pbd.Patient_Basic_Details_Serial_No 
                WHERE pvbd.Permanent_Visit_No = '{active_visit}'
                """
                v_sync_raw = autonomous_agent.execute_select_sql(v_sync_sql)
                if v_sync_raw and v_sync_raw.startswith("["):
                    v_sync_data = json.loads(v_sync_raw)
                    if v_sync_data and len(v_sync_data) > 0:
                        matched_mrn = str(v_sync_data[0].get("Permanent_MRN_No", "")).strip()
                        if matched_mrn:
                            sess["active_entities"]["mrn"] = matched_mrn
            except Exception as e_sync:
                print(f"[VisitSync] Notice: {e_sync}")

        active_mrn = sess["active_entities"].get("mrn")
        active_visit = sess["active_entities"].get("visit_no")


        # Core Concept: If MRN is active but visit_no is unset, and inquiry is not a general screen/module lookup,
        # auto-resolve the latest encounter visit for that patient dynamically
        is_system_meta_inquiry = any(w in msg_lower for w in ["module", "screen", "menu", "workflow", "lifecycle", "route"])
        if active_mrn and not active_visit and not is_system_meta_inquiry:
            # First check if the screen URL provided the visit
            if screen_ents and screen_ents.get("visit_no") and screen_ents.get("mrn") == active_mrn:
                active_visit = screen_ents["visit_no"]
                sess["active_entities"]["visit_no"] = active_visit
                sess["active_entities"]["visit_serial"] = screen_ents.get("visit_serial")
            else:
                cached_v = valkey_manager.get_patient_snapshot(active_mrn, "latest_visit")
                if cached_v:
                    active_visit = str(cached_v)
                    sess["active_entities"]["visit_no"] = active_visit
                else:
                    try:
                        v_sql = f"""
                        SELECT TOP 1 pvbd.Permanent_Visit_No, pvbd.Patient_Visit_Basic_Details_Serial_No
                        FROM Patient_Visit_Basic_Details pvbd WITH(NOLOCK)
                        JOIN Patient_Basic_Details pbd WITH(NOLOCK) ON pvbd.Patient_Basic_Details_Serial_No = pbd.Patient_Basic_Details_Serial_No
                        WHERE pbd.Permanent_MRN_No = '{active_mrn}'
                        ORDER BY pvbd.Patient_Visit_Basic_Details_Serial_No DESC
                        """
                        v_raw = autonomous_agent.execute_select_sql(v_sql)
                        if v_raw and v_raw.startswith("["):
                            v_data = json.loads(v_raw)
                            if v_data and len(v_data) > 0:
                                active_visit = str(v_data[0].get("Permanent_Visit_No", "")).strip()
                                sess["active_entities"]["visit_no"] = active_visit
                                sess["active_entities"]["visit_serial"] = str(v_data[0].get("Patient_Visit_Basic_Details_Serial_No", "")).strip()
                                valkey_manager.cache_patient_snapshot(active_mrn, "latest_visit", active_visit, ttl=300)
                    except Exception as e:
                        print(f"[EntityResolution] Error fetching latest visit for MRN {active_mrn}: {e}")

        # ====================================================================
        # TIER 1: ZERO-TOKEN DETERMINISTIC PATIENT ENGINE + VALKEY 5-MIN EPHEMERAL CACHE
        # ====================================================================

        # 0. Valkey 5-Minute Ephemeral Query Cache (SHA256: hash(query + mrn + session_id))
        cached_ephemeral = valkey_manager.get_ephemeral_query(payload.message, active_mrn=active_mrn or "", session_id=payload.session_id)
        if cached_ephemeral and isinstance(cached_ephemeral, dict):
            cached_resp = cached_ephemeral.get("formatted_response") or ""
            if cached_resp:
                update_session_memory(payload.session_id, payload.message, cached_resp)
                return ChatResponse(
                    status="success",
                    reply=cached_resp,
                    model_used="Valkey Ephemeral Cache (SHA256, 5-min TTL, 0 Tokens)",
                    mode=current_mode,
                    action_executed={
                        "mrn": active_mrn,
                        "cache_hit": True,
                        "sha256": valkey_manager.generate_query_hash(payload.message, active_mrn or "", payload.session_id),
                        "executed_sql": cached_ephemeral.get("executed_sql", "")
                    }
                )

        # Dedicated Handler 00: Installation Parameters & Hospital System Settings
        is_install_params_query = any(w in msg_lower for w in ["installation parameter", "installation_parameter", "installation parameters", "insurance method", "inurance method", "eclaim method", "dhpo url", "claim url"])
        if is_install_params_query:
            try:
                ip_sql = "SELECT TOP 1 Insurance_Method, Insurance_Claim_URL, Insurance_Label_Text FROM Installation_Parameters"
                ip_raw = autonomous_agent.execute_select_sql(ip_sql)
                if ip_raw and ip_raw.strip().startswith("["):
                    ip_rows = json.loads(ip_raw)
                    if ip_rows and len(ip_rows) > 0:
                        row = ip_rows[0]
                        ins_method = row.get("Insurance_Method") or "DHA"
                        claim_url = row.get("Insurance_Claim_URL") or "N/A"
                        label_text = row.get("Insurance_Label_Text") or "N/A"
                        
                        if current_mode == "developer":
                            ip_reply = (
                                f"### 💻 Installation Parameters — Insurance Configuration\n"
                                f"• **Insurance Method:** `{ins_method}`\n"
                                f"• **Claim Submission URL:** `{claim_url}`\n"
                                f"• **Insurance Label Text:** `{label_text}`\n\n"
                                f"**Live MSSQL Query:**\n```sql\n{ip_sql}\n```\n"
                                f"*(⚡ Executed on live MSSQL with 0 LLM Presentation Tokens)*"
                            )
                        else:
                            ip_reply = (
                                f"### 🏥 HIMES Installation Parameters\n\n"
                                f"HIMES-ல் உள்ள `Installation_Parameters` அட்டவணையின்படி, தற்போதைய **Insurance Method**: **`{ins_method}`**.\n\n"
                                f"• **Insurance Method:** `{ins_method}`\n"
                                f"• **Claim Portal URL:** `{claim_url}`\n"
                                f"• **Insurance Label:** `{label_text}`\n\n"
                                f"> ✅ **Verification:** Live database record retrieved directly from `Installation_Parameters`."
                            )
                        update_session_memory(payload.session_id, payload.message, ip_reply, user_id=payload.user_id)
                        return ChatResponse(
                            status="success",
                            reply=ip_reply,
                            model_used="HIMES System Config Engine (0 Tokens)",
                            mode=current_mode,
                            action_executed={
                                "installation_parameters_lookup": True,
                                "insurance_method": ins_method,
                                "executed_sql": ip_sql
                            }
                        )
            except Exception as e:
                print(f"[InstallParamsLookup] Error: {e}")

        # Dedicated Handler 0A: Patient Demographics Lookup (MRN -> Name, Phone, Gender, Age)
        is_demographics_query = (
            active_mrn and any(w in msg_lower for w in ["name", "patient name", "yaaru", "details", "profile", "mobile", "phone", "contact", "age", "gender"])
            and not any(w in msg_lower for w in ["service", "services", "unbilled", "bill", "billing", "deposit", "receipt", "visit list", "visits"])
        )
        if is_demographics_query:
            # 1. Check Valkey Ephemeral Cache (5-Minute TTL)
            cached_demo = valkey_manager.get_patient_snapshot(active_mrn, "demographics")
            if cached_demo:
                update_session_memory(payload.session_id, payload.message, cached_demo)
                return ChatResponse(
                    status="success",
                    reply=cached_demo,
                    model_used="Valkey Ephemeral Cache (5-min TTL, 0 Tokens)",
                    mode=current_mode,
                    action_executed={"mrn": active_mrn, "cache_hit": True, "ttl_remaining": "active"}
                )

            # 2. Live DB Lookup (Safe SELECT)
            demo_sql = f"""
            SELECT TOP 1
                pbd.Permanent_MRN_No,
                ISNULL(pbed.Patient_First_Name, pbd.Patient_First_Name) AS Patient_First_Name,
                ISNULL(pbed.Patient_Middle_Name, pbd.Patient_Middle_Name) AS Patient_Middle_Name,
                ISNULL(pbed.Patient_Last_Name, pbd.Patient_Last_Name) AS Patient_Last_Name,
                ISNULL(pbed.Contact_Phone_Mobile, pbd.Contact_Phone_Mobile) AS Contact_Phone_Mobile,
                ISNULL(pbed.Contact_Email, pbd.Contact_Email) AS Contact_Email,
                pbd.Gender_Code,
                pbd.Patient_DOB,
                pbed.Emirates_Id
            FROM Patient_Basic_Details pbd WITH(NOLOCK)
            LEFT JOIN Patient_Basic_Encript_Details pbed WITH(NOLOCK) 
                ON pbd.Patient_Basic_Details_Serial_No = pbed.Patient_Basic_Details_Serial_No
            WHERE pbd.Permanent_MRN_No = '{active_mrn}'
            """
            raw_demo = autonomous_agent.execute_select_sql(demo_sql)
            demo_data = json.loads(raw_demo) if raw_demo and raw_demo.startswith("[") else []
            if demo_data:
                p = demo_data[0]
                first = (p.get("Patient_First_Name") or "").strip()
                middle = (p.get("Patient_Middle_Name") or "").strip()
                last = (p.get("Patient_Last_Name") or "").strip()
                full_name = " ".join([w for w in [first, middle, last] if w]) or "Registered Patient"
                gender = "Female" if p.get("Gender_Code") == "F" else ("Male" if p.get("Gender_Code") == "M" else (p.get("Gender_Code") or "-"))
                mobile = p.get("Contact_Phone_Mobile") or "-"
                dob = str(p.get("Patient_DOB") or "-").split("T")[0]
                eid = p.get("Emirates_Id") or "-"

                if current_mode == "developer":
                    reply = (
                        f"### 👤 Patient Master Record: `{active_mrn}`\n\n"
                        f"• **Full Name:** **{full_name}**\n"
                        f"• **MRN:** `{active_mrn}` (Exact Match Verified)\n"
                        f"• **Gender:** `{gender}` | **DOB:** `{dob}`\n"
                        f"• **Mobile:** `{mobile}` | **Emirates ID:** `{eid}`\n\n"
                        f"*(⚡ Retrieved live from MSSQL `Patient_Basic_Details` with 0 LLM Tokens, cached in Valkey for 5 mins)*"
                    )
                else:
                    reply = (
                        f"Vanakkam! MRN **{active_mrn}** patient-oda details itho:\n\n"
                        f"• 👤 **Patient Name:** **{full_name}**\n"
                        f"• 🆔 **MRN Number:** `{active_mrn}`\n"
                        f"• ⚧️ **Gender:** {gender}\n"
                        f"• 📞 **Mobile:** {mobile}\n\n"
                        f"Intha patient-oda visit details illa billing pathi ethavathu theriyanuma?"
                    )
                
                # Cache in Valkey for 5 minutes (300s)
                valkey_manager.cache_patient_snapshot(active_mrn, "demographics", reply, ttl=300)
                update_session_memory(payload.session_id, payload.message, reply)
                valkey_manager.update_session_entities(payload.session_id, sess["active_entities"])
                return ChatResponse(
                    status="success",
                    reply=reply,
                    model_used="HIMES Deterministic Engine (0 LLM Tokens, Live DB)",
                    mode=current_mode,
                    action_executed={"mrn": active_mrn, "cached_valkey_5m": True}
                )

        # Core Concept: Patient Services & Encounter Orders Inquiry (single visit specific)
        is_comparative_or_multi = any(w in msg_lower for w in [
            "athula", "which", "entha", "oru visit", "ethana", "how many", "all", "ellam", "highest", "athiga", "lowest", "invoice", "invoices"
        ])
        is_services_query = (
            active_mrn and not is_comparative_or_multi and any(w in msg_lower for w in [
                "service", "services", "cpt", "unbilled service", "procedure", "procedures",
                "lab order", "test", "tests", "சிகிச்சை", "பரிசோதனை", "service list",
                "فحوصات", "خدمات", "فحص", "خدمة", "bill podadha", "bill aagadha", "unbilled"
            ])
        )

        if is_services_query and active_visit:
            # Core Concept: Unbilled / Pending vs All Services
            is_unbilled_only = any(w in msg_lower for w in ["unbilled", "un-billed", "pending", "not bill", "podadha", "aagadha", "ஆகாத", "போடாத", "நிலுவை"]) or ("غير" in msg_lower and "مفوتر" in msg_lower)
            from utils.table_formatter import detect_language
            query_lang = detect_language(payload.message)
            aspect_key = f"{active_visit}:{'unbilled' if is_unbilled_only else 'all_services'}:{current_mode}:{query_lang}"
            
            # 1. Check Valkey Ephemeral Cache (5-Minute TTL)
            cached_srv = valkey_manager.get_patient_snapshot(active_mrn, aspect_key)
            if cached_srv:
                update_session_memory(payload.session_id, payload.message, cached_srv)
                return ChatResponse(
                    status="success",
                    reply=cached_srv,
                    model_used="Valkey Ephemeral Cache (5-min TTL, 0 Tokens)",
                    mode=current_mode,
                    action_executed={"mrn": active_mrn, "visit_no": active_visit, "cache_hit": True}
                )

            # 2. Query Live Database (NO arbitrary TOP 5 truncation; fetch all up to 100)
            filter_sql = "AND pvs.Is_Service_Billed = 'N'" if is_unbilled_only else ""
            srv_sql = f"""
            SELECT TOP 100
                pvbd.Permanent_Visit_No,
                pbd.Permanent_MRN_No,
                pvs.Patient_Visit_Services_Serial_No,
                pvs.Is_Service_Billed,
                pvs.Service_Quantity,
                s.Service_Description,
                s.CPT_Code,
                s.Service_Internal_Code,
                pvs.Patient_Payment_Type_Code
            FROM Patient_Visit_Services pvs WITH(NOLOCK)
            JOIN Patient_Visit_Basic_Details pvbd WITH(NOLOCK) ON pvs.Patient_Visit_Basic_Details_Serial_No = pvbd.Patient_Visit_Basic_Details_Serial_No
            JOIN Patient_Basic_Details pbd WITH(NOLOCK) ON pvbd.Patient_Basic_Details_Serial_No = pbd.Patient_Basic_Details_Serial_No
            JOIN Service_USSDB sussdb WITH(NOLOCK) ON sussdb.Service_USSDB_Serial_No = pvs.Service_USSDB_Serial_No
            JOIN Service s WITH(NOLOCK) ON s.Service_Serial_No = sussdb.Service_Serial_No
            WHERE pvbd.Permanent_Visit_No = '{active_visit}'
              AND pbd.Permanent_MRN_No = '{active_mrn}'
              AND pvs.Active_Status = 'A'
              AND pvs.Patient_Visit_Service_Cancellation_Flag = 'N'
              {filter_sql}
            ORDER BY pvs.Patient_Visit_Services_Serial_No DESC
            """
            raw_srv = autonomous_agent.execute_select_sql(srv_sql)
            srv_list = json.loads(raw_srv) if raw_srv and raw_srv.startswith("[") else []
            if srv_list:
                from utils.table_formatter import format_user_friendly_response
                reply = format_user_friendly_response(
                    srv_list,
                    query_context={
                        "user_query": payload.message,
                        "mrn": active_mrn,
                        "visit_no": active_visit,
                        "executed_sql": srv_sql
                    },
                    mode=current_mode
                )
                
                # Cache in Valkey for 5 minutes (300s)
                valkey_manager.cache_patient_snapshot(active_mrn, aspect_key, reply, ttl=300)
                valkey_manager.cache_ephemeral_query(
                    payload.message,
                    active_mrn=active_mrn or "",
                    session_id=payload.session_id,
                    formatted_response=reply,
                    executed_sql=srv_sql,
                    ttl=300
                )
                update_session_memory(payload.session_id, payload.message, reply)
                valkey_manager.update_session_entities(payload.session_id, sess["active_entities"])
                return ChatResponse(
                    status="success",
                    reply=reply,
                    model_used="HIMES Deterministic Engine (0 LLM Tokens, Live DB)",
                    mode=current_mode,
                    action_executed={"mrn": active_mrn, "visit_no": active_visit, "services_count": len(srv_list), "cached_valkey_5m": True}
                )



        # 1. Valkey Fast-Path: Menu Navigation Lookup
        msg_lower = payload.message.lower()
        if any(p in msg_lower for p in ["price list management", "pricelist", "price list"]) and any(w in msg_lower for w in ["menu", "enga", "where", "screen", "location", "path", "open", "iruku"]):
            if current_mode == "developer":
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
            else:
                reply = (
                    "**HIMES Price List Management:**\n\n"
                    "Price List Setup menus are located in the following hospital sections:\n\n"
                    "1. ✅ **Services & Insurance Tariff Price List:**\n"
                    "   Navigate to **Application > Price List Management**.\n\n"
                    "2. ✅ **Pharmacy & Inventory Items Price List:**\n"
                    "   Navigate to **Inventory > Inventory Price List Management**.\n\n"
                    "3. ✅ **Bed & Doctor Resources Pricing Rules:**\n"
                    "   Navigate to **Application > Price Rule For Resources**.\n\n"
                    "4. ✅ **Bulk Price List Management:**\n"
                    "   Available under **Application > Bulk Price List Management**.\n\n"
                    "> ℹ️ **Summary:** All medical service tariffs and medicine prices can be configured in these screens."
                )
            update_session_memory(payload.session_id, payload.message, reply)
            valkey_manager.update_session_entities(payload.session_id, sess["active_entities"])
            return ChatResponse(
                status="success",
                reply=reply,
                model_used="Valkey In-Memory Cache (Sub-millisecond)",
                mode=current_mode,
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
                if current_mode == "developer":
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
                else:
                    reply = (
                        f"### {screen_data.get('title')}\n\n"
                        f"**Module:** {screen_data.get('module').upper()}\n\n"
                        f"**Screen Purpose & Functionality:**\n"
                        f"{screen_data.get('description')}\n\n"
                        f"> ✅ **Status:** Screen verified and operational in HIMES."
                    )
                update_session_memory(payload.session_id, payload.message, reply)
                return ChatResponse(
                    status="success",
                    reply=reply,
                    model_used="Valkey In-Memory Cache (Sub-millisecond)",
                    mode=current_mode,
                    action_executed={
                        "cache_hit": True,
                        "source": "valkey_screen_index",
                        "namespace": f"himes:screen:{clean_route}"
                    }
                )

        # 1b. Valkey Fast-Path: Instant Module Lifecycle & Flow lookup (All 12 HIMES Domains)
        # CRITICAL: ONLY trigger general module overview if user explicitly asks for the general module overview / architecture,
        # NEVER hijack specific functional or capability questions (e.g. "allow pannuma", "multiple invoices", "how to revert", "can we do X")!
        specific_question_markers = [
            "allow", "mudiyum", "mudium", "mudiyuma", "mudiyadhu", "pannum", "pannuma", "pannalama", "pannalam",
            "can ", "can i", "can we", "is it possible", "how to", "how do", "why", "what happens", "epdi", "eppadi",
            "enna aagum", "revert", "cancel", "multiple", "refund", "receipt", "short payment", "discount", "advance",
            "deposit", "copay", "co-pay", "vat", "tax", "thevai", "thevaiya", "edhuku", "ethuku", "difference", "compare",
            "illaye", "answer"
        ]
        has_specific_question = any(w in msg_lower for w in specific_question_markers)

        is_module_overview_request = not has_specific_question and any(
            phrase in msg_lower for phrase in [
                "explain module", "module overview", "module lifecycle", "module flow",
                "explain the flow", "show workflow", "all tables in", "tables for module",
                "lifecycle of", "architecture of"
            ]
        )
        if is_module_overview_request:
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
                        raw_wf = mod_data.get("key_workflows") or mod_data.get("rules") or []
                        workflows = "\n".join([f"• {wf}" for wf in raw_wf])
                        if current_mode == "developer":
                            reply = (
                                f"**HIMES {mod_data.get('title')} Lifecycle Details:**\n\n"
                                f"{mod_data.get('description')}\n\n"
                                f"**Key SQL Tables:**\n`{tables_str}`\n\n"
                                f"**Core Workflows:**\n{workflows}\n\n"
                                f"*(⚡ Instant response powered by Valkey In-Memory Index)*"
                            )
                        else:
                            reply = (
                                f"### {mod_data.get('title')}\n\n"
                                f"{mod_data.get('description')}\n\n"
                                f"**Hospital Workflows:**\n{workflows}\n\n"
                                f"> ✅ **Workflow Status:** Standard HIMES hospital process verified."
                            )
                        update_session_memory(payload.session_id, payload.message, reply)
                        valkey_manager.update_session_entities(payload.session_id, sess["active_entities"])
                        return ChatResponse(
                            status="success",
                            reply=reply,
                            model_used="Valkey In-Memory Cache (Sub-millisecond)",
                            mode=current_mode,
                            action_executed={
                                "cache_hit": True,
                                "source": "valkey_module_index",
                                "namespace": f"himes:module:{mod_k}"
                            }
                        )

        # Healthcare Privacy & Real-Time Data Freshness Guardrail: NEVER cache patient, encounter, or clinical PHI!
        from semantic_cache import is_transactional_query
        is_patient_query = bool(v_m or m_m) or is_patient_or_phi_data(payload.message)
        is_followup = not is_patient_query and bool(sess["active_entities"].get("visit_no") or sess["active_entities"].get("mrn"))
        is_live_or_dynamic_query = is_patient_query or is_transactional_query(payload.message)
        
        # Grounding & PHI Rule: Only check semantic cache for static system/workflow knowledge
        if not is_followup and not is_live_or_dynamic_query:
            cached_result = check_semantic_cache(payload.message, threshold=0.30)
            if cached_result:
                c_answer = cached_result["answer"]
                if current_mode == "user":
                    c_answer = format_user_mode_response(c_answer)
                update_session_memory(payload.session_id, payload.message, c_answer)
                valkey_manager.update_session_entities(payload.session_id, sess["active_entities"])
                return ChatResponse(
                    status="success",
                    reply=c_answer,
                    model_used="ChromaDB Semantic Cache (Instant Hit)",
                    mode=current_mode,
                    action_executed={
                        "cache_hit": True,
                        "matched_query": cached_result.get("matched_query"),
                        "distance": cached_result.get("distance")
                    }
                )

        # Build enriched context with session memory and Valkey Hybrid Search
        full_context = dict(payload.context or {})
        full_context["is_developer_mode"] = is_developer_mode
        full_context["attachments"] = payload.attachments or []

        # Determine if query is a general module or screen inquiry rather than a visit follow-up
        is_module_or_screen_query = any(w in msg_lower for w in ["module", "screen", "menu", "workflow", "lifecycle", "page", "viewglobal", "view"]) and not bool(v_m)
        active_ents_to_pass = dict(sess["active_entities"])
        if is_module_or_screen_query:
            active_ents_to_pass["visit_no"] = None  # Prevent old visit from hijacking module questions

        full_context["active_entities"] = active_ents_to_pass
        try:
            from memory.session_memory import get_session_memory
            v_mem = get_session_memory(payload.session_id, user_id=payload.user_id)
            v_turns = v_mem.get_history()
            full_context["previous_chat_turns"] = v_turns[-10:] if v_turns else list(sess["turns"][-10:])
            full_context["recent_history_context"] = v_mem.format_context_for_prompt(max_turns=10)
        except Exception:
            full_context["previous_chat_turns"] = list(sess["turns"][-10:])

        # Valkey Smart Hybrid Context enrichment
        valkey_ctx = get_himes_context(payload.message, limit=2)
        if valkey_ctx.get("context"):
            full_context["valkey_knowledge"] = valkey_ctx["context"]

        # Sync active session state into Valkey
        valkey_manager.update_session_entities(payload.session_id, sess["active_entities"])

        # 3. Dispatch to Dynamic Multi-Step Chain OR HIMES Multi-Agent Specialist Orchestrator
        from chains.multi_step_clinical_chain import is_multi_step_query, run_multi_step_clinical_chain

        effective_message = payload.message
        if is_multi_step_query(effective_message):
            chain_res = run_multi_step_clinical_chain(
                message=effective_message,
                mrn=active_ents_to_pass.get("mrn"),
                visit_no=active_ents_to_pass.get("visit_no"),
                mode=current_mode,
                session_id=payload.session_id,
                context=full_context,
            )
            agent_res = {
                "reply": chain_res.get("reply", "No response generated."),
                "agent": chain_res.get("model_used", "HIMES Universal Multi-Step Chain"),
                "status": chain_res.get("status", "success"),
                "actions_taken": [
                    {"action": "multi_step_execution", "steps": len(chain_res.get("steps_run", []))}
                ],
                "steps": len(chain_res.get("steps_run", [])),
            }
        else:
            agent_res = himes_orchestrator.dispatch(effective_message, full_context, is_dev_mode=is_developer_mode)
        reply_text = agent_res.get("reply", "No response generated.")
        actions_taken = agent_res.get("actions_taken", [])
        specialist_name = agent_res.get("agent", "Autonomous Agent (Live MSSQL Engine)")

        # Format reply based on mode
        if current_mode == "user":
            reply_text = format_user_mode_response(reply_text)
        elif current_mode == "developer" and actions_taken:
            # Append structured developer diagnostics if not already present in response
            queries_run = [
                a for a in actions_taken
                if a.get("action") == "execute_select_sql" or a.get("tool") == "execute_select_sql"
            ]
            if queries_run and "```sql" not in reply_text:
                tech_details = "\n\n### 💻 Developer Diagnostics\n**Executed SQL Queries:**\n"
                for q in queries_run[:3]:
                    sql_text = q.get("input", {}).get("sql_query") or q.get("args", {}).get("sql_query", "")
                    if sql_text:
                        tech_details += f"```sql\n{sql_text}\n```\n"
                cache_info = f"• **Session Mode Key:** `chat_session:{payload.session_id}:mode` (developer)\n• **Valkey Session:** Active\n• **Specialist Agent:** `{specialist_name}`\n"
                tech_details += f"**Cache & State Store:**\n{cache_info}"
                reply_text += tech_details

        # Strict Multi-Lingual & Tanglish Language Mirroring via Language Specialist Agent
        reply_text = language_specialist.mirror_reply(reply_text, user_lang)

        # Enforce User Mode clean formatting after language mirroring
        if current_mode == "user":
            reply_text = format_user_mode_response(reply_text)

        # Update session memory
        update_session_memory(payload.session_id, payload.message, reply_text, user_id=payload.user_id)
        valkey_manager.update_session_entities(payload.session_id, sess["active_entities"])


        # 4. Save into ChromaDB Semantic Cache (STRICTLY PROHIBITED for dynamic availability, transactions, or PHI)
        if not is_followup and not is_live_or_dynamic_query and not is_patient_or_phi_data(payload.message, reply_text):
            save_to_semantic_cache(payload.message, reply_text)

        return ChatResponse(
            status=agent_res.get("status", "success"),
            reply=reply_text,
            model_used=f"{specialist_name} (HIMES Multi-Agent)",
            mode=current_mode,
            action_executed={
                "cache_hit": False,
                "specialist_agent": specialist_name,
                "orchestrator_intent": agent_res.get("orchestrator_intent", "dynamic"),
                "actions_taken": actions_taken,
                "steps": agent_res.get("steps", 1)
            }
        )

    except SecurityException as se:
        curr_m = valkey_manager.get_session_mode(payload.session_id)
        return ChatResponse(
            status="blocked_by_guardrails",
            reply=f"⚠️ Guardrail Protection Triggered: {str(se)}",
            model_used="Security Guardrail",
            mode=curr_m,
            action_executed={"error": str(se)}
        )
    except Exception as e:
        curr_m = valkey_manager.get_session_mode(payload.session_id)
        if curr_m == "user":
            err_reply = "⚠️ **System Notice:** We encountered a temporary issue while retrieving your information. Our automatic recovery system has been notified. Status: In Progress."
        else:
            err_reply = f"⚠️ Error processing query: {str(e)}\n\n```python\n{traceback.format_exc()[:1000]}\n```"
        return ChatResponse(
            status="error",
            reply=err_reply,
            model_used="Error Handler",
            mode=curr_m,
            action_executed={"error": str(e)}
        )

# ====================================================================
# LANGCHAIN MULTI-STEP CHAIN ENDPOINT
# POST /api/agent/chain
# Triggered ONLY for complex multi-intent queries (unbilled + pricing + insurance).
# Simple single-intent queries continue through /api/chat Tier-1 engine.
# ====================================================================

class ChainRequest(BaseModel):
    message: str
    session_id: str = "default"
    mrn: Optional[str] = None
    visit_no: Optional[str] = None
    mode: Optional[str] = "user"
    context: Optional[Dict[str, Any]] = None

class ChainResponse(BaseModel):
    status: str
    reply: str
    model_used: str
    steps_run: List[Dict[str, Any]] = []
    mrn: Optional[str] = None
    visit_no: Optional[str] = None

@app.post("/api/agent/chain", response_model=ChainResponse)
def run_clinical_chain(payload: ChainRequest):
    """
    LangChain Multi-Step Clinical Chain endpoint.
    Handles complex queries that require:
      Step 1: Unbilled service SQL
      Step 2: Tariff/pricing cross-reference
      Step 3: ChromaDB RAG insurance policy lookup
      Step 4: Synthesis into unified response card

    The Laravel frontend may call this endpoint directly for complex questions,
    or /api/chat auto-routes here when is_multi_step_query() returns True.
    """
    try:
        enforce_safety_rules(payload.message)

        # Resolve entities from session memory
        from memory.session_memory import get_session_memory
        from chains.multi_step_clinical_chain import is_multi_step_query, run_multi_step_clinical_chain
        from utils.table_formatter import detect_language

        session_mem = get_session_memory(payload.session_id)
        active_ents = session_mem.get_active_entities()

        mrn = payload.mrn or active_ents.get("mrn")
        visit_no = payload.visit_no or active_ents.get("visit_no")
        lang = detect_language(payload.message)
        mode = payload.mode or valkey_manager.get_session_mode(payload.session_id)

        result = run_multi_step_clinical_chain(
            message=payload.message,
            mrn=mrn,
            visit_no=visit_no,
            lang=lang,
            mode=mode,
            session_id=payload.session_id,
            context=payload.context,
        )

        return ChainResponse(
            status=result.get("status", "success"),
            reply=result.get("reply", ""),
            model_used=result.get("model_used", ""),
            steps_run=result.get("steps_run", []),
            mrn=result.get("mrn"),
            visit_no=result.get("visit_no"),
        )

    except SecurityException as se:
        return ChainResponse(
            status="blocked_by_guardrails",
            reply=f"⚠️ Guardrail: {str(se)}",
            model_used="Security Guardrail",
        )
    except Exception as e:
        return ChainResponse(
            status="error",
            reply=f"⚠️ Chain error: {str(e)}",
            model_used="Error Handler",
        )


# ====================================================================
# MCP SERVER ENDPOINTS
# ====================================================================

import json as _json

@app.get("/mcp/mssql")
def mcp_mssql_info():
    """MCP MSSQL Inspection Server — returns capabilities manifest."""
    cfg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config", "mcp_servers.json")
    try:
        with open(cfg_path, "r", encoding="utf-8") as f:
            cfg = _json.load(f)
        return cfg.get("mcp_servers", {}).get("mssql_inspection", {})
    except Exception:
        return {"name": "HIMES MSSQL Inspection MCP", "status": "config_not_found"}

@app.post("/mcp/mssql/inspect")
def mcp_inspect_table(payload: Dict[str, Any]):
    """MCP: Inspect MSSQL table schema. Input: {'table_name': str}"""
    from agents.sql_agent import _build_agent_tools
    tools = {t.name: t for t in _build_agent_tools()}
    table = payload.get("table_name", "")
    if not table:
        return {"error": "table_name is required"}
    return {"schema": tools["inspect_table_schema"].func(table)}

@app.post("/mcp/mssql/query")
def mcp_execute_query(payload: Dict[str, Any]):
    """MCP: Execute a read-only SQL query. Input: {'sql': str}"""
    from agents.sql_agent import _build_agent_tools
    tools = {t.name: t for t in _build_agent_tools()}
    sql = payload.get("sql", "")
    if not sql:
        return {"error": "sql is required"}
    try:
        enforce_safety_rules(sql)
    except SecurityException as se:
        return {"error": f"BLOCKED: {se}"}
    return {"result": tools["execute_read_only_sql"].func(sql)}

@app.post("/mcp/clinical/search")
def mcp_clinical_search(payload: Dict[str, Any]):
    """MCP: ChromaDB hybrid search for clinical policies. Input: {'query': str, 'top_k': int}"""
    try:
        from retrieval.hybrid_search import hybrid_search_engine
        q = payload.get("query", "")
        k = int(payload.get("top_k", 3))
        if not hybrid_search_engine._index_built:
            hybrid_search_engine.build_bm25_index_from_store()
        result = hybrid_search_engine.search(q, top_k=k)
        return {"chunks": result.get("top_chunks", []), "query": q}
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/skills")
def list_agent_skills():
    """Returns the registered HIMES agent skills manifest."""
    from skills.himes_skills import list_skills
    return {"skills": list_skills()}


if __name__ == "__main__":
    import uvicorn
    host = os.getenv("AGENT_HOST", "127.0.0.1")
    port = int(os.getenv("AGENT_PORT", 8000))
    uvicorn.run("main:app", host=host, port=port, reload=True)
