# SAI FastAPI

A FastAPI-based GraphQL API service with MongoDB integration.

## Features

- FastAPI with GraphQL support using Strawberry
- MongoDB database integration
- Docker and Docker Compose support
- Background jobs for calendar events and community check-ins
- RESTful API endpoints

## Prerequisites

- Python 3.9 or higher
- Docker and Docker Compose (for containerized deployment)
- MongoDB (if running locally)

## Project Structure

```
.
├── config/           # Configuration files
├── database/         # Database models and connections
├── graphql_utils/    # GraphQL type definitions
├── jobs/            # Background jobs
├── resolvers/       # GraphQL resolvers
├── service/         # Business logic services
├── utils/           # Utility functions
├── main.py          # Application entry point
├── schema.graphql   # GraphQL schema
└── requirements.txt # Python dependencies
```

## Getting Started

### Local Development

1. Create and activate a virtual environment:
```bash
pyenv virtualenv 3.11.8 sai-fast-api
pyenv activate sai-fast-api
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env  # Create and configure your .env file
```

4. Run the application:
```bash
uvicorn main:app --reload
```

### Docker Deployment

1. Build and start the services:
```bash
docker-compose up --build
```

2. For detached mode (background):
```bash
docker-compose up -d --build
```

3. Stop the services:
```bash
docker-compose down
```

4. View logs:
```bash
docker-compose logs -f
```

5. *Optional* - Run MongoDB locally:
```bash
docker-compose up -d mongodb
```

## API Endpoints

- GraphQL API: `http://localhost:8000/graphql`

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
MONGODB_URL=mongodb://localhost:27017
# Add other environment variables as needed
```

## Development

### Running Tests

```bash
pytest
```

### Code Style

This project follows PEP 8 guidelines. You can check your code style using:

```bash
flake8
```

### Background Jobs

The application includes two background jobs that run every 60 seconds:
- Calendar event push notifications
- Community check-in push notifications

## Docker Commands Reference

### Build and Run
```bash
# Build images
docker-compose build

# Start services
docker-compose up

# Start services in detached mode
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f
```

### Container Management
```bash
# List running containers
docker-compose ps

# Restart a service
docker-compose restart web

# Rebuild and restart a service
docker-compose up -d --build web
```

### Database Management
```bash
# Access MongoDB shell
docker-compose exec mongodb mongosh

# Backup database
docker-compose exec mongodb mongodump --out /backup
```

## Database Migration

This project has been migrated from MongoDB to PostgreSQL using SQLModel. Follow these steps to migrate your own data:

1. Install the new dependencies:
```bash
pip install -r requirements.txt
```

2. Configure your database connection:
   - Set the `DATABASE_URL` environment variable: `postgresql://postgres:postgres@localhost:5432/sai`
   - Or create a `.env` file with this variable

3. Initialize database migrations:
```bash
python migrate.py init
```

4. Run the application with the new PostgreSQL backend:
```bash
uvicorn main:app --reload
```

### Database Configuration

The database connection is configured using environment variables:
- `DATABASE_URL`: PostgreSQL connection string (default: `postgresql://postgres:postgres@localhost:5432/sai`)

### Using Docker with PostgreSQL

You can start a PostgreSQL instance using Docker:
```bash
docker-compose up -d postgres
```


## Database Migrations

The project uses Alembic for database migrations. The following commands are available:

### Initialize Migrations
```bash
python migrate.py init
```

### Create New Migration
```bash
python migrate.py create "Description of changes"
```

### Apply Migrations
```bash
python migrate.py upgrade
python migrate.py upgrade --revision abc123  # Specific revision
```

### Rollback Migrations
```bash
python migrate.py downgrade
python migrate.py downgrade --revision abc123  # Specific revision
```

### View Migration Status
```bash
python migrate.py history  # Show history
python migrate.py current  # Show current revision
```

### Migration Workflow
1. Make changes to models in database/models.py
2. Create migration: python migrate.py create "Description"
3. Review migration in alembic/versions/
4. Apply migration: python migrate.py upgrade
5. If needed, rollback: python migrate.py downgrade