# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A FastAPI-based GraphQL API service for a dog walking and community management application. The project uses Strawberry GraphQL, PostgreSQL with SQLModel, and Firebase authentication.

## Development Commands

### Running Locally
```bash
# Set up virtual environment
pyenv virtualenv 3.11.8 sai-fast-api
pyenv activate sai-fast-api

# Install dependencies
pip install -r requirements.txt

# Run development server (with hot reload)
uvicorn main:app --reload
```

### Docker

**Full stack with PostgreSQL (recommended):**
```bash
# Build and run (migrations run automatically via entrypoint.sh)
docker-compose -f docker-compose-with-database.yaml up --build

# Detached mode
docker-compose -f docker-compose-with-database.yaml up -d --build

# Stop services
docker-compose -f docker-compose-with-database.yaml down

# Clean start (remove volumes)
docker-compose -f docker-compose-with-database.yaml down -v

# View logs
docker-compose -f docker-compose-with-database.yaml logs -f
```

**Note:** The `entrypoint.sh` script automatically:
1. Waits for PostgreSQL to be ready
2. Runs database migrations (`python migrate.py upgrade`)
3. Starts the FastAPI application

**External database:**
```bash
# If using external PostgreSQL database
docker-compose up --build
```

### Database Migrations
```bash
# Initialize migrations (first time only)
python migrate.py init

# Create new migration after model changes
python migrate.py create "Description of changes"

# Apply migrations
python migrate.py upgrade

# Rollback migration
python migrate.py downgrade

# View migration status
python migrate.py current
python migrate.py history
```

### Testing
```bash
pytest  # No test suite currently exists
flake8  # Check code style
```

## Architecture

### Database Layer (PostgreSQL + SQLModel)

**Models** (`database/models.py`):
- All models inherit from `UUID` base class with UUID primary keys
- Models include a `to_graphQL()` method that converts SQLModel instances to Strawberry GraphQL types
- Key models: `User`, `Dog`, `Community`, `CommunityMember`, `CommunityPlace`, `Walk`, `WalkInterval`, `CalendarEvent`
- Many-to-many relationships use explicit link tables (e.g., `UserDog`)
- Walk model includes distance/speed calculation methods using haversine formula

**Database Connection** (`config/database.py`):
- Connection via `DATABASE_URL` env var (default: `postgresql://postgres:postgres@localhost:5432/sai`)
- SQLModel engine with echo=True for SQL logging
- `get_session()` context manager handles commit/rollback automatically
- `init_db()` is called on FastAPI startup (currently commented out for table creation)

### GraphQL Layer (Strawberry)

**Schema Definition** (`main.py`):
- Single `Query` and `Mutation` root types
- Custom `DateTimeScalar` for datetime handling
- Context-based dependency injection for database sessions and authentication

**Type Definitions** (`graphql_utils/`):
- GraphQL types are defined separately from SQLModel models
- Each domain has its own type file: `user.py`, `dog.py`, `community.py`, `walk.py`, `calendar_event.py`
- Input types use `@strawberry.input` decorator (e.g., `CreateDogInput`, `UpdateDogInput`)

**Resolvers** (`resolvers/`):
- All resolvers are async functions
- Each resolver receives `info: Info` parameter containing context (session, user)
- Authentication checked via `check_authentication(info)` helper
- Session management happens through `info.context.session`
- Pattern: authenticate → query/modify data → commit → return GraphQL type

### Authentication (`config/authentication.py`)

**Context System**:
- `Context` class extends `BaseContext` and manages database session lifecycle
- `user` property is a cached property that:
  - If `SKIP_AUTH=True`: returns default user (`dev@example.com`)
  - Otherwise: verifies Firebase token from `Authorization` header
  - Queries user from database by email
- `check_authentication()` helper raises exception if user not authenticated

**Important**: `SKIP_AUTH` flag currently set to `True` for development

### Background Jobs

**Structure** (`jobs/`):
- `calendar_event_job.py`: Push notifications for calendar events
- `community_checkin_job.py`: Push notifications for community check-ins
- Jobs currently commented out in `main.py` startup events

**Pattern**: Jobs use `@repeat_every(seconds=60)` decorator from fastapi-utils

## Key Patterns

### Adding a New Entity

1. **Define SQLModel** in `database/models.py`:
   - Inherit from `UUID` for standard ID
   - Add relationships using `Relationship()`
   - Implement `to_graphQL()` method

2. **Define GraphQL types** in `graphql_utils/[entity].py`:
   - Create `@strawberry.type` for the entity
   - Create `@strawberry.input` for mutations

3. **Create resolvers** in `resolvers/[entity].py`:
   - All resolvers are async
   - Use `check_authentication(info)` for protected operations
   - Access session via `info.context.session`
   - Commit changes before returning

4. **Register in schema** (`main.py`):
   - Add queries to `Query` class
   - Add mutations to `Mutation` class
   - Import resolver functions

5. **Create migration**:
   ```bash
   python migrate.py create "Add [entity] model"
   python migrate.py upgrade
   ```

### Database Session Management

The Context class manages sessions:
- Session created lazily on first access via `info.context.session`
- Auto-commit on successful response
- Auto-rollback on exceptions
- Manual commits needed for intermediate operations

### Working with Relationships

When querying relationships:
- SQLModel doesn't auto-eager load by default
- Access relationships directly (e.g., `user.dogs`) - SQLModel will lazy load
- For complex queries, use explicit joins with SQLModel `select()` and `.join()`
- Refresh entities after commits to get updated relationship data: `session.refresh(entity)`

## Environment Variables

Required variables (create `.env` file):
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/sai
```

Firebase credentials are loaded from: `config/sai-ios-firebase-adminsdk-dmgtl-2dcabece02.json`

## API Access

- GraphQL endpoint: `http://localhost:3000/graphql`
- GraphQL playground available at the same URL
- Local dev runs on port 3000 (default uvicorn)
- Docker (with-database) exposes port 3000 (mapped 3000:3000)
