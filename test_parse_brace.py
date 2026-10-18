import re, json

s = 'Action: execute_select_sql({"sql_query": "SELECT COUNT(*) as test_patient_count FROM Patient_Bill_Header pbh JOIN Patient_Visit_Basic_Details pvbd ON pbh.Patient_Visit_Basic_Details_Serial_No = pvbd.Patient_Visit_Basic_Details_Serial_No JOIN Patient_Personal_Details ppd ON pvbd.Patient_Master_Serial_No = ppd.Patient_Master_Serial_No WHERE CAST(pbh.Bill_Date AS DATE) = CAST(DATEADD(day, -1, GETDATE()) AS DATE) AND (ppd.Patient_First_Name = \'Test\' OR ppd.Patient_First_Name = \'TEST\')"})'

m = re.search(r"Action:\s*([a-zA-Z0-9_]+)", s, re.I)
action = m.group(1).strip()
after = s[m.end():]
fb = after.find('{')
lb = after.rfind('}')
raw = after[fb:lb+1]
args = json.loads(raw)

print("Action:", action)
print("Query from args:", args.get("sql_query"))
