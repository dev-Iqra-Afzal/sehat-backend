# PowerShell script to initialize PostgreSQL databases for all services

# Define services and their database settings based on init.sql
$services = @(
    @{Name = "auth-service"; DB = "auth_db"; User = "auth_user"; Password = "galadhrim154"},
    @{Name = "resource-service"; DB = "resource_db"; User = "resource_user"; Password = "galadhrim154"},
    @{Name = "notification-service"; DB = "notification_db"; User = "notification_user"; Password = "galadhrim154"}
)

# Check if PostgreSQL is installed and running
function Test-PostgreSQL {
    try {
        # PostgreSQL superuser credentials
        $pgUser = "postgres"
        $pgPassword = "postgres"
        
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

# Create database if it doesn't exist
function Create-Database {
    param (
        [string]$dbName,
        [string]$dbUser,
        [string]$dbPassword
    )
    
    Write-Host "Checking if database $dbName exists..." -ForegroundColor Yellow
    
    # PostgreSQL superuser credentials
    $pgUser = "postgres"
    $pgPassword = "galadhrim154"
    
    # Check if database exists
    $env:PGPASSWORD = $pgPassword
    $dbExists = & psql -U $pgUser -c "SELECT 1 FROM pg_database WHERE datname = '$dbName'" postgres
    
    if ($dbExists -notcontains " 1") {
        Write-Host "Creating database $dbName..." -ForegroundColor Green
        & psql -U $pgUser -c "CREATE DATABASE $dbName;" postgres
        
        # Check if user exists
        $userExists = & psql -U $pgUser -c "SELECT 1 FROM pg_roles WHERE rolname = '$dbUser'" postgres
        
        if ($userExists -notcontains " 1") {
            Write-Host "Creating user $dbUser..." -ForegroundColor Green
            & psql -U $pgUser -c "CREATE USER $dbUser WITH ENCRYPTED PASSWORD '$dbPassword';" postgres
        }
        
        # Grant privileges
        Write-Host "Granting privileges to $dbUser on $dbName..." -ForegroundColor Green
        & psql -U $pgUser -c "GRANT ALL PRIVILEGES ON DATABASE $dbName TO $dbUser;" postgres
        & psql -U $pgUser -c "ALTER USER $dbUser WITH SUPERUSER;" postgres
    }
    else {
        Write-Host "Database $dbName already exists." -ForegroundColor Green
    }
}

# Main script
Write-Host "Sehat-Iqra Database Initialization Script" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Creating only the databases mentioned in postgres-init/init.sql" -ForegroundColor Cyan
Write-Host ""

# Check if PostgreSQL is installed and running
# if (-not (Test-PostgreSQL)) {
#     Write-Host "PostgreSQL is not installed or not running." -ForegroundColor Red
#     Write-Host "Please install PostgreSQL and make sure it's running before continuing." -ForegroundColor Red
#     exit 1
# }

# Create databases for each service
foreach ($service in $services) {
    Write-Host ""
    Write-Host "Processing $($service.Name)..." -ForegroundColor Cyan
    
    # Create database if it doesn't exist
    Create-Database -dbName $service.DB -dbUser $service.User -dbPassword $service.Password
}

Write-Host ""
Write-Host "Database initialization completed!" -ForegroundColor Green