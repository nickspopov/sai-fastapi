# GraphQL
from datetime import datetime

# Utils
import strawberry

# FastAPI
from fastapi import FastAPI, Response
from strawberry.fastapi import GraphQLRouter

from config.authentication import Context
from config.database import init_db
from graphql_utils.calendar_event import CalendarEventType
from graphql_utils.community import CommunityType
from graphql_utils.dog import DogType
from graphql_utils.user import UserType
from graphql_utils.walk import WalkDayActivity, WalkIntervalActivity, WalkType
from resolvers.calendar_event import create_event_resolver, get_event_resolver, get_events_resolver
from resolvers.places import (
    checkin_community_place,
    create_community_place,
    create_community_resolver,
    get_communities_resolver,
    get_community_resolver,
)
from resolvers.user import (
    create_dog_resolver,
    delete_dog_resolver,
    me_resolver,
    set_push_token,
    update_dog_resolver,
)
from resolvers.walks import (
    create_walk_resolver,
    get_walk_day_activity_resolver,
    get_walk_interval_activity_by_day,
    get_walk_resolver,
    get_walks_resolver,
)
from utils.scalars import DateTimeScalar


@strawberry.type
class Query:
    get_event: CalendarEventType | None = strawberry.field(resolver=get_event_resolver)
    get_events: list[CalendarEventType] = strawberry.field(resolver=get_events_resolver)
    get_walks: list[WalkType] = strawberry.field(resolver=get_walks_resolver)
    get_walk: WalkType | None = strawberry.field(resolver=get_walk_resolver)
    get_walk_day_activity: WalkDayActivity = strawberry.field(
        resolver=get_walk_day_activity_resolver
    )
    get_walk_interval_activity_by_day: WalkIntervalActivity = strawberry.field(
        resolver=get_walk_interval_activity_by_day
    )
    me: UserType = strawberry.field(resolver=me_resolver)
    get_communities: list[CommunityType] = strawberry.field(resolver=get_communities_resolver)
    get_community: CommunityType = strawberry.field(resolver=get_community_resolver)


@strawberry.type
class Mutation:
    create_event: CalendarEventType = strawberry.field(resolver=create_event_resolver)
    create_walk: WalkType = strawberry.field(resolver=create_walk_resolver)
    set_push_token: UserType = strawberry.field(resolver=set_push_token)
    create_community: CommunityType = strawberry.field(resolver=create_community_resolver)
    create_community_place: CommunityType = strawberry.field(resolver=create_community_place)
    checkin_community_place: CommunityType = strawberry.field(resolver=checkin_community_place)
    create_dog: DogType = strawberry.field(resolver=create_dog_resolver)
    update_dog: DogType = strawberry.field(resolver=update_dog_resolver)
    delete_dog: bool = strawberry.field(resolver=delete_dog_resolver)


schema = strawberry.Schema(Query, mutation=Mutation, scalar_overrides={datetime: DateTimeScalar})


async def get_context() -> Context:
    return Context()


graphql_app = GraphQLRouter(schema, context_getter=get_context)  # type: ignore[arg-type]

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")


@app.get("/health")
async def health_check():
    """Basic health check endpoint for liveness probes."""
    return {"status": "healthy"}


@app.get("/health/ready")
async def readiness_check():
    """Readiness check that verifies database connectivity."""
    from sqlmodel import Session, text

    from config.database import engine

    try:
        with Session(engine) as session:
            session.exec(text("SELECT 1"))
        return {"status": "ready", "database": "connected"}
    except Exception:
        return Response(
            content='{"status": "not ready", "database": "disconnected"}',
            status_code=503,
            media_type="application/json",
        )


@app.on_event("startup")
def setup_db():
    init_db()


# @app.on_event("startup")
# @repeat_every(seconds=60)
# async def send_events_push_tokens() -> None:
#     try:
#         await calendar_event_push_job()
#     except Exception as e:
#         print(e)

# @app.on_event("startup")
# @repeat_every(seconds=60)
# async def send_community_push_tokens() -> None:
#     try:
#         await community_checkin_push_job()
#     except Exception as e:
#         print(e)
