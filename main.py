# GraphQL
import strawberry

# FastAPI
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

# Mongo
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine, Model

# Utils
from datetime import datetime

client = AsyncIOMotorClient("mongodb://<user>:<password>@cluster0.lxu2tdn.mongodb.net/")
engine = AIOEngine(client=client, database="sai")


class CalendarEvent(Model):
    name: str
    startedAt: datetime

    class Config:
        collection = "calendar_events"


@strawberry.type
class CalendarEventType:
    id: str
    name: str
    startedAt: datetime


def odmantic_to_strawberry(odmantic_model: CalendarEvent) -> CalendarEventType:
    return CalendarEventType(id=str(odmantic_model.id), name=odmantic_model.name, startedAt=odmantic_model.startedAt)

@strawberry.type
class Query:
    @strawberry.field
    async def get_event(self) -> CalendarEventType:
        odmantic_event = await engine.find_one(CalendarEvent, CalendarEvent.name == "AAAAA")
        return odmantic_to_strawberry(odmantic_event)

    @strawberry.field
    async def get_all_events(self) -> list[CalendarEventType]:
        odmantic_events = await engine.find(CalendarEvent)
        return [odmantic_to_strawberry(event) for event in odmantic_events]

@strawberry.type
class Mutation:
    @strawberry.field
    async def create_event(self, name: str, started_at: datetime) -> CalendarEventType:
        odmantic_event = await engine.save(CalendarEvent(name=name, startedAt=started_at))
        return odmantic_to_strawberry(odmantic_event)


schema = strawberry.Schema(Query, mutation=Mutation)

graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
