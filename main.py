# GraphQL
from datetime import datetime
import strawberry

# FastAPI
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from fastapi_utils.tasks import repeat_every

# Utils
from typing import List
from config.authentication import Context

from graphql_utils.calendar_event import CalendarEventType
from graphql_utils.community import CommunityType
from graphql_utils.user import UserType
from graphql_utils.walk import  WalkDayActivity, WalkIntervalActivity, WalkType
from jobs.calendar_event_job import calendar_event_push_job
from resolvers.calendar_event import create_event_resolver, get_events_resolver, get_event_resolver
from resolvers.user import me_resolver, set_push_token
from resolvers.places import get_communities_resolver, create_community_resolver, get_community_resolver, create_community_place, checkin_community_place
from resolvers.walks import create_walk_resolver, get_walk_day_activity_resolver, get_walk_interval_activity_by_day, get_walk_resolver, get_walks_resolver
from utils.scalars import DateTimeScalar

@strawberry.type
class Query:
    get_event: CalendarEventType = strawberry.field(resolver=get_event_resolver)
    get_events: List[CalendarEventType] = strawberry.field(resolver=get_events_resolver)
    get_walks: List[WalkType] = strawberry.field(resolver=get_walks_resolver)
    get_walk: WalkType = strawberry.field(resolver=get_walk_resolver)
    get_walk_day_activity: WalkDayActivity = strawberry.field(resolver=get_walk_day_activity_resolver)
    get_walk_interval_activity_by_day: WalkIntervalActivity = strawberry.field(resolver=get_walk_interval_activity_by_day)
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


schema = strawberry.Schema(Query, mutation=Mutation, scalar_overrides={datetime: DateTimeScalar})

async def get_context() -> Context:
    return Context()

graphql_app = GraphQLRouter(schema, context_getter=get_context)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")


@app.on_event("startup")
@repeat_every(seconds=60)
async def send_events_push_tokens() -> None:
    try: 
        await calendar_event_push_job()
    except Exception as e:
        print(e)
