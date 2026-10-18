import re
import os
from pathlib import PurePosixPath

class SecurityException(Exception):
    """Raised when an operation violates Nagul's AI Agent Safety Guardrails."""
    pass

# ====================================================================
# 1. DATABASE SAFETY GUARDRAIL: SELECT ONLY VALIDATOR
# ====================================================================

FORBIDDEN_SQL_KEYWORDS = [
    r"\bUPDATE\b",
    r"\bDELETE\b",
    r"\bDROP\b",
    r"\bTRUNCATE\b",
    r"\bALTER\b",
    r"\bINSERT\b",
    r"\bCREATE\b",
    r"\bREPLACE\b",
    r"\bMERGE\b",
    r"\bUPSERT\b",
    r"\bGRANT\b",
    r"\bREVOKE\b",
    r"\bEXEC\b",
    r"\bEXECUTE\b",
    r"\bSHUTDOWN\b",
    r"\bINTO\b\s+(?:OUTFILE|DUMPFILE)"  # File export protection
]

def validate_sql_query(query: str) -> bool:
    """
    Intercepts SQL queries before execution.
    STRICT RULE: Only SELECT queries are permitted.
    If UPDATE, DELETE, DROP, INSERT, ALTER, or destructive commands are found,
    it raises a SecurityException and aborts immediately.
    """
    if not query or not query.strip():
        raise SecurityException("Empty SQL query rejected.")

    # Strip SQL comments (-- and /* ... */) and wrapper quotes/escapes
    cleaned = re.sub(r"--.*$", "", query, flags=re.MULTILINE)
    cleaned = re.sub(r"/\*.*?\*/", "", cleaned, flags=re.DOTALL).strip(' \t\n\r\\"\'`')

    # Must start with SELECT or WITH (for CTE queries that select)
    first_word_match = re.match(r"^\s*([A-Za-z]+)", cleaned)
    if not first_word_match:
        raise SecurityException("Invalid SQL query syntax.")

    first_word = first_word_match.group(1).upper()
    if first_word not in ["SELECT", "WITH"]:
        raise SecurityException(
            f"Database Security Violation: Only SELECT queries are allowed. "
            f"Query started with '{first_word}'. Execution aborted!"
        )

    # Check for forbidden keywords anywhere in query
    for kw in FORBIDDEN_SQL_KEYWORDS:
        if re.search(kw, cleaned, flags=re.IGNORECASE):
            matched = kw.replace(r"\b", "")
            raise SecurityException(
                f"Database Security Violation: Dangerous keyword '{matched}' detected! "
                f"UPDATE, DELETE, DROP, INSERT, and ALTER are strictly forbidden."
            )

    # Prevent multiple queries separated by semicolons (e.g. SELECT 1; DROP TABLE users;)
    statements = [s.strip() for s in cleaned.split(";") if s.strip()]
    if len(statements) > 1:
        for stmt in statements:
            stmt_first = re.match(r"^\s*([A-Za-z]+)", stmt)
            if not stmt_first or stmt_first.group(1).upper() not in ["SELECT", "WITH"]:
                raise SecurityException(
                    "Database Security Violation: Multi-statement query contains non-SELECT statement!"
                )

    return True


# ====================================================================
# 2. DIRECTORY & PATH LOCK GUARDRAIL
# ====================================================================

DEFAULT_ALLOWED_DIR = "/L9/nagul"

def is_path_inside_allowed_dir(target_path: str, allowed_base: str = DEFAULT_ALLOWED_DIR) -> bool:
    """Checks whether target_path stays strictly within allowed_base directory."""
    try:
        norm_target = PurePosixPath(os.path.normpath(target_path).replace("\\", "/"))
        norm_base = PurePosixPath(os.path.normpath(allowed_base).replace("\\", "/"))
        return norm_target == norm_base or norm_base in norm_target.parents
    except Exception:
        return False

def validate_command_directory_safety(command: str, allowed_dir: str = DEFAULT_ALLOWED_DIR) -> bool:
    """
    Validates terminal commands before SSH execution.
    STRICT RULE: Operates strictly inside Nagul's directory.
    Blocks directory traversal (cd ..), escaping to root (/), or referencing
    paths outside Nagul's workspace.
    """
    cmd = command.strip()

    # Disallow destructive system-wide commands
    forbidden_patterns = [
        r"\brm\s+-[a-zA-Z]*[rfRF][a-zA-Z]*\s+/(?:$|\s|;|\*)",        # rm -rf / or rm -rf /*
        r"\brm\s+-[a-zA-Z]*[rfRF][a-zA-Z]*\s+/var(?:$|\s|/|;)",     # rm -rf /var
        r"\brm\s+-[a-zA-Z]*[rfRF][a-zA-Z]*\s+/etc(?:$|\s|/|;)",     # rm -rf /etc
        r"\brm\s+-[a-zA-Z]*[rfRF][a-zA-Z]*\s+/home(?:$|\s|/|;)",    # rm -rf /home
        r"\bmkfs\b",
        r"\bdd\s+if=",
        r"\bshutdown\b",
        r"\breboot\b",
        r"\bchmod\s+777\s+/(?:$|\s|;)",
    ]
    for pat in forbidden_patterns:
        if re.search(pat, cmd, flags=re.IGNORECASE):
            raise SecurityException(f"Command Security Violation: Prohibited destructive command detected: '{cmd}'")

    # Disallow cd .. or directory traversal attempting to leave Nagul's folder
    if re.search(r"\bcd\s+\.\.(?:/|$|\s|;)", cmd):
        raise SecurityException("Directory Lock Violation: Escaping parent directory via 'cd ..' is strictly forbidden!")

    # Check for cd into unauthorized root or home directories
    cd_matches = re.findall(r"\bcd\s+([^\s;&|]+)", cmd)
    for cd_target in cd_matches:
        if cd_target.startswith("/"):
            if not is_path_inside_allowed_dir(cd_target, allowed_dir):
                raise SecurityException(
                    f"Directory Lock Violation: Navigation to '{cd_target}' blocked! "
                    f"Agent is restricted strictly inside '{allowed_dir}'."
                )

    return True
