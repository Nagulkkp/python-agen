import json
import sys
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from autonomous_agent import autonomous_agent

visit_serial = 97340
bill_serial = 59386

print("--- 1. PATIENT_VISIT_DEPOSITS ---")
sql_dep = f"SELECT * FROM Patient_Visit_Deposits WHERE Patient_Visit_Basic_Details_Serial_No = {visit_serial}"
res_dep = json.loads(autonomous_agent.execute_select_sql(sql_dep))
print("Deposits:", res_dep)

print("\n--- 2. PATIENT_BILL_HEADER_PAYMENTS_RECEIVED ---")
sql_pay = f"SELECT * FROM Patient_Bill_Header_Payments_Received WHERE Patient_Bill_Header_Serial_No = {bill_serial}"
res_pay = json.loads(autonomous_agent.execute_select_sql(sql_pay))
print("Payments received:", res_pay)

print("\n--- 3. RECEIPTS_FOR_PAYMENTS_RECEIVED ---")
try:
    if res_pay:
        pay_serial = res_pay[0].get('Patient_Bill_Header_Payments_Received_Serial_No')
        sql_rcpt = f"SELECT * FROM Receipts_For_Payments_Received WHERE Patient_Bill_Header_Payments_Received_Serial_No = {pay_serial}"
        print("Receipts:", json.loads(autonomous_agent.execute_select_sql(sql_rcpt)))
except Exception as e:
    print("Receipts query error:", e)
