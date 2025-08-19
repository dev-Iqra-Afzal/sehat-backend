@echo off
REM Batch script to run database migrations for all services

echo ========================================================
echo Sehat-Iqra Database Migration Runner
echo ========================================================
echo.
echo This script will:
echo 1. Check if PostgreSQL is installed and running
echo 2. Create databases for each service if they don't exist
echo 3. Run database migrations using Alembic
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

echo Running PowerShell script to run migrations...
powershell -ExecutionPolicy Bypass -File "%~dp0run_migrations.ps1"

echo.
echo Database migrations completed.
echo.
pause
