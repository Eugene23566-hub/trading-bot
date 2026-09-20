@echo off
setlocal
cd /d C:\CryptoAnalyst
if not exist ".venv\Scripts\python.exe" exit /b 2
".venv\Scripts\python.exe" run_cycle.py >> "C:\CryptoAnalyst\state\scheduler.log" 2>&1
