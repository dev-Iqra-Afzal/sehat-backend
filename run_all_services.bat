@echo off
REM Batch script to run all Sehat-Iqra backend services without Docker

echo ========================================================
echo Sehat-Iqra Backend Services Launcher
echo ========================================================
echo.
echo This script will:
echo 1. Copy the master .env file to each service
echo 2. Create Python virtual environments for each service
echo 3. Install dependencies for each service
echo 4. Start all services in separate terminal windows
echo.

if not exist ".env-master" (
    echo ERROR: Master .env file not found!
    echo Please create .env-master file in the sehat-backend directory first.
    echo.
    pause
    exit /b 1
)

echo Running PowerShell script to start all services...
powershell -ExecutionPolicy Bypass -File "%~dp0run_all_services.ps1"

echo.
echo All services should be starting in separate windows.
echo Access the gateway at http://localhost:8000
echo.
pause