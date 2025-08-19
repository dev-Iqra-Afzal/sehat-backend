# Sehat-Iqra Backend

This is the backend for the Sehat-Iqra application, a healthcare platform that connects patients with hospitals, blood donors, and NGOs.

## Architecture

The backend is built using a microservices architecture with the following services:

- **Gateway Service**: API Gateway that routes requests to the appropriate service
- **Auth Service**: Handles user authentication and authorization
- **Hospital Service**: Manages hospital data and operations
- **Resource Service**: Manages hospital resources and availability
- **Blood Service**: Manages blood donation and requests
- **NGO Service**: Manages NGO data and operations
- **Notification Service**: Handles notifications to users
- **AI Service**: Provides AI-powered features

## Deployment on Render

### Prerequisites

1. A Render account
2. Git repository with this code

### Deployment Steps

1. Push your code to a Git repository (GitHub, GitLab, etc.)
2. Log in to your Render account
3. Click on "New" and select "Blueprint"
4. Connect your Git repository
5. Render will automatically detect the `render.yaml` file and create the necessary services
6. Set up the required environment variables:
   - `SECRET_KEY`: A secure secret key for JWT token generation
   - `OPENROUTER_API_KEY`: Your OpenRouter API key for AI services

### Manual Deployment

If you prefer to deploy manually:

1. Click on "New" and select "Web Service"
2. Connect your Git repository
3. Select "Docker" as the environment
4. Set the build command to `docker-compose build`
5. Set the start command to `./start.sh`
6. Add the required environment variables
7. Click "Create Web Service"

## Local Development

### Prerequisites

- Docker and Docker Compose
- PostgreSQL
- RabbitMQ

### Setup

1. Clone the repository
2. Create a `.env` file in the root directory with the required environment variables
3. Run the services:

```bash
docker-compose up
```

4. Access the API at http://localhost:8000

## API Documentation

Once the services are running, you can access the API documentation at:

- Gateway Service: http://localhost:8000/docs

## Environment Variables

The following environment variables are required:

- `SECRET_KEY`: Secret key for JWT token generation
- `OPENROUTER_API_KEY`: OpenRouter API key for AI services

## Database Migrations

Database migrations are handled automatically during deployment. If you need to run migrations manually:

```bash
docker-compose exec auth-service alembic upgrade head
docker-compose exec resource-service alembic upgrade head
docker-compose exec notification-service alembic upgrade head
```