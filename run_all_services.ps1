# PowerShell script to run all Sehat-Iqra backend services without Docker

# Define services and their ports
$services = @(
    @{Name = "gateway-service"; Port = 8000},
    @{Name = "auth-service"; Port = 8001},
    @{Name = "hospital-service"; Port = 8002},
    @{Name = "resource-service"; Port = 8003},
    @{Name = "blood-service"; Port = 8004},
    @{Name = "ngo-service"; Port = 8005},
    @{Name = "notification-service"; Port = 8007},
    @{Name = "ai-service"; Port = 8008}
)

# Check if master .env file exists
# $masterEnvPath = ".\.env-master"
# if (-not (Test-Path $masterEnvPath)) {
#     Write-Host "Error: Master .env file not found at $masterEnvPath" -ForegroundColor Red
#     Write-Host "Please create the master .env file first."
#     exit 1
# }

# Generate service-specific .env files
# Write-Host "Generating service-specific .env files..." -ForegroundColor Green
# & ".\generate_env_files.ps1"

# Function to create and activate a virtual environment
function Setup-VirtualEnv {
    param (
        [string]$serviceName
    )
    
    $servicePath = ".\services\$serviceName"
    $venvPath = "$servicePath\venv"
    
    # Create virtual environment if it doesn't exist
    # if (-not (Test-Path $venvPath)) {
    #     Write-Host "Creating virtual environment for $serviceName..."
    #     python -m venv $venvPath
    # }
    
    # Activate virtual environment and install requirements
    Write-Host "Installing requirements for $serviceName..."
    # & "$venvPath\Scripts\pip" install -r "$servicePath\requirements.txt"
    
    return $venvPath
}

# Function to start a service
function Start-Service {
    param (
        [string]$serviceName,
        [int]$port
    )
    
    $servicePath = ".\services\$serviceName"
    
    # Start the service
    Write-Host "Starting $serviceName on port $port..."
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$servicePath'; & 'venv\Scripts\activate'; uvicorn app.main:app --host 0.0.0.0 --port $port --reload"
}

# Setup and start each service
foreach ($service in $services) {
    $venvPath = Setup-VirtualEnv -serviceName $service.Name
    Start-Service -serviceName $service.Name -port $service.Port
    
    # Wait a bit between starting services
    Start-Sleep -Seconds 2
}

Write-Host "All services started. Access the gateway at http://localhost:8000" -ForegroundColor Green