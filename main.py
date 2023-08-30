# GraphQL
from datetime import datetime
import strawberry

# FastAPI
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

# Utils
from typing import List, Optional, Union
from config.authentication import Context

from graphql_utils.calendar_event import CalendarEventType
from graphql_utils.types import Info
from graphql_utils.user import UserType
from graphql_utils.walk import  WalkDayActivity, WalkIntervalActivity, WalkType
from resolvers.calendar_event import create_event_resolver, get_events_resolver, get_event_resolver
from resolvers.user import me_resolver
from resolvers.walks import create_walk_resolver, get_walk_day_activity_resolver, get_walk_interval_activity_by_day, get_walk_resolver, get_walks_resolver
from utils.scalars import DateTimeScalar

@strawberry.type
class Query:
    get_event: Union[CalendarEventType, None] = strawberry.field(resolver=get_event_resolver)
    get_events: List[Union[CalendarEventType, None]] = strawberry.field(resolver=get_events_resolver)
    get_walks: List[WalkType] = strawberry.field(resolver=get_walks_resolver)
    get_walk: Optional[WalkType] = strawberry.field(resolver=get_walk_resolver)
    get_walk_day_activity: WalkDayActivity = strawberry.field(resolver=get_walk_day_activity_resolver)
    get_walk_interval_activity_by_day: WalkIntervalActivity = strawberry.field(resolver=get_walk_interval_activity_by_day)
    me: UserType = strawberry.field(resolver=me_resolver)


@strawberry.type
class Mutation:
    create_event: CalendarEventType = strawberry.field(resolver=create_event_resolver)
    create_walk: WalkType = strawberry.field(resolver=create_walk_resolver)


schema = strawberry.Schema(Query, mutation=Mutation, scalar_overrides={datetime: DateTimeScalar})

async def get_context() -> Context:
    return Context()

graphql_app = GraphQLRouter(schema, context_getter=get_context)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
