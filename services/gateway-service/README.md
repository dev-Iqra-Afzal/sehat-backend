# Gateway Service for Sehat-Iqra

This service acts as an API Gateway for all the microservices in the Sehat-Iqra backend.

## Features

- Single entry point for all API requests
- Route requests to appropriate microservices
- Consistent API structure with versioning
- Centralized CORS handling

## Setup

1. Copy the `.env-example` file to `.env`:
   ```
   cp .env-example .env
   ```

2. Update the service URLs in the `.env` file if needed.

## API Endpoints

All services are accessible through the gateway with the following URL structure:

- Auth Service: `/api/v1/auth/*`
- Hospital Service: `/api/v1/hospital/*`
- Resource Service: `/api/v1/resource/*`
- Blood Service: `/api/v1/blood/*`
- NGO Service: `/api/v1/ngo/*`
- Notification Service: `/api/v1/notification/*`
- AI Service: `/api/v1/ai/*`

## Development

To run this service locally:

```bash
uvicorn app.main:app --reload
```

## Docker

This service is included in the main docker-compose.yml file and will be started along with other services.
