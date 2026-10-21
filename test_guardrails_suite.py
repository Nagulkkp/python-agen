import sys
sys.stdout.reconfigure(encoding='utf-8')
import requests
import json
from guardrails import validate_sql_query, validate_command_directory_safety, SecurityException

print("=" * 60)
print("TEST 1: DATABASE GUARDRAILS (SELECT ONLY)")
print("=" * 60)

test_queries = [
    ("SELECT * FROM Patient_Visit_Basic_Details WHERE id = 1", True),
    ("WITH cte AS (SELECT id FROM patients) SELECT * FROM cte", True),
    ("UPDATE Patient_Visit_Basic_Details SET Active_Status = 'D' WHERE id = 1", False),
    ("DELETE FROM Patient_Visit_Basic_Details WHERE id = 1", False),
    ("DROP TABLE patients", False),
    ("TRUNCATE TABLE logs", False),
    ("ALTER TABLE patients ADD COLUMN test int", False),
    ("INSERT INTO patients (name) VALUES ('test')", False),
    ("SELECT 1; DROP TABLE patients;", False)
]

for query, should_pass in test_queries:
    try:
        validate_sql_query(query)
        assert should_pass, f"Expected violation but passed: {query}"
        print(f"✅ PASSED (Allowed): {query[:45]}...")
    except SecurityException as e:
        assert not should_pass, f"Expected pass but blocked: {query}"
        print(f"🛡️ BLOCKED (Security Guardrail): {query[:45]}... -> {e}")

print("\n" + "=" * 60)
print("TEST 2: DIRECTORY LOCK GUARDRAILS (NAGUL FOLDER ONLY)")
print("=" * 60)

test_commands = [
    ("ls -la /L9/nagul/himes-ai", True),
    ("php artisan route:list", True),
    ("cd .. && ls", False),
    ("cd /etc && cat passwd", False),
    ("cd /L9/other_developer && ls", False),
    ("rm -rf /", False),
    ("rm -rf /var/www", False),
]

for cmd, should_pass in test_commands:
    try:
        validate_command_directory_safety(cmd, allowed_dir="/L9/nagul")
        assert should_pass, f"Expected violation but passed: {cmd}"
        print(f"✅ PASSED (Allowed): {cmd}")
    except SecurityException as e:
        assert not should_pass, f"Expected pass but blocked: {cmd}"
        print(f"🛡️ BLOCKED (Directory Lock): {cmd} -> {e}")

print("\n" + "=" * 60)
print("TEST 3 & 4: /api/chat ENDPOINT WITH SYSTEM PROMPT")
print("=" * 60)

try:
    res = requests.post("http://127.0.0.1:8050/api/chat", json={
        "message": "emr workstation page la yesterday date la patient count enna",
        "session_id": "test_nagul_session"
    }, timeout=30)
    print("Chat API Response Status Code:", res.status_code)
    print("Response JSON:\n", json.dumps(res.json(), indent=2, ensure_ascii=False))
except Exception as e:
    print("Error calling /api/chat:", e)
