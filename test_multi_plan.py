import os
import datetime
from dotenv import load_dotenv

load_dotenv(override=True)

from main import generate_ai_response

def plan_command_with_ai(task: str, context: dict = None) -> str:
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    yesterday_str = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    planner_prompt = f"""You are the backend planner for an autonomous AI Assistant inside HIMES Laravel Hospital Management System.
Current Date: {today_str} (Yesterday was {yesterday_str}).
Database Engine: Microsoft SQL Server (database: himes_dev_new).
Docker container: nagul.
Laravel project root inside container: /var/www/html/himes-ai.
Host project path: /L9/nagul/himes-ai.

User Task/Question: "{task}"
Context: {context or {}}

Determine what shell/tinker command to run on the server to get the exact data needed to answer the question.
Rules:
1. If the question asks for patient counts, visits, appointments, EMR records, or hospital statistics:
   Use `docker exec nagul php /var/www/html/himes-ai/artisan tinker --execute="echo json_encode(DB::select(\\"...SQL...\\"));"`
   - Table for patient visits / EMR workstation: `Patient_Visit_Basic_Details`
   - Key columns: `Patient_Visit_Registered_Date_Time`, `Active_Status = 'A'`, `Visit_Cancellation_Flag = 'N'`, `Visit_Is_Non_Consultation = 'N'`, `Branch_Code`, `Is_EMR_Completed`, `Is_EMR_In_Progress`.
   - Date filtering in MSSQL: `CAST(Patient_Visit_Registered_Date_Time AS DATE) = '{yesterday_str}'` (for yesterday) or `{today_str}` (for today).
2. If the question asks about Laravel errors, bugs, exceptions, or crashes:
   Use `tail -n 60 /L9/nagul/himes-ai/storage/logs/laravel.log`
3. If the question asks about routes or URLs:
   Use `cd /L9/nagul/himes-ai && php artisan route:list | grep -i ...`
4. If the question asks about server health, memory, disk, or docker:
   Use `df -h`, `free -h`, `uptime`, or `docker ps`
5. If the question is a greeting, general knowledge, or requires no server/DB action:
   Output `NONE`.

Output format:
ONLY output the single command line string to execute, with no markdown code blocks, no backticks, and no explanation.
If no command needed, output NONE.
"""
    raw_cmd = generate_ai_response(planner_prompt).strip()
    if raw_cmd.startswith("```"):
        raw_cmd = raw_cmd.split("\n", 1)[1].rsplit("\n", 1)[0].strip()
        if raw_cmd.startswith("bash") or raw_cmd.startswith("sh"):
            raw_cmd = raw_cmd.split("\n", 1)[1].strip()
    return raw_cmd

if __name__ == "__main__":
    queries = [
        "emr workstation page la yesterday date la patient count enna",
        "latest laravel error check pannu",
        "hi vanakkam"
    ]
    for q in queries:
        plan = plan_command_with_ai(q)
        print(f"Query: {q}")
        print(f"Plan:  {plan}\n")
