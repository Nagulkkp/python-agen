import sys
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from ssh_sandbox import sandboxed_ssh

sql = """
SELECT TOP 10 
    pvbd.Permanent_Visit_No,
    pvbd.Patient_Visit_Registered_Date_Time,
    pvbd.Is_Visit_Completely_Billed,
    pbh.Patient_Bill_Header_Serial_No,
    pbh.Bill_No,
    pbh.Bill_Net_Value,
    pbh.Is_Bill_Finalized,
    pbh.Bill_Cancellation_Flag
FROM Patient_Basic_Details pbd
JOIN Patient_Visit_Basic_Details pvbd ON pvbd.Patient_Basic_Details_Serial_No = pbd.Patient_Basic_Details_Serial_No
LEFT JOIN Patient_Bill_Header pbh ON pbh.Patient_Visit_Basic_Details_Serial_No = pvbd.Patient_Visit_Basic_Details_Serial_No AND pbh.Bill_Cancellation_Flag = 'N'
WHERE pbd.Permanent_MRN_No = '3004383'
ORDER BY pvbd.Patient_Visit_Registered_Date_Time DESC
"""

escaped_sql = sql.strip().replace('"', '\\"').replace('\n', ' ')
cmd = f'docker exec nagul php /var/www/html/himes-ai/artisan tinker --execute="echo json_encode(DB::select(\\"{escaped_sql}\\"));"'
out = sandboxed_ssh.execute_sandboxed_command(cmd)
print("Visits for MRN 3004383:")
print(out)
