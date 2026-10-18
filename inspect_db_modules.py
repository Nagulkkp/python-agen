import json
from autonomous_agent import autonomous_agent

def check():
    sql = """
    SELECT TABLE_NAME 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_TYPE='BASE TABLE' AND (
        TABLE_NAME LIKE '%Menu%' OR 
        TABLE_NAME LIKE '%Module%' OR 
        TABLE_NAME LIKE '%Permission%'
    )
    ORDER BY TABLE_NAME
    """
    out = autonomous_agent.execute_select_sql(sql)
    tables = [r['TABLE_NAME'] for r in json.loads(out)]
    print("Found Tables:", tables)

    # Check sample contents of tables like Menus, Modules_Master, etc.
    for t in tables[:8]:
        try:
            sample = autonomous_agent.execute_select_sql(f"SELECT TOP 3 * FROM {t}")
            cols = list(json.loads(sample)[0].keys()) if json.loads(sample) else []
            print(f"Table {t}: Columns -> {cols}")
        except Exception as e:
            print(f"Table {t} error: {e}")

if __name__ == "__main__":
    check()
