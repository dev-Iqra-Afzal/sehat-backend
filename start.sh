#!/bin/bash
set -e

# Function to check if Docker is running
check_docker() {
  docker info > /dev/null 2>&1
  return $?
}

# Start Docker daemon if not running
if ! check_docker; then
  echo "Starting Docker daemon..."
  
  # Create a custom Docker daemon config to work around read-only file system issues
  mkdir -p /etc/docker
  cat > /etc/docker/daemon.json << EOL
{
  "userns-remap": "default",
  "storage-driver": "overlay2",
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
EOL

  # Try starting Docker with various methods
  echo "Attempting to start Docker daemon..."
  
  # Method 1: Using service command
  if command -v service > /dev/null 2>&1; then
    echo "Trying to start Docker using service command..."
    service docker start > /dev/null 2>&1 || echo "Service start failed, trying next method"
  fi
  
  # Method 2: Using systemctl
  if ! check_docker && command -v systemctl > /dev/null 2>&1; then
    echo "Trying to start Docker using systemctl..."
    systemctl start docker > /dev/null 2>&1 || echo "Systemctl start failed, trying next method"
  fi
  
  # Method 3: Direct dockerd with minimal options
  if ! check_docker; then
    echo "Trying to start Docker daemon directly..."
    mkdir -p /var/run/docker
    dockerd --host=unix:///var/run/docker.sock --data-root=/var/lib/docker --exec-root=/var/run/docker > /var/log/dockerd.log 2>&1 &
    
    # Wait for Docker to be available
    echo "Waiting for Docker daemon to start..."
    timeout=60
    until check_docker || [ $timeout -eq 0 ]; do
      sleep 2
      ((timeout-=2))
      echo "Waiting for Docker to start... ($timeout seconds left)"
    done
    
    if [ $timeout -eq 0 ]; then
      echo "Docker failed to start. Checking logs:"
      tail -n 50 /var/log/dockerd.log
      echo "Trying to run without Docker..."
      
      # Print environment for debugging
      echo "Environment:"
      env | grep -i docker
      
      # List processes
      echo "Running processes:"
      ps aux | grep docker
      
      # Run the fallback script
      echo "Attempting to run in fallback mode..."
      chmod +x /app/fallback.sh
      exec /app/fallback.sh
      exit 1
    fi
  fi
  
  echo "Docker daemon started successfully!"
fi

# Create a simple docker-compose.override.yml for Render
cat > docker-compose.override.yml << EOL
version: '3.8'
services:
  postgres:
    environment:
      - POSTGRES_HOST_AUTH_METHOD=trust
EOL

# Run database migrations
echo "Running database migrations..."
docker-compose up -d postgres rabbitmq
sleep 15  # Give the databases time to initialize

# Check if postgres is ready
echo "Checking if PostgreSQL is ready..."
docker-compose exec -T postgres pg_isready -U postgres || {
  echo "PostgreSQL is not ready yet. Waiting another 15 seconds..."
  sleep 15
  docker-compose exec -T postgres pg_isready -U postgres || {
    echo "PostgreSQL failed to start properly. Check logs."
    docker-compose logs postgres
    exit 1
  }
}

# Run migrations
echo "Running migrations..."
docker-compose up -d auth-service resource-service notification-service
sleep 10

# Run all services
echo "Starting all services..."
docker-compose up -d

# Follow logs
echo "All services started. Following gateway-service logs..."
docker-compose logs -f gateway-service
