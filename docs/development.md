# Loyalty Points System - Docker Setup

This document provides instructions for setting up and running the Loyalty Points System using Docker.

## Prerequisites

Before you begin, ensure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Project Structure

The application consists of multiple services:

- **loyalty_web**: Django web application
- **loyalty_celery**: Background task processor
- **loyalty_flower**: Celery monitoring tool
- **loyalty_db**: PostgreSQL database (includes main and warehouse databases)
- **loyalty_redis**: Redis for message broker

## Setup and Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd django-loyalty-points-app
```

### 2. Environment Setup (Optional)

You may need to create an `.env` file for environment variables if not already included.

### 3. Build and Start the Containers

```bash
docker-compose up -d
```

This command will:
- Build the necessary Docker images
- Create and start all the containers defined in the `docker-compose.yml` file
- Set up the volumes for data persistence
- Initialize the database with any required SQL scripts

### 4. Run Database Migrations

Since this is a Django application, you'll need to run migrations:

```bash
docker-compose exec loyalty_web python manage.py migrate
```

### 5. Create an Admin User (Optional)

```bash
docker-compose exec loyalty_web python manage.py createsuperuser
```

## Accessing the Application

- **Web Application**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **API Documentation**: http://localhost:8000/swagger/
- **Celery Monitoring (Flower)**: http://localhost:5555

## Running Tests

To run the test suite within the Docker environment:

```bash
# Run all tests
docker-compose exec loyalty_web pytest

# Run with coverage report
docker-compose exec loyalty_web pytest --cov=. --cov-report=html

# Run tests for a specific app
docker-compose exec loyalty_web pytest points/
```

## Common Commands

### View Logs

```bash
# View logs for all services
docker-compose logs

# View logs for a specific service
docker-compose logs loyalty_web

# Follow logs in real-time
docker-compose logs -f
```

### Restart Services

```bash
# Restart a single service
docker-compose restart loyalty_web

# Restart all services
docker-compose restart
```

### Stop and Remove Containers

```bash
# Stop all containers
docker-compose stop

# Stop and remove containers (preserves volumes)
docker-compose down

# Stop and remove containers, networks, and volumes
docker-compose down -v
```

### Database Management

```bash
# Connect to the PostgreSQL database
docker-compose exec loyalty_db psql -U loyalty_user -d loyalty_db

# Connect to the Warehouse database
docker-compose exec loyalty_db psql -U loyalty_user -d warehouse_db

# Backup the database
docker-compose exec loyalty_db pg_dump -U loyalty_user loyalty_db > backup.sql
```

## Troubleshooting

### Database Connection Issues

If the application can't connect to the database:

1. Ensure the database container is running:
   ```bash
   docker-compose ps loyalty_db
   ```

2. Check if the database was properly initialized:
   ```bash
   docker-compose logs loyalty_db
   ```

3. Try reconnecting to the database manually:
   ```bash
   docker-compose exec loyalty_db psql -U loyalty_user -d loyalty_db
   ```

### Web Application Not Responding

1. Check the web application logs:
   ```bash
   docker-compose logs loyalty_web
   ```

2. Restart the web service:
   ```bash
   docker-compose restart loyalty_web
   ```

### Celery Workers Not Processing Tasks

1. Check the Celery logs:
   ```bash
   docker-compose logs loyalty_celery
   ```

2. Ensure Redis is running:
   ```bash
   docker-compose ps loyalty_redis
   ```

3. Monitor tasks through Flower:
   - Open http://localhost:5555 in your browser

## Development Workflow

### Making Code Changes

1. Edit files on your local machine
2. Changes will be reflected in the running containers thanks to volume mounting
3. For certain changes (like adding new dependencies), you may need to rebuild:
   ```bash
   docker-compose build
   docker-compose up -d
   ```

### Adding Dependencies

If you add dependencies to `requirements.txt`:

```bash
docker-compose build
docker-compose up -d
```