# GraphQL
import strawberry

# FastAPI
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

# Utils
from typing import List, Union, cast

from graphql_utils.calendar_event import CalendarEventType
from graphql_utils.walk import  WalkType
from resolvers.calendar_event import create_event_resolver, get_all_events_resolver, get_event_resolver
from resolvers.walks import get_walks_resolver

@strawberry.type
class Query:
    get_event: Union[CalendarEventType, None] = strawberry.field(resolver=get_event_resolver)
    get_all_events: List[Union[CalendarEventType, None]] = strawberry.field(resolver=get_all_events_resolver)
    get_walks: List[WalkType] = strawberry.field(resolver=get_walks_resolver)

@strawberry.type
class Mutation:
    create_event: CalendarEventType = strawberry.field(resolver=create_event_resolver)

schema = strawberry.Schema(Query, mutation=Mutation)

graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
