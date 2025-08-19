#!/bin/bash
set -e

# Start Docker daemon if not running
if ! docker info > /dev/null 2>&1; then
  echo "Starting Docker daemon..."
  # Modify the Docker service file to remove problematic ulimit settings
  if [ -f "/etc/init.d/docker" ]; then
    sed -i 's/ulimit -n.*/# ulimit call removed/' /etc/init.d/docker
    sed -i 's/ulimit -l.*/# ulimit call removed/' /etc/init.d/docker
  fi
  
  # Try starting Docker service
  service docker start || {
    echo "Could not start Docker service. Trying alternative method..."
    # Alternative: Start dockerd directly
    dockerd > /var/log/dockerd.log 2>&1 &
    # Wait for Docker to be available
    timeout=30
    until docker info > /dev/null 2>&1 || [ $timeout -eq 0 ]; do
      sleep 1
      ((timeout--))
      echo "Waiting for Docker to start... ($timeout seconds left)"
    done
    
    if [ $timeout -eq 0 ]; then
      echo "Docker failed to start. Check logs at /var/log/dockerd.log"
      exit 1
    fi
  }
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
