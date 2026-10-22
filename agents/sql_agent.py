"""
agents/sql_agent.py
====================
Dynamic LangChain SQL Agent for HIMES — navigates 2,550+ MSSQL tables.

Used ONLY when the deterministic engine (main.py Tier-1) cannot resolve the intent
with its known patterns. The SQL agent uses LangChain Tool + ReAct loop to:
  1. Inspect table schemas dynamically.
  2. Validate foreign-key relationships.
  3. Build and execute a valid SELECT query.

Guardrails:
  - 100% SELECT-only — validate_sql_query() from guardrails.py enforced on every query.
  - WITH(NOLOCK) injected automatically if missing.
  - Result capped at TOP 100 rows.
  - Agent loop capped at 6 reasoning steps to prevent runaway token usage.
"""

import json
import re
import sys
from typing import Any, Dict, Optional

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Maximum ReAct reasoning steps before forcing a direct answer
MAX_AGENT_STEPS = 6


# ── LangChain Tool definitions ────────────────────────────────────────────────

def _build_agent_tools():
    """
    Builds LangChain Tool list wrapping existing autonomous_agent methods.
    Imported lazily to avoid circular imports at module load time.
    """
    from langchain.tools import Tool
    from autonomous_agent import autonomous_agent
    from guardrails import validate_sql_query, SecurityException

    def inspect_table_schema(table_name: str) -> str:
        """
        Returns column names and types for a given MSSQL table.
        Uses existing autonomous_agent.execute_select_sql() — no new connection.
        """
        clean = re.sub(r'[^A-Za-z0-9_]', '', table_name.strip())
        if not clean:
            return "Error: table_name must be alphanumeric."
        sql = f"""SELECT TOP 1 * FROM {clean} WITH(NOLOCK)"""
        try:
            validate_sql_query(sql)
        except SecurityException as e:
            return f"BLOCKED: {e}"
        schema_sql = f"""
            SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = '{clean}'
            ORDER BY ORDINAL_POSITION
        """
        raw = autonomous_agent.execute_select_sql(schema_sql.strip())
        cols = json.loads(raw) if raw and raw.startswith("[") else []
        if not cols:
            return f"Table '{clean}' not found or has no columns."
        lines = [f"Table: {clean}"]
        for c in cols:
            col = c.get("COLUMN_NAME", "")
            dtype = c.get("DATA_TYPE", "")
            maxlen = c.get("CHARACTER_MAXIMUM_LENGTH")
            lines.append(f"  - {col}: {dtype}" + (f"({maxlen})" if maxlen else ""))
        return "\n".join(lines)

    def execute_read_only_sql(query: str) -> str:
        """
        Executes a SELECT query on MSSQL via existing autonomous_agent pipeline.
        Automatically injects WITH(NOLOCK) and TOP 100 if missing.
        """
        query = query.strip()
        try:
            validate_sql_query(query)
        except SecurityException as e:
            return f"SECURITY BLOCKED: {e}"

        # Auto-inject WITH(NOLOCK) on tables that are missing it
        if "WITH(NOLOCK)" not in query.upper():
            query = re.sub(
                r'\bFROM\s+(\w+)\b(?!\s+WITH)',
                r'FROM \1 WITH(NOLOCK)',
                query, flags=re.IGNORECASE
            )

        # Auto-inject TOP 100 if SELECT * or no TOP clause
        if "TOP " not in query.upper() and query.upper().startswith("SELECT"):
            query = re.sub(r'^SELECT\s+', 'SELECT TOP 100 ', query, flags=re.IGNORECASE)

        return autonomous_agent.execute_select_sql(query)

    def validate_foreign_keys(source_table: str, target_table: str) -> str:
        """
        Checks if a foreign-key relationship exists between two MSSQL tables.
        Returns join column suggestions from INFORMATION_SCHEMA.
        """
        clean_src = re.sub(r'[^A-Za-z0-9_]', '', source_table.strip())
        clean_tgt = re.sub(r'[^A-Za-z0-9_]', '', target_table.strip())
        sql = f"""
            SELECT
                fk.name AS FK_Name,
                tp.name AS Source_Table,
                cp.name AS Source_Column,
                tr.name AS Target_Table,
                cr.name AS Target_Column
            FROM sys.foreign_keys fk WITH(NOLOCK)
            JOIN sys.foreign_key_columns fkc WITH(NOLOCK) ON fkc.constraint_object_id = fk.object_id
            JOIN sys.tables tp WITH(NOLOCK) ON tp.object_id = fkc.parent_object_id
            JOIN sys.columns cp WITH(NOLOCK) ON cp.object_id = tp.object_id AND cp.column_id = fkc.parent_column_id
            JOIN sys.tables tr WITH(NOLOCK) ON tr.object_id = fkc.referenced_object_id
            JOIN sys.columns cr WITH(NOLOCK) ON cr.object_id = tr.object_id AND cr.column_id = fkc.referenced_column_id
            WHERE (tp.name = '{clean_src}' AND tr.name = '{clean_tgt}')
               OR (tp.name = '{clean_tgt}' AND tr.name = '{clean_src}')
        """
        raw = autonomous_agent.execute_select_sql(sql.strip())
        rows = json.loads(raw) if raw and raw.startswith("[") else []
        if not rows:
            return (
                f"No direct FK relationship found between '{clean_src}' and '{clean_tgt}'. "
                f"Consider joining via an intermediate table (inspect schemas first)."
            )
        lines = [f"FK relationships between {clean_src} ↔ {clean_tgt}:"]
        for r in rows:
            lines.append(
                f"  {r['Source_Table']}.{r['Source_Column']} → "
                f"{r['Target_Table']}.{r['Target_Column']}"
            )
        return "\n".join(lines)

    def search_db_tables(keyword: str) -> str:
        """
        Discovers table names matching a keyword across the 2,550+ MSSQL database tables.
        Input: keyword (e.g. 'doctor', 'appointment', 'bed', 'tariff', 'pharmacy', 'patient').
        """
        clean_kw = re.sub(r'[^A-Za-z0-9_]', '', str(keyword or '').strip())
        if not clean_kw:
            return "Error: search keyword must be alphanumeric."
        sql = f"SELECT TOP 25 TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WITH(NOLOCK) WHERE TABLE_NAME LIKE '%{clean_kw}%' ORDER BY TABLE_NAME"
        raw = autonomous_agent.execute_select_sql(sql.strip())
        rows = json.loads(raw) if raw and raw.startswith("[") else []
        if not rows:
            return f"No tables found matching '{clean_kw}'."
        return "Matching tables: " + ", ".join([r.get("TABLE_NAME", "") for r in rows])

    return [
        Tool(
            name="search_db_tables",
            func=search_db_tables,
            description=(
                "Search table names matching a keyword across all 2,550+ database tables. "
                "Use this to find relevant tables (e.g., 'appointment', 'bed', 'tariff', 'drug', 'bill')."
            ),
        ),
        Tool(
            name="inspect_table_schema",
            func=inspect_table_schema,
            description=(
                "Inspect the column names and data types of any MSSQL table. "
                "Input: table_name (string). Use this first when you don't know the schema."
            ),
        ),
        Tool(
            name="execute_read_only_sql",
            func=execute_read_only_sql,
            description=(
                "Execute a SELECT-only SQL query on the HIMES MSSQL database. "
                "WITH(NOLOCK) and TOP 100 are auto-injected. "
                "Input: full SQL SELECT statement. Returns JSON array of rows."
            ),
        ),
        Tool(
            name="validate_foreign_keys",
            func=validate_foreign_keys,
            description=(
                "Check for foreign-key relationships between two MSSQL tables "
                "to determine the correct JOIN column. "
                "Input: 'source_table, target_table' (comma-separated)."
            ),
        ),
    ]


