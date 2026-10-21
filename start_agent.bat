@echo off
title HIMES Python AI Agent (Port 8050)
echo ====================================================
echo Starting Nagul HIMES AI Agent Service
echo Host: http://127.0.0.1:8050
echo Valkey: http://127.0.0.1:6379
echo ====================================================
cd /d "%~dp0"
.\venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8050 --reload
pause
