#!/bin/bash
set -e

# Start Docker daemon if not running
if ! docker info > /dev/null 2>&1; then
  echo "Starting Docker daemon..."
  service docker start
fi

# Run database migrations
echo "Running database migrations..."
docker-compose up -d postgres rabbitmq
sleep 10  # Give the databases time to initialize

# Run all services
echo "Starting all services..."
docker-compose up --build

# Keep the container running
tail -f /dev/null
