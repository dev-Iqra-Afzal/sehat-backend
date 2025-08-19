@echo off
REM Batch script to generate service-specific .env files from the master .env file

echo ========================================================
echo Sehat-Iqra Environment File Generator
echo ========================================================
echo.
echo This script will:
echo 1. Read the .env-master file
echo 2. Generate service-specific .env files for each service
echo.

if not exist ".env-master" (
    echo ERROR: Master .env file not found!
    echo Please create .env-master file in the sehat-backend directory first.
    echo.
    pause
    exit /b 1
)

echo Running PowerShell script to generate .env files...
powershell -ExecutionPolicy Bypass -File "%~dp0generate_env_files.ps1"

echo.
echo All service-specific .env files have been generated.
echo.
pause
