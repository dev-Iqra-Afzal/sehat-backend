#!/bin/bash
set -e

echo "Running in fallback mode - starting gateway service directly"

# Install requirements for gateway service
echo "Current directory: $PWD"
cd ./services/gateway-service
echo "Current directory: $PWD"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set environment variables
export ENVIRONMENT=production
export API_V1_STR=/api/v1
export AUTH_SERVICE_URL=https://sehat-iqra-auth.onrender.com
export HOSPITAL_SERVICE_URL=https://sehat-iqra-hospital.onrender.com
export RESOURCE_SERVICE_URL=https://sehat-iqra-resource.onrender.com
export BLOOD_SERVICE_URL=https://sehat-iqra-blood.onrender.com
export NGO_SERVICE_URL=https://sehat-iqra-ngo.onrender.com
export NOTIFICATION_SERVICE_URL=https://sehat-iqra-notification.onrender.com
export AI_SERVICE_URL=https://sehat-iqra-ai.onrender.com

# Start the gateway service
echo "Starting gateway service..."
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
