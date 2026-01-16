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
uvicorn main:app --reload --port 3000
```

### Docker

**Full stack with PostgreSQL (recommended for testing):**
```bash
docker-compose -f docker-compose-with-database.yaml up --build

# Migrations run automatically via entrypoint.sh
# Stop: docker-compose -f docker-compose-with-database.yaml down
# Clean start: docker-compose -f docker-compose-with-database.yaml down -v
```

**External database (production):**
```bash
docker-compose up --build
```

### Database Migrations
```bash
python migrate.py init              # First time only
python migrate.py create "message"  # Create migration after model changes
python migrate.py upgrade           # Apply migrations
python migrate.py downgrade         # Rollback
python migrate.py current           # View current revision
python migrate.py history           # View history
```

## Architecture

### Database Layer (PostgreSQL + SQLModel)

**Models** (`database/models.py`):
- All models inherit from `UUID` base class with UUID primary keys
- Models include a `to_graphQL()` method that converts SQLModel instances to Strawberry GraphQL types
- Key models: `User`, `Dog`, `Community`, `CommunityMember`, `CommunityPlace`, `Walk`, `WalkInterval`, `CalendarEvent`
- Many-to-many relationships use explicit link tables (e.g., `UserDog`)
- **Important**: Models with forward references must call `Model.model_rebuild()` at end of file

**Database Connection** (`config/database.py`):
- Connection via `DATABASE_URL` env var (default: `postgresql://postgres:postgres@localhost:5432/sai`)
- SQLModel engine with echo=True for SQL logging

### GraphQL Layer (Strawberry)

**Type Definitions** (`graphql_utils/`):
- GraphQL types are defined separately from SQLModel models
- Each domain has its own type file: `user.py`, `dog.py`, `community.py`, `walk.py`, `calendar_event.py`
- **Typed Info**: Use `Info` from `graphql_utils/types.py` (typed alias with Context)

**Resolvers** (`resolvers/`):
- All resolvers are async functions with signature: `async def resolver(self, info: Info, ...) -> Type`
- **Note**: `self` parameter is required for Strawberry field resolvers even though unused
- Authentication: `user = await check_authentication(info)`
- Session access: `info.context.session`
- Pattern: authenticate → query/modify → commit → return `model.to_graphQL()`

### Authentication (`config/authentication.py`)

- `Context` class manages database session lifecycle and user authentication
- `SKIP_AUTH = True` for development (uses default user `dev@example.com`)
- Production: verifies Firebase token from `Authorization` header
- `check_authentication(info)` helper raises exception if user not authenticated

### Background Jobs (`jobs/`)

- `calendar_event_job.py`, `community_checkin_job.py`: Push notification jobs
- Currently commented out in `main.py`
- Pattern: `@repeat_every(seconds=60)` decorator from fastapi-utils

## Key Patterns

### Adding a New Entity

1. **SQLModel** (`database/models.py`): Inherit from `UUID`, add `Relationship()`, implement `to_graphQL()`, add `Model.model_rebuild()` at end
2. **GraphQL types** (`graphql_utils/[entity].py`): `@strawberry.type` and `@strawberry.input`
3. **Resolvers** (`resolvers/[entity].py`): async functions with `self` and `info: Info` params
4. **Register** (`main.py`): Add to `Query`/`Mutation` classes with `strawberry.field(resolver=...)`
5. **Migration**: `python migrate.py create "Add [entity]" && python migrate.py upgrade`

### Session Management

- Session created lazily via `info.context.session`
- Auto-commit on success, auto-rollback on exception
- Call `session.commit()` for intermediate operations
- Call `session.refresh(entity)` after commit to get updated relationship data

## Environment Variables

```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/sai
```

Firebase credentials: `config/sai-ios-firebase-adminsdk-dmgtl-2dcabece02.json`

## API Access

- GraphQL endpoint: `http://localhost:3000/graphql`
- GraphQL playground available at the same URL
