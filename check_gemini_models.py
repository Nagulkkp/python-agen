import os
import sys
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from dotenv import load_dotenv
load_dotenv(override=True)
import google.genai as genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

models = [
    "gemini-3.1-flash-lite",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash-lite-preview-02-05",
    "gemini-1.5-flash",
    "gemini-1.5-flash-8b",
    "gemini-1.5-pro",
    "gemini-2.0-flash",
    "gemini-3.8-flash",
    "gemini-3.5-flash"
]

for m in models:
    try:
        res = client.models.generate_content(model=m, contents="hi")
        print(f"[OK] {m}: ACTIVE and WORKING! ({res.text.strip()[:30]})")
    except Exception as e:
        err_msg = str(e)
        if "RESOURCE_EXHAUSTED" in err_msg:
            print(f"[QUOTA EXCEEDED] {m}: 429 Quota Exceeded (Free Tier limit reached)")
        elif "NOT_FOUND" in err_msg:
            print(f"[NOT FOUND] {m}: Not Found / Deprecated")
        else:
            print(f"[ERROR] {m}: {err_msg[:60]}")
