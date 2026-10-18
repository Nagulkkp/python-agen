import json
import sys
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from autonomous_agent import autonomous_agent

sql = """
SELECT TABLE_NAME 
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_TYPE='BASE TABLE' AND (
    TABLE_NAME LIKE '%Deposit%' OR 
    TABLE_NAME LIKE '%Receipt%' OR 
    TABLE_NAME LIKE '%Payment%'
)
ORDER BY TABLE_NAME
"""
res = json.loads(autonomous_agent.execute_select_sql(sql))
print("Deposit / Receipt / Payment Tables:")
for r in res:
    print(" ", r['TABLE_NAME'])
