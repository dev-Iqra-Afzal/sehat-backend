#!/bin/bash
set -e

# Function to check if Docker is running
check_docker() {
  docker info > /dev/null 2>&1
  return $?
}

# If Docker isn't available, fall back to running the gateway directly
if ! check_docker; then
  echo "Docker not detected. Running in fallback mode."
  exec /app/fallback.sh
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
