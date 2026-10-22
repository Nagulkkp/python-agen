"""
skills/himes_skills.py
======================
HIMES Modular Agent Skills Registry.

Each skill is a THIN WRAPPER around existing production functions:
  - autonomous_agent.execute_select_sql()       → live MSSQL execution
  - valkey_himes_manager.valkey_manager.*()     → caching
  - utils.table_formatter.*()                   → zero-token formatting
  - main.py intent routing                      → existing keyword & entity logic

Skills add NO new keyword dictionaries or SQL templates.
They simply expose named, composable call interfaces for the LangChain chain layer.
"""

import sys
import hashlib
from typing import Any, Callable, Dict, List, Optional
from functools import wraps

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# ─────────────────────────────────────────────────────────────────────────────
# Skill Registry
# ─────────────────────────────────────────────────────────────────────────────
_SKILL_REGISTRY: Dict[str, Dict[str, Any]] = {}


def register_skill(name: str, description: str, tags: Optional[List[str]] = None):
    """Decorator — registers a function as a named HIMES skill."""
    def decorator(fn: Callable):
        _SKILL_REGISTRY[name] = {
            "fn": fn,
            "description": description,
            "tags": tags or [],
        }
        @wraps(fn)
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def get_skill(name: str) -> Optional[Callable]:
    """Returns the skill callable by name, or None if not registered."""
    entry = _SKILL_REGISTRY.get(name)
    return entry["fn"] if entry else None


def list_skills() -> List[Dict[str, Any]]:
    """Returns all registered skill metadata (no callables exposed)."""
    return [
        {"name": k, "description": v["description"], "tags": v["tags"]}
        for k, v in _SKILL_REGISTRY.items()
    ]


