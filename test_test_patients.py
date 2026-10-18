import sys
from ssh_sandbox import sandboxed_ssh

test_sql = """
docker exec nagul php /var/www/html/himes-ai/artisan tinker --execute="
\\$res = DB::select(\\"
    SELECT 
        COUNT(DISTINCT pvbd.Patient_Basic_Details_Serial_No) as distinct_billed_patients_with_test,
        COUNT(DISTINCT pbh.Patient_Bill_Header_Serial_No) as total_bills_count
    FROM Patient_Visit_Basic_Details pvbd
    JOIN Patient_Basic_Encript_Details PBED ON PBED.Patient_Basic_Details_Serial_No = pvbd.Patient_Basic_Details_Serial_No
    JOIN Patient_Visit_Services pvs ON pvs.Patient_Visit_Basic_Details_Serial_No = pvbd.Patient_Visit_Basic_Details_Serial_No
      AND pvs.Patient_Visit_Service_Cancellation_Flag = 'N' AND pvs.Active_Status = 'A'
    JOIN Patient_Bill_Detail_Services_Packages_Resources_Drugs pbdsprd ON pbdsprd.Patient_Visit_Services_Serial_No = pvs.Patient_Visit_Services_Serial_No
      AND pbdsprd.Active_Status = 'A' AND pbdsprd.Service_Resource_Drug_Cancellation_Flag = 'N'
    JOIN Patient_Bill_Header pbh ON pbh.Patient_Bill_Header_Serial_No = pbdsprd.Bill_Header_Serial_No
      AND pbh.Bill_Cancellation_Flag = 'N'
    WHERE CAST(pvbd.Patient_Visit_Registered_Date_Time AS DATE) = CAST(DATEADD(day, -1, GETDATE()) AS DATE)
      AND pvbd.Active_Status = 'A' AND pvbd.Visit_Cancellation_Flag = 'N'
      AND (PBED.Patient_First_Name LIKE '%Test%' OR PBED.Patient_Middle_Name LIKE '%Test%' OR PBED.Patient_Last_Name LIKE '%Test%')
\\");
echo json_encode(\\$res);
"
"""

out = sandboxed_ssh.execute_sandboxed_command(test_sql.strip())
print("Test Patients Count:", out)
