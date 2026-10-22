"""
chains/multi_step_clinical_chain.py
=====================================
Universal Dynamic Multi-Step Clinical & Hospital Operations Agent for HIMES.

ARCHITECTURAL PRINCIPLE:
- ZERO hardcoded Q&A or query templates.
- NEVER assume the user is only asking about billing or unbilled services.
- Hospital users (doctors, nurses, cashiers, administrators) can ask ANYTHING
  in ANY language (Tamil, Tanglish, English, Arabic, Hindi, etc.):
    * Appointments & Doctor OPD schedules
    * Inpatient (IP) / ICU Bed occupancy & ward status
    * Pharmacy stock & drug dispensing records
    * Laboratory (LIS) test orders, results, and critical panic values
    * Billing, deposits, receipts, and invoices
    * Insurance pre-authorizations, DHA/Shafafiya coverage policies
    * Patient visit histories and clinical notes
- Operates just like Antigravity IDE:
  1. Dynamically analyzes the user's intent.
  2. Discovers relevant tables or schema via search_db_tables & inspect_table_schema.
  3. Formulates and executes live SELECT-only queries via execute_read_only_sql.
  4. Cross-references secondary sources (tariffs, policies, master tables) dynamically.
  5. Synthesizes a verified factual answer in the requested language and mode (User View vs. Developer View).
"""

import json
import os
import re
import sys
import time
from typing import Any, Dict, List, Optional

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


# ── Dynamic Tool Implementations ──────────────────────────────────────────────

def _tool_search_db_tables(keyword: str) -> str:
    """Discovers table names matching a keyword across the 2,550+ MSSQL database tables."""
    from autonomous_agent import autonomous_agent
    clean_kw = re.sub(r'[^A-Za-z0-9_]', '', str(keyword or '').strip())
    if not clean_kw:
        return "Error: search keyword must be alphanumeric."
    sql = f"""
        SELECT TOP 25 TABLE_NAME
        FROM INFORMATION_SCHEMA.TABLES WITH(NOLOCK)
        WHERE TABLE_NAME LIKE '%{clean_kw}%'
        ORDER BY TABLE_NAME
    """
    raw = autonomous_agent.execute_select_sql(sql.strip())
    rows = json.loads(raw) if raw and raw.startswith("[") else []
    if not rows:
        return f"No tables found matching '{clean_kw}'."
    return "Matching tables: " + ", ".join([r.get("TABLE_NAME", "") for r in rows])


def _tool_inspect_table_schema(table_name: str) -> str:
    """Inspects column names, data types, and nullability for any MSSQL table."""
    from autonomous_agent import autonomous_agent
    from guardrails import validate_sql_query, SecurityException

    clean = re.sub(r'[^A-Za-z0-9_]', '', str(table_name or '').strip())
    if not clean:
        return "Error: table_name must be alphanumeric."
    schema_sql = f"""
        SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, IS_NULLABLE
        FROM INFORMATION_SCHEMA.COLUMNS WITH(NOLOCK)
        WHERE TABLE_NAME = '{clean}'
        ORDER BY ORDINAL_POSITION
    """
    raw = autonomous_agent.execute_select_sql(schema_sql.strip())
    cols = json.loads(raw) if raw and raw.startswith("[") else []
    if not cols:
        return f"Table '{clean}' not found or has no columns."
    lines = [f"Table: {clean}"]
    for c in cols[:40]:
        col = c.get("COLUMN_NAME", "")
        dtype = c.get("DATA_TYPE", "")
        maxlen = c.get("CHARACTER_MAXIMUM_LENGTH")
        lines.append(f"  - {col}: {dtype}" + (f"({maxlen})" if maxlen else ""))
    return "\n".join(lines)


def _tool_execute_read_only_sql(sql_query: str) -> str:
    """
    Executes a SELECT query on MSSQL via live database connection.
    Enforces SELECT-only guardrails, auto-injects WITH(NOLOCK) and TOP 100 limit.
    """
    from autonomous_agent import autonomous_agent
    from guardrails import validate_sql_query, SecurityException

    query = str(sql_query or '').strip()
    if not query:
        return "Error: SQL query is empty."

    try:
        validate_sql_query(query)
    except SecurityException as e:
        return f"SECURITY BLOCKED: {e}"

    # Auto-inject WITH(NOLOCK)
    if "WITH(NOLOCK)" not in query.upper():
        query = re.sub(
            r'\bFROM\s+(\w+)\b(?!\s+WITH)',
            r'FROM \1 WITH(NOLOCK)',
            query, flags=re.IGNORECASE
        )
        query = re.sub(
            r'\bJOIN\s+(\w+)\b(?!\s+WITH)',
            r'JOIN \1 WITH(NOLOCK)',
            query, flags=re.IGNORECASE
        )

    # Auto-inject TOP 100 limit if missing
    if "TOP " not in query.upper() and query.upper().startswith("SELECT"):
        query = re.sub(r'^SELECT\s+', 'SELECT TOP 100 ', query, flags=re.IGNORECASE)

    raw = autonomous_agent.execute_select_sql(query)
    return raw


def _tool_search_codebase(query: str, subpath: str = "") -> str:
    """Searches Laravel controllers, models, and routes in /L9/nagul/himes-ai to inspect business logic."""
    from autonomous_agent import autonomous_agent
    return autonomous_agent.search_code(query, subpath=subpath)


def _tool_query_clinical_knowledge(query: str) -> str:
    """Hybrid search ChromaDB for DHA/Shafafiya insurance rules, clinical SOPs, and hospital guidelines."""
    try:
        from retrieval.hybrid_search import hybrid_search_engine
        if not hybrid_search_engine._index_built:
            hybrid_search_engine.build_bm25_index_from_store()
        res = hybrid_search_engine.search(query, top_k=3)
        chunks = res.get("top_chunks", [])
        if not chunks:
            return "No matching clinical or policy documentation found."
        formatted = []
        for c in chunks:
            title = c.get("metadata", {}).get("title", "Clinical Policy")
            text = c.get("text", "")[:350]
            formatted.append(f"[{title}]: {text}")
        return "\n\n".join(formatted)
    except Exception as e:
        return f"Knowledge retrieval notice: {str(e)}"


# ── Dynamic Tool Dispatcher ───────────────────────────────────────────────────

_DYNAMIC_TOOLS = {
    "search_db_tables": _tool_search_db_tables,
    "inspect_table_schema": _tool_inspect_table_schema,
    "execute_read_only_sql": _tool_execute_read_only_sql,
    "search_codebase": _tool_search_codebase,
    "query_clinical_knowledge": _tool_query_clinical_knowledge,
}


def _execute_tool_call(tool_name: str, tool_args: Any) -> str:
    """Executes a named tool with provided arguments safely."""
    fn = _DYNAMIC_TOOLS.get(tool_name.strip())
    if not fn:
        return f"Error: Tool '{tool_name}' does not exist. Available: {list(_DYNAMIC_TOOLS.keys())}"

    try:
        if isinstance(tool_args, dict):
            # Pick first value or keyword arg
            first_val = next(iter(tool_args.values())) if tool_args else ""
            return fn(first_val)
        elif isinstance(tool_args, str):
            return fn(tool_args)
        else:
            return fn(str(tool_args))
    except Exception as e:
        return f"Error executing tool '{tool_name}': {str(e)}"


# ── Dynamic Multi-Step ReAct Loop ─────────────────────────────────────────────

def run_multi_step_clinical_chain(
    message: str,
    mrn: Optional[str] = None,
    visit_no: Optional[str] = None,
    lang: str = "en",
    mode: str = "user",
    session_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
    max_steps: int = 5,
) -> Dict[str, Any]:
    """
    Universal Dynamic Multi-Step Hospital Agent Chain.
    Can resolve ANY hospital query across 2,550+ MSSQL tables and codebase dynamically.

    Does NOT rely on fixed templates or hardcoded sample question patterns.
    """
    from autonomous_agent import autonomous_agent
    from utils.table_formatter import detect_language

    start_time = time.time()
    msg_raw = message.strip()

    system_prompt = f"""
You are the HIMES Universal Multi-Step Hospital AI Agent.
You have real-time dynamic access to the live MSSQL Database (2,550+ tables) and Laravel Codebase (/L9/nagul/himes-ai).

CRITICAL OPERATIONAL RULES:
1. Understand the CORE CONCEPT of the user's inquiry regardless of colloquial phrasing, slang, or grammar.
2. NEVER hallucinate facts, numbers, patient records, or table names.
3. DO NOT assume the user's question is limited to an example. The user can ask about ANY hospital topic:
   - Appointments, doctor schedules, OPD queue
   - Patient demographics, visit history, emergency triage
   - Inpatient (IP) / ICU beds, ward occupancy
   - Prescriptions, pharmacy formulary, stock dispensing
   - Lab orders, test results, panic / critical thresholds
   - Billing, unbilled items, tariffs, deposits, receipts, invoices
   - Insurance policies, pre-authorizations, DHA/Shafafiya rules
4. ALWAYS check the live database or codebase dynamically using the available tools before answering.
5. ONLY execute read-only SELECT queries with WITH(NOLOCK) and TOP 100.
6. STRICT DYNAMIC LANGUAGE MIRRORING:
   - Automatically detect the user query's language and dialect:
     • Pure Tamil script (தமிழ் எழுத்துகளில்) -> Answer purely in Tamil script (தமிழ்).
     • Tanglish (Tamil words written in English alphabet) -> Answer in natural, friendly Tanglish.
     • English -> Answer in clear, professional English.
     • Other language -> Answer in that language.
   - NEVER switch languages away from what the user used.
7. NEVER mention 'User Mode' or 'Developer Mode' in your Final Answer. Simply give the direct, factual hospital response!

AVAILABLE TOOLS:
1. `search_db_tables`: Search table names matching a keyword (e.g. 'appointment', 'bed', 'tariff', 'pharmacy', 'doctor').
   Input: keyword (string)
2. `inspect_table_schema`: Inspect column names and types for any table.
   Input: table_name (string)
3. `execute_read_only_sql`: Run a SELECT query on MSSQL.
   Input: sql_query (string)
4. `search_codebase`: Grep Laravel code to check route, controller, or table join logic.
   Input: query (string)
5. `query_clinical_knowledge`: Search ChromaDB for clinical policies / DHA guidelines.
   Input: query (string)

REACT FORMAT:
In each step, output:
Thought: <what information is needed next>
Action: <tool_name>
Action Input: <input string for tool>

When you have retrieved sufficient verified live data to answer the user's question, output:
Final Answer: <Your clear, verified answer following the language style above, stating facts and numbers directly>
"""

    react_history = f"""User Request: {message}\n{active_entities_str}\n"""

    final_reply = ""
    executed_sql_queries: List[str] = []

    for step_num in range(1, max_steps + 1):
        prompt = (
            f"{react_history}\n"
            f"Step {step_num} of {max_steps}:\n"
            f"Decide your next Thought and Action, or output Final Answer if you have verified data."
        )

        llm_output = autonomous_agent.call_llm(prompt=prompt, system_prompt=system_prompt)
        if not llm_output or not llm_output.strip():
            break

        # Check for Final Answer
        if "Final Answer:" in llm_output:
            final_reply = llm_output.split("Final Answer:", 1)[-1].strip()
            steps_run.append({
                "step": step_num,
                "action": "final_answer",
                "output_summary": "Final answer reached.",
            })
            break

        # Parse Thought and Action
        action_match = re.search(r"Action:\s*([a-zA-Z0-9_]+)", llm_output)
        input_match = re.search(r"Action Input:\s*([^\n\r]+(?:(?:\n[^\n\r]+)*))", llm_output)

        if not action_match:
            # If no clear action format, treat whatever output as the answer
            final_reply = llm_output.strip()
            steps_run.append({
                "step": step_num,
                "action": "direct_llm_response",
                "output_summary": "Generated direct synthesis.",
            })
            break

        tool_name = action_match.group(1).strip()
        tool_input = input_match.group(1).strip() if input_match else ""

        # Clean tool input (remove quotes or backticks if wrapped)
        tool_input = re.sub(r"^[`'\"]+|[`'\"]+$", "", tool_input).strip()

        # Track executed SQL
        if tool_name == "execute_read_only_sql":
            executed_sql_queries.append(tool_input)

        # Execute the tool
        obs = _execute_tool_call(tool_name, tool_input)

        # Truncate large observations to avoid context blowout
        obs_summary = obs[:2000] if len(obs) > 2000 else obs

        steps_run.append({
            "step": step_num,
            "action": tool_name,
            "input": tool_input[:200],
            "observation_preview": obs[:300],
        })

        react_history += f"\nThought: Step {step_num} complete.\nAction: {tool_name}\nAction Input: {tool_input}\nObservation: {obs_summary}\n"

    # If loop ended without explicit Final Answer, synthesize with LLM
    if not final_reply:
        synth_prompt = (
            f"Based on the live data retrieved during this multi-step investigation:\n\n"
            f"{react_history}\n\n"
            f"Provide the final clear, verified response to the user. "
            f"STRICTLY mirror the user's input language and dialect (Pure Tamil script, Tanglish, or English). "
            f"State live facts and numbers directly. Mode: {mode}."
        )
        final_reply = autonomous_agent.call_llm(prompt=synth_prompt, system_prompt=system_prompt)

    # Format reply according to mode (User View vs Developer View)
    if mode == "developer" and executed_sql_queries:
        sql_traces = "\n\n### 💻 Developer Diagnostics (Multi-Step Chain)\n**Executed Live SQL Queries:**\n"
        for q in executed_sql_queries:
            sql_traces += f"```sql\n{q}\n```\n"
        steps_summary = f"• **Steps Executed:** {len(steps_run)}\n• **Execution Time:** {round(time.time() - start_time, 2)}s\n"
        final_reply += sql_traces + steps_summary

    # Save turn to session memory if session_id provided
    if session_id:
        try:
            from memory.session_memory import get_session_memory
            get_session_memory(session_id).add_turn(message, final_reply)
        except Exception:
            pass

    return {
        "reply": final_reply,
        "steps_run": steps_run,
        "model_used": "HIMES Universal Multi-Step Clinical & Operations Chain",
        "mrn": mrn or "",
        "visit_no": visit_no or "",
        "status": "success",
        "sql_queries": executed_sql_queries,
        "execution_time_sec": round(time.time() - start_time, 3),
    }


def is_multi_step_query(message: str) -> bool:
    """
    Evaluates whether a query requires multi-step investigation
    (e.g., cross-referencing multiple tables, cross-departmental operations, or comparative analytics).
    """
    msg = message.lower()
    has_multiple_questions = "?" in msg and msg.count("?") > 1
    has_multi_domain = any(k in msg for k in [
        "breakdown", "comparison", "cross-reference", "reconcile",
        "records breakdown", "both clinic and", "compare", "overall metrics"
    ])
    return has_multiple_questions or has_multi_domain


__all__ = [
    "run_multi_step_clinical_chain",
    "is_multi_step_query",
    "_tool_search_db_tables",
    "_tool_inspect_table_schema",
    "_tool_execute_read_only_sql",
    "_tool_search_codebase",
    "_tool_query_clinical_knowledge",
]