# ─────────────────────────────────────────────────────────────────────────────
# SKILL 1: Multilingual NL2SQL
# Delegates entirely to the existing autonomous_agent pipeline.
# main.py already contains all keyword routing & SQL templates.
# This skill exposes that pipeline as a named callable for LangChain chains.
# ─────────────────────────────────────────────────────────────────────────────
@register_skill(
    name="skill_multilingual_nl2sql",
    description=(
        "Converts any natural-language message (any world language) into a structured "
        "HIMES MSSQL query result by delegating to the existing autonomous_agent pipeline. "
        "Returns {'rows': list, 'sql': str, 'intent': str, 'mrn': str, 'visit_no': str, 'lang': str}."
    ),
    tags=["nl2sql", "multilingual", "sql"],
)
def skill_multilingual_nl2sql(
    message: str,
    session_context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Dynamic NL2SQL skill: converts natural language query into MSSQL execution.
    Delegates to dynamic_sql_agent or autonomous_agent safely with SELECT-only guardrails.
    """
    from autonomous_agent import autonomous_agent
    from utils.table_formatter import detect_language
    from agents.sql_agent import run_dynamic_sql_agent

    lang = detect_language(message)

    # Inherit session entities (MRN, visit_no) for pronoun resolution
    active_entities = {}
    if session_context and isinstance(session_context, dict):
        active_entities = session_context.get("active_entities", {})

    agent_result = run_dynamic_sql_agent(query=message, session_context=session_context)
    reply_text = agent_result.get("reply", "")
    sql_used = agent_result.get("sql_used", "")

    return {
        "reply": reply_text,
        "sql": sql_used,
        "intent": "dynamic_sql",
        "mrn": active_entities.get("mrn"),
        "visit_no": active_entities.get("visit_no"),
        "lang": lang,
        "status": agent_result.get("status", "success"),
    }


# ─────────────────────────────────────────────────────────────────────────────
# SKILL 2: Zero-Token Formatter
# Delegates to utils/table_formatter.py — already production-tested.
# ─────────────────────────────────────────────────────────────────────────────
@register_skill(
    name="skill_zero_token_formatter",
    description=(
        "Formats raw MSSQL row dicts into localized human-centric action cards. "
        "Delegates to utils.table_formatter.format_user_friendly_response(). "
        "Zero LLM tokens. Supports 'user' (collapsible) and 'developer' (full SQL diagnostic) modes."
    ),
    tags=["formatter", "zero-token", "presentation"],
)
def skill_zero_token_formatter(
    rows: List[Dict[str, Any]],
    intent: str = "unbilled_services",
    lang: str = "en",
    mrn: Optional[str] = None,
    visit_no: Optional[str] = None,
    mode: str = "user",
    executed_sql: Optional[str] = None,
) -> str:
    """Thin wrapper around the existing table_formatter."""
    from utils.table_formatter import format_user_friendly_response

    return format_user_friendly_response(
        rows,
        query_context={
            "lang": lang,
            "mrn": mrn or "N/A",
            "visit_no": visit_no or "N/A",
            "intent": intent,
            "executed_sql": executed_sql or "",
        },
        mode=mode,
    )


# ─────────────────────────────────────────────────────────────────────────────
# SKILL 3: Panic Threshold Evaluator
# Lab panic thresholds are seeded into Valkey by valkey_himes_manager.
# This skill reads them from Valkey and evaluates live lab rows.
# ─────────────────────────────────────────────────────────────────────────────
@register_skill(
    name="skill_panic_threshold_evaluator",
    description=(
        "Cross-references live lab result rows against Valkey-seeded clinical panic thresholds. "
        "Injects 🔴 escalation alerts for out-of-range values. "
        "Returns {'enriched_rows': list, 'critical_alerts': list, 'has_critical': bool}."
    ),
    tags=["clinical", "lab", "critical-values", "alerts"],
)
def skill_panic_threshold_evaluator(
    lab_rows: List[Dict[str, Any]],
    patient_mrn: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Reads panic thresholds from Valkey (seeded by valkey_himes_manager),
    evaluates each lab row, and injects critical alert banners.
    """
    from valkey_himes_manager import valkey_manager

    # Load thresholds from Valkey (fast-path) — seeded at startup
    raw_thresholds = valkey_manager.get_himes_context("lab_panic_thresholds") or {}
    if not raw_thresholds:
        # Fallback: trigger re-seed and fetch again
        valkey_manager._seed_default_himes_flows()
        raw_thresholds = valkey_manager.get_himes_context("lab_panic_thresholds") or {}

    critical_alerts: List[str] = []
    enriched: List[Dict[str, Any]] = []

    for row in lab_rows:
        row_copy = dict(row)
        test_name = str(row.get("Test_Name") or row.get("test_name") or "").strip()
        result_raw = row.get("Result_Value") or row.get("result_value") or ""
        panic_flag = False

        try:
            result_val = float(str(result_raw).replace(",", "").strip())
        except (ValueError, TypeError):
            enriched.append({**row_copy, "panic_flag": False})
            continue

        for analyte, thresholds in raw_thresholds.items():
            if analyte.lower() in test_name.lower():
                low = thresholds.get("low")
                high = thresholds.get("high")
                unit = thresholds.get("unit", "")
                alert_label = thresholds.get("alert", "CRITICAL VALUE")

                direction = ""
                if low is not None and result_val < float(low):
                    direction = f"LOW ({result_val} {unit} < {low} {unit})"
                elif high is not None and result_val > float(high):
                    direction = f"HIGH ({result_val} {unit} > {high} {unit})"

                if direction:
                    panic_flag = True
                    mrn_tag = f" | Patient MRN: `{patient_mrn}`" if patient_mrn else ""
                    critical_alerts.append(
                        f"{alert_label} — {test_name}: **{direction}**{mrn_tag}"
                    )
                break

        row_copy["panic_flag"] = panic_flag
        enriched.append(row_copy)

    return {
        "enriched_rows": enriched,
        "critical_alerts": critical_alerts,
        "has_critical": len(critical_alerts) > 0,
    }


# ─────────────────────────────────────────────────────────────────────────────
# SKILL 4: Valkey Cache Manager
# Thin wrapper around valkey_manager.get/cache_ephemeral_query().
# ─────────────────────────────────────────────────────────────────────────────
@register_skill(
    name="skill_valkey_cache_manager",
    description=(
        "get/set/invalidate operations on the SHA256 ephemeral query cache. "
        "Wraps valkey_manager.get_ephemeral_query() and cache_ephemeral_query(). "
        "Never caches raw PHI — only formatted response strings."
    ),
    tags=["cache", "valkey", "performance"],
)
def skill_valkey_cache_manager(
    action: str,
    query: Optional[str] = None,
    mrn: Optional[str] = None,
    session_id: Optional[str] = None,
    value: Optional[str] = None,
    ttl: int = 300,
) -> Dict[str, Any]:
    """Thin wrapper — delegates directly to valkey_manager ephemeral cache methods."""
    from valkey_himes_manager import valkey_manager

    if action == "get":
        cached = valkey_manager.get_ephemeral_query(
            query or "", active_mrn=mrn or "", session_id=session_id or ""
        )
        if cached and isinstance(cached, dict):
            return {
                "hit": True,
                "value": cached.get("formatted_response", ""),
                "action": action,
            }
        return {"hit": False, "value": None, "action": action}

    elif action == "set":
        if not value:
            return {"hit": False, "value": None, "action": action, "error": "no_value"}
        valkey_manager.cache_ephemeral_query(
            query or "", active_mrn=mrn or "", session_id=session_id or "",
            formatted_response=value, ttl=ttl
        )
        return {"hit": True, "value": value, "action": action}

    elif action == "invalidate":
        valkey_manager.invalidate_patient_snapshot(mrn or "")
        return {"hit": False, "value": None, "action": action}

    return {"hit": False, "value": None, "action": "unknown", "error": "invalid_action"}


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────
__all__ = [
    "register_skill",
    "get_skill",
    "list_skills",
    "skill_multilingual_nl2sql",
    "skill_zero_token_formatter",
    "skill_panic_threshold_evaluator",
    "skill_valkey_cache_manager",
]