# ── Agent factory ─────────────────────────────────────────────────────────────

def _build_himes_sql_agent(llm):
    """
    Creates the LangChain ReAct SQL agent with HIMES-specific system prompt.
    """
    from langchain.agents import initialize_agent, AgentType

    tools = _build_agent_tools()

    system_message = (
        "You are the HIMES Dynamic SQL Agent for a hospital information system "
        "with 2,550+ MSSQL tables. Your job is to answer clinical and billing queries "
        "by dynamically discovering the correct tables and building accurate SELECT queries.\n\n"
        "STRICT RULES:\n"
        "1. ONLY use SELECT queries. Never use INSERT, UPDATE, DELETE, DROP, or ALTER.\n"
        "2. Always add WITH(NOLOCK) to every table in FROM and JOIN clauses.\n"
        "3. Always limit results with TOP 100.\n"
        "4. Start by inspecting table schemas if you are unsure of column names.\n"
        "5. Validate foreign keys before writing JOINs.\n"
        "6. Return results as a structured JSON array.\n"
        "7. If you cannot find the answer within 6 steps, explain what tables are needed.\n\n"
        "Available tools: inspect_table_schema, execute_read_only_sql, validate_foreign_keys."
    )

    return initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=False,
        max_iterations=MAX_AGENT_STEPS,
        early_stopping_method="generate",
        handle_parsing_errors=True,
        agent_kwargs={"prefix": system_message},
    )


