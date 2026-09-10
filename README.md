# sai-fastapi

GraphQL backend for [sai](https://github.com/nickspopov/sai-ios), a dog walking & pet care iOS app. FastAPI + Strawberry GraphQL + SQLModel on PostgreSQL, Firebase for auth and push, Alembic migrations, Docker. Started in August 2023 (originally on MongoDB/Motor, migrated to Postgres in 2025).

## What's in it

- **Schema-first GraphQL** — `schema.graphql` is the contract shared with the iOS client (Apollo codegen reads it); Strawberry types are mapped from SQLModel models via `to_graphQL()`.
- **Walks** — the client uploads raw GPS intervals; the server computes distance (haversine over consecutive points), duration, average speed and pace. `getWalkIntervalActivityByDay(fromDate, toDate)` aggregates per day in one query so the app's today/week/month/year stats don't fetch every walk.
- **Calendar events** — typed pet care events (walking, food, pills, grooming, vet, other) with a job table (`CalendarEventJob`) for scheduled push notifications.
- **Communities** — places + members with periodic check-in jobs (`CommunityCheckinJob`).
- **Auth** — Firebase ID token verified per request in the Strawberry context; `SKIP_AUTH=true` swaps in a fixed dev user for local work without Firebase.
- **Push** — FCM multicast via `firebase-admin` (`service/notifications.py`).
- **Ops** — `/health` and `/ready` (DB ping) endpoints, `entrypoint.sh` waits for Postgres and runs migrations, ruff + pre-commit.

## Run

Full stack (Postgres + API on `:3000`, migrations run on start):

```bash
docker compose -f docker-compose-with-database.yaml up --build
```

Local:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
cp .env.example .env            # set DATABASE_URL, SKIP_AUTH=true, DEFAULT_DEV_USER_EMAIL
python migrate.py upgrade
uvicorn main:app --reload       # GraphiQL at http://localhost:8000/graphql
```

The default user for `SKIP_AUTH` is created by migration `bfb8d5639915`; set `DEFAULT_DEV_USER_EMAIL` to its email.

Firebase: put a service-account JSON at `FIREBASE_CREDENTIALS_PATH` (default `./config/firebase-credentials.json`, gitignored). Required unless `SKIP_AUTH=true`.

## Layout

```
main.py             FastAPI app, GraphQL router, health endpoints, background job hooks
schema.graphql      GraphQL schema (source of truth for the iOS client)
graphql_utils/      Strawberry types, inputs, enums
resolvers/          user, walks, calendar_event, places
database/models.py  SQLModel tables: User, Dog, Walk, WalkInterval, CalendarEvent, Community, jobs
config/             database engine, authentication context (Firebase)
service/            push notifications
jobs/               calendar event + community check-in push jobs
alembic/            migrations (python migrate.py upgrade|downgrade|revision)
```

## Migrations

```bash
python migrate.py revision "add something"   # autogenerate
python migrate.py upgrade
```

## License

MIT © Nick Popov
