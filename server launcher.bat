@echo off
title LEO SERVER
cd /d "%~dp0"

echo [SYSTEM] Starting Chrome...
:: Launch Chrome first
start "http://127.0.0.1:8000"

echo [SYSTEM] Warming up Leo's brain...
:: Small delay to let the system breathe
timeout /t 2 /nobreak > nul

echo [SYSTEM] Leo is now live on the network.
".venv\Scripts\python.exe" -m uvicorn face:app --host 0.0.0.0 --port 8000 --reload

pause