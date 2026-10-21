@echo off
title Local Redis Server (Port 6379)
echo ====================================================
echo Starting Local Redis Server for HIMES Python Agent
echo Port: 127.0.0.1:6379
echo ====================================================
cd /d "%~dp0"
if not exist redis_server\redis-server.exe (
    echo [ERROR] redis_server\redis-server.exe not found!
    pause
    exit /b 1
)
redis_server\redis-server.exe --port 6379 --maxmemory 256mb
