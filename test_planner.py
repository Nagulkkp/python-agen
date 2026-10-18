import os
import json
import datetime
from dotenv import load_dotenv
from ssh_tool import execute_ssh_command

load_dotenv(override=True)

from langchain_google_genai import ChatGoogleGenerativeAI

gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key=gemini_key,
    temperature=0.1
)

def test_planner(user_query: str):
    today_date = "2026-10-17"
    yesterday_date = "2026-10-16"
    
    planner_prompt = f"""You are the backend planner for an autonomous AI Assistant inside HIMES Laravel Hospital Management System.
Current Date: {today_date} (Yesterday was {yesterday_date}).
Database Engine: Microsoft SQL Server (database: himes_dev_new).
Docker container: nagul.
Laravel project root inside container: /var/www/html/himes-ai.

User Question: "{user_query}"

Determine what shell/tinker command to run on the server to get the exact data needed to answer the question.
Rules:
1. If the question asks for patient counts, visits, appointments, or database records:
   Use `docker exec nagul php /var/www/html/himes-ai/artisan tinker --execute="echo json_encode(DB::select(\\"...SQL...\\"));"`
   - Table for patient visits / EMR workstation: `Patient_Visit_Basic_Details`
   - Key columns: `Patient_Visit_Registered_Date_Time`, `Active_Status = 'A'`, `Visit_Cancellation_Flag = 'N'`, `Visit_Is_Non_Consultation = 'N'`, `Branch_Code`, `Is_EMR_Completed`, `Is_EMR_In_Progress`.
   - Date filtering in MSSQL: `CAST(Patient_Visit_Registered_Date_Time AS DATE) = '{yesterday_date}'` (or appropriate date).
2. If the question asks about errors/bugs:
   Use `tail -n 60 /L9/nagul/himes-ai/storage/logs/laravel.log`
3. If the question asks about routes:
   Use `cd /L9/nagul/himes-ai && php artisan route:list | grep -i ...`
4. If no command is needed (e.g. general greeting or knowledge), return NONE.

Output format:
ONLY output the single command line string to execute, with no markdown code blocks, no quotes, and no explanation.
If no command needed, output NONE.
"""
    raw_content = llm.invoke(planner_prompt).content
    if isinstance(raw_content, list):
        cmd = "".join([part.get("text", "") if isinstance(part, dict) else str(part) for part in raw_content]).strip()
    else:
        cmd = str(raw_content).strip()
    # Remove markdown code block if present
    if cmd.startswith("```"):
        cmd = cmd.split("\n", 1)[1].rsplit("\n", 1)[0].strip()
        if cmd.startswith("bash") or cmd.startswith("sh"):
            cmd = cmd.split("\n", 1)[1].strip()
            
    print(f"Generated Command:\n{cmd}\n")
    if cmd != "NONE":
        res = execute_ssh_command.invoke({"command": cmd})
        print(f"Command Output:\n{res}\n")
        
        # Now generate final response
        final_prompt = f"""You are the friendly AI assistant integrated inside HIMES hospital system for user Nagul.
User Question: "{user_query}"
Command Executed: `{cmd}`
Live Data / Query Result:
```
{res}
```

Instructions:
1. Provide a direct, simple, and crystal-clear answer in Tanglish / Tamil + English.
2. Give the exact numbers/facts right at the start.
3. Keep it brief, simple, and clean as requested by the user. Do NOT give long generic tutorials or manual steps unless asked.
"""
        final_raw = llm.invoke(final_prompt).content
        if isinstance(final_raw, list):
            final_res = "".join([part.get("text", "") if isinstance(part, dict) else str(part) for part in final_raw]).strip()
        else:
            final_res = str(final_raw).strip()
        print(f"Final Answer:\n{final_res}")

if __name__ == "__main__":
    test_planner("emr workstation page la yesterday date la patient count enna")
