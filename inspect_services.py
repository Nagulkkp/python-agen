import sys
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from ssh_sandbox import sandboxed_ssh

sql = """
SELECT 
    pvbd.Permanent_Visit_No,
    pvs.Patient_Visit_Services_Serial_No,
    pvs.Patient_Visit_Service_Cancellation_Flag,
    pvs.Active_Status,
    s.CPT_Code,
    s.Service_Internal_Code,
    s.Service_Description
FROM Patient_Visit_Basic_Details pvbd
JOIN Patient_Visit_Services pvs ON pvs.Patient_Visit_Basic_Details_Serial_No = pvbd.Patient_Visit_Basic_Details_Serial_No
JOIN Service_USSDB sussdb ON sussdb.Service_USSDB_Serial_No = pvs.Service_USSDB_Serial_No
JOIN Service s ON s.Service_Serial_No = sussdb.Service_Serial_No
WHERE pvbd.Permanent_Visit_No = '16928'
"""

escaped_sql = sql.strip().replace('"', '\\"').replace('\n', ' ')
cmd = f'docker exec nagul php /var/www/html/himes-ai/artisan tinker --execute="echo json_encode(DB::select(\\"{escaped_sql}\\"));"'
out = sandboxed_ssh.execute_sandboxed_command(cmd)
print("Actual services in DB for Visit 16928:")
print(out)
