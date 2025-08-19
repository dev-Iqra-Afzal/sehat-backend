# PowerShell script to generate service-specific .env files from the master .env file
# This script reads the .env-master file and creates customized .env files for each service

# Define services and their prefixes
$services = @(
    @{Name = "gateway-service"; Prefix = "GATEWAY"},
    @{Name = "auth-service"; Prefix = "AUTH"},
    @{Name = "hospital-service"; Prefix = "HOSPITAL"},
    @{Name = "resource-service"; Prefix = "RESOURCE"},
    @{Name = "blood-service"; Prefix = "BLOOD"},
    @{Name = "ngo-service"; Prefix = "NGO"},
    @{Name = "notification-service"; Prefix = "NOTIFICATION"},
    @{Name = "ai-service"; Prefix = "AI"}
)

# Check if master .env file exists
$masterEnvPath = ".\.env-master"
if (-not (Test-Path $masterEnvPath)) {
    Write-Host "Error: Master .env file not found at $masterEnvPath" -ForegroundColor Red
    Write-Host "Please create the master .env file first."
    exit 1
}

# Read the master .env file
$masterEnvContent = Get-Content $masterEnvPath -Raw
$masterEnvLines = Get-Content $masterEnvPath

# Function to extract value from the master .env file
function Get-EnvValue {
    param (
        [string]$key
    )
    
    foreach ($line in $masterEnvLines) {
        if ($line -match "^$key=(.*)$") {
            return $matches[1]
        }
    }
    
    return $null
}

# Create service-specific .env files
Write-Host "Creating service-specific .env files..." -ForegroundColor Green
foreach ($service in $services) {
    $serviceEnvPath = ".\services\$($service.Name)\.env"
    $servicePrefix = $service.Prefix
    
    Write-Host "Creating .env file for $($service.Name)..."
    
    # Common environment variables for all services
    $envContent = @"
# Generated from .env-master for $($service.Name)
# =============================================
# Common Settings
# =============================================
ENVIRONMENT=$(Get-EnvValue "ENVIRONMENT")
SECRET_KEY=$(Get-EnvValue "SECRET_KEY")
ALGORITHM=$(Get-EnvValue "ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES=$(Get-EnvValue "ACCESS_TOKEN_EXPIRE_MINUTES")
REFRESH_TOKEN_EXPIRE_DAYS=$(Get-EnvValue "REFRESH_TOKEN_EXPIRE_DAYS")

"@

    # Add service-specific settings
    if ($service.Name -eq "gateway-service") {
        # Gateway service needs all service URLs
        $envContent += @"
# =============================================
# Gateway Service Settings
# =============================================
APP_NAME=$(Get-EnvValue "GATEWAY_APP_NAME")
PROJECT_NAME=$(Get-EnvValue "GATEWAY_APP_NAME")
API_V1_STR=$(Get-EnvValue "API_V1_STR")

# Service URLs
AUTH_SERVICE_URL=$(Get-EnvValue "AUTH_SERVICE_URL")
HOSPITAL_SERVICE_URL=$(Get-EnvValue "HOSPITAL_SERVICE_URL")
RESOURCE_SERVICE_URL=$(Get-EnvValue "RESOURCE_SERVICE_URL")
BLOOD_SERVICE_URL=$(Get-EnvValue "BLOOD_SERVICE_URL")
NGO_SERVICE_URL=$(Get-EnvValue "NGO_SERVICE_URL")
NOTIFICATION_SERVICE_URL=$(Get-EnvValue "NOTIFICATION_SERVICE_URL")
AI_SERVICE_URL=$(Get-EnvValue "AI_SERVICE_URL")

# CORS settings
BACKEND_CORS_ORIGINS=$(Get-EnvValue "BACKEND_CORS_ORIGINS")
"@
    }
    else {
        # For other services, include their specific app and database settings
        $envContent += @"
# =============================================
# $($service.Name) Settings
# =============================================
# App Settings
APP_NAME=$(Get-EnvValue "$($servicePrefix)_APP_NAME")
APP_DESCRIPTION=$(Get-EnvValue "$($servicePrefix)_APP_DESCRIPTION")
APP_VERSION=$(Get-EnvValue "APP_VERSION")
LICENSE=$(Get-EnvValue "LICENSE")
CONTACT_NAME=$(Get-EnvValue "CONTACT_NAME")
CONTACT_EMAIL=$(Get-EnvValue "CONTACT_EMAIL")

# Database Settings
POSTGRES_USER=$(Get-EnvValue "$($servicePrefix)_POSTGRES_USER")
POSTGRES_PASSWORD=$(Get-EnvValue "$($servicePrefix)_POSTGRES_PASSWORD")
POSTGRES_SERVER=$(Get-EnvValue "POSTGRES_SERVER")
POSTGRES_PORT=$(Get-EnvValue "POSTGRES_PORT")
POSTGRES_DB=$(Get-EnvValue "$($servicePrefix)_POSTGRES_DB")
POSTGRES_SYNC_PREFIX=$(Get-EnvValue "POSTGRES_SYNC_PREFIX")
POSTGRES_ASYNC_PREFIX=$(Get-EnvValue "POSTGRES_ASYNC_PREFIX")
POSTGRES_URL=$(Get-EnvValue "$($servicePrefix)_POSTGRES_URL")

# Redis Settings
REDIS_CACHE_HOST=$(Get-EnvValue "REDIS_CACHE_HOST")
REDIS_CACHE_PORT=$(Get-EnvValue "REDIS_CACHE_PORT")
REDIS_QUEUE_HOST=$(Get-EnvValue "REDIS_QUEUE_HOST")
REDIS_QUEUE_PORT=$(Get-EnvValue "REDIS_QUEUE_PORT")
"@

        # Add AI-specific settings
        if ($service.Name -eq "ai-service") {
            $envContent += @"

# AI API Keys
OPENROUTER_API_KEY=$(Get-EnvValue "OPENROUTER_API_KEY")
HF_API_KEY=$(Get-EnvValue "HF_API_KEY")
HF_MODEL=$(Get-EnvValue "HF_MODEL")
GROQ_API_KEY=$(Get-EnvValue "GROQ_API_KEY")
"@
        }
    }

    # Write the service-specific .env file
    $envContent | Out-File -FilePath $serviceEnvPath -Encoding utf8
    Write-Host "Created .env file for $($service.Name)" -ForegroundColor Green
}

Write-Host "All service-specific .env files have been generated successfully!" -ForegroundColor Green