# ── Public run interface ──────────────────────────────────────────────────────

def run_dynamic_sql_agent(
    query: str,
    session_context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Runs the LangChain Dynamic SQL Agent for queries the deterministic engine
    could not handle. Falls back gracefully if LLM key is not configured.

    Args:
        query:           Natural-language query (any language).
        session_context: Active entities dict {'mrn': ..., 'visit_no': ...}.

    Returns:
        {
            'reply':      str,   — formatted answer
            'sql_used':   str,   — last executed SQL
            'model_used': str,
            'status':     str,
        }
    """
    import os
    from dotenv import load_dotenv
    load_dotenv(override=True)

    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY", "")

    # Build LLM — use Gemini (already used in main.py)
    llm = None
    model_name = ""

    if gemini_key and not gemini_key.startswith("your_"):
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                google_api_key=gemini_key,
                temperature=0,
                max_retries=1,
            )
            model_name = "gemini-2.0-flash"
        except Exception as e:
            print(f"[SQLAgent] Gemini init failed: {e}")

    if llm is None:
        return {
            "reply": "SQL Agent unavailable — no LLM API key configured. Using deterministic engine.",
            "sql_used": "",
            "model_used": "unavailable",
            "status": "no_llm",
        }

    try:
        # Inject active context into the query for entity resolution
        enriched_query = query
        if session_context:
            active = session_context.get("active_entities", {})
            mrn = active.get("mrn")
            visit = active.get("visit_no")
            if mrn:
                enriched_query += f"\n[Context: Active MRN = {mrn}"
                if visit:
                    enriched_query += f", Active Visit No = {visit}"
                enriched_query += "]"

        agent = _build_himes_sql_agent(llm)
        result = agent.run(enriched_query)

        # Format the agent's raw result through zero-token formatter if it's JSON rows
        formatted = result
        if isinstance(result, str) and result.strip().startswith("["):
            try:
                rows = json.loads(result)
                from skills.himes_skills import skill_zero_token_formatter
                from utils.table_formatter import detect_language
                lang = detect_language(query)
                formatted = skill_zero_token_formatter(
                    rows=rows, intent="dynamic_sql", lang=lang,
                    mrn=session_context.get("active_entities", {}).get("mrn") if session_context else None,
                )
            except Exception:
                pass

        return {
            "reply": formatted,
            "sql_used": "(agent-generated — see developer mode for trace)",
            "model_used": f"HIMES Dynamic SQL Agent ({model_name})",
            "status": "success",
        }

    except Exception as e:
        return {
            "reply": f"⚠️ SQL Agent encountered an error: {str(e)}",
            "sql_used": "",
            "model_used": f"HIMES Dynamic SQL Agent ({model_name}) — Error",
            "status": "error",
            "error": str(e),
        }


__all__ = ["run_dynamic_sql_agent"]
