# PowerShell script to run database migrations for all services

# Define services that use Alembic migrations (based on init.sql)
$services_with_migrations = @(
    @{Name = "auth-service"; DB = "auth_db"; User = "auth_user"; Password = "galadhrim154"},
    @{Name = "resource-service"; DB = "resource_db"; User = "resource_user"; Password = "galadhrim154"},
    @{Name = "notification-service"; DB = "notification_db"; User = "notification_user"; Password = "galadhrim154"}
)

# Check if PostgreSQL is installed and running
function Test-PostgreSQL {
    try {
        # PostgreSQL superuser credentials
        $pgUser = "postgres"
        $pgPassword = "galadhrim154"
        
        # Try to connect to PostgreSQL
        $env:PGPASSWORD = $pgPassword
        $result = & psql -U $pgUser -c "SELECT 1" postgres 2>&1
        if ($LASTEXITCODE -eq 0) {
            return $true
        }
        return $false
    }
    catch {
        return $false
    }
}

# Run migrations for a service
function Run-Migrations {
    param (
        [string]$serviceName,
        [string]$dbName,
        [string]$dbUser,
        [string]$dbPassword
    )
    
    $servicePath = ".\services\$serviceName"
    $venvPath = "$servicePath\venv"
    
    # Check if virtual environment exists
    if (-not (Test-Path $venvPath)) {
        Write-Host "Creating virtual environment for $serviceName..." -ForegroundColor Yellow
        python -m venv $venvPath
        
        # Install requirements
        Write-Host "Installing requirements for $serviceName..." -ForegroundColor Yellow
        & "$venvPath\Scripts\pip" install -r "$servicePath\requirements.txt"
    }
    
    # Ensure alembic is installed
    Write-Host "Ensuring alembic is installed in $serviceName virtual environment..." -ForegroundColor Yellow
    & "$venvPath\Scripts\pip" install alembic
    
    # Update alembic.ini with correct database URL
    $alembicIniPath = "$servicePath\alembic.ini"
    if (Test-Path $alembicIniPath) {
        $alembicContent = Get-Content $alembicIniPath -Raw
        $newDbUrl = "postgresql://$dbUser`:$dbPassword@localhost/$dbName"
        
        # Replace the database URL in alembic.ini
        $updatedContent = $alembicContent -replace "sqlalchemy.url = .*", "sqlalchemy.url = $newDbUrl"
        $updatedContent | Out-File -FilePath $alembicIniPath -Encoding utf8
        
        # Run migrations
        Write-Host "Running migrations for $serviceName..." -ForegroundColor Green
        $currentLocation = Get-Location
        # Set-Location $servicePath
        
        # Run alembic using the full path
        Write-Host "Running alembic upgrade head..." -ForegroundColor Green
        & "$venvPath\Scripts\python" -m alembic upgrade head
        
        # Return to original location
        Set-Location $currentLocation
    }
    else {
        Write-Host "No alembic.ini found for $serviceName. Skipping migrations." -ForegroundColor Yellow
    }
}

# Main script
Write-Host "Sehat-Iqra Database Migration Script" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan
Write-Host ""

# Check if PostgreSQL is installed and running
# if (-not (Test-PostgreSQL)) {
#     Write-Host "PostgreSQL is not installed or not running." -ForegroundColor Red
#     Write-Host "Please install PostgreSQL and make sure it's running before continuing." -ForegroundColor Red
#     exit 1
# }

# Generate service-specific .env files first
# if (Test-Path ".\generate_env_files.ps1") {
#     Write-Host "Generating service-specific .env files..." -ForegroundColor Yellow
#     & ".\generate_env_files.ps1"
# }

# Run migrations
foreach ($service in $services_with_migrations) {
    Write-Host ""
    Write-Host "Processing $($service.Name)..." -ForegroundColor Cyan
    
    # Run migrations
    Run-Migrations -serviceName $service.Name -dbName $service.DB -dbUser $service.User -dbPassword $service.Password
}

Write-Host ""
Write-Host "Database migrations completed!" -ForegroundColor Green