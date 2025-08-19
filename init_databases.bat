@echo off
REM Batch script to initialize PostgreSQL databases for all services

echo ========================================================
echo Sehat-Iqra Database Initialization
echo ========================================================
echo.
echo This script will:
echo 1. Check if PostgreSQL is installed and running
echo 2. Create databases for each service if they don't exist
echo 3. Create database users for each service if they don't exist
echo 4. Grant necessary privileges to the database users
echo.

REM Check if PostgreSQL is installed
where psql >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: PostgreSQL is not installed or not in your PATH!
    echo Please install PostgreSQL and make sure the bin directory is in your PATH.
    echo.
    pause
    exit /b 1
)

echo Running PowerShell script to initialize databases...
powershell -ExecutionPolicy Bypass -File "%~dp0init_databases.ps1"

echo.
echo Database initialization completed.
echo.
pause
