@echo off
echo ==============================================
echo   Student Management System - Startup Script
echo ==============================================

REM Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Error: Python is not installed or not in your PATH.
    pause
    exit /b 1
)

echo [Step 1] Activating Virtual Environment...
IF EXIST "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) ELSE (
    echo Virtual environment not found. Creating one now...
    python -m venv venv
    call venv\Scripts\activate.bat
)

echo [Step 2] Installing Dependencies from requirements.txt...
pip install -r requirements.txt

echo [Step 3] Setting PYTHONPATH and Starting the Flask Application...
set PYTHONPATH=%cd%
python src\app.py

pause
