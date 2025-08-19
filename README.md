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

There are two deployment options available:

### Option 1: Docker-in-Docker (All-in-One Container)

This approach runs all services in a single container using Docker-in-Docker.

#### Prerequisites

1. A Render account
2. Git repository with this code

#### Deployment Steps

1. Push your code to a Git repository (GitHub, GitLab, etc.)
2. Log in to your Render account
3. Click on "New" and select "Blueprint"
4. Connect your Git repository
5. Render will automatically detect the `render.yaml` file and create the necessary services
6. Set up the required environment variables:
   - `SECRET_KEY`: A secure secret key for JWT token generation
   - `OPENROUTER_API_KEY`: Your OpenRouter API key for AI services

### Option 2: Separate Services (Alternative Approach)

This approach deploys each service separately, with a managed PostgreSQL database.

#### Deployment Steps

1. Rename `render.yaml.alternative` to `render.yaml` (or use it directly)
2. Push your code to a Git repository
3. Log in to your Render account
4. Click on "New" and select "Blueprint"
5. Connect your Git repository
6. Select the alternative render.yaml file
7. Render will create all the necessary services

## Local Development

### Prerequisites

- Docker and Docker Compose
- PostgreSQL
- RabbitMQ

### Setup

1. Clone the repository
2. Create a `.env` file in the root directory with the required environment variables (see `.env-example`)
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

## Troubleshooting Deployment

### Docker-in-Docker Issues

If you encounter issues with the Docker-in-Docker approach:

1. Check the logs in the Render dashboard
2. The deployment includes a fallback mode that will automatically run just the gateway service if Docker fails to start
3. Consider using the alternative deployment approach (Option 2)
4. Make sure your Render account has the necessary permissions and plan

### Fallback Mode

The deployment includes a fallback mode that will automatically activate if Docker fails to start:

1. Only the gateway service will run directly (without Docker)
2. The gateway will be configured to connect to other services deployed separately
3. You'll need to deploy the other services separately using Option 2

### Database Connection Issues

If services can't connect to the database:

1. Check the database connection string in the environment variables
2. Ensure the database is running and accessible
3. Check if the database migrations have run successfully

### RabbitMQ Issues

If services can't connect to RabbitMQ:

1. Check the RabbitMQ connection settings
2. Ensure RabbitMQ is running and accessible
3. Check if the queues have been created correctly