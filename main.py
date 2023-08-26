# GraphQL
import strawberry

# FastAPI
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

# Mongo
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine, Model, Field, EmbeddedModel

# Utils
from datetime import datetime
from typing import List

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


class WalkHistoryItem(EmbeddedModel):
    latitude: float = Field(...)
    longitude: float = Field(...)
    timestamp: datetime = Field(...)


class WalkHistory(EmbeddedModel):
    history: List[WalkHistoryItem] = Field([])


class Walk(Model):
    startedAt: datetime = Field(...)
    finishedAt: datetime = Field(...)
    walkHistory: WalkHistory = Field(WalkHistory(history=[]))

    class Config:
        collection = "walks"

@strawberry.type
class WalkHistoryItemType:
    latitude: float
    longitude: float
    timestamp: datetime

@strawberry.type
class WalkHistoryType:
    history: List[WalkHistoryItemType]

@strawberry.type
class WalkType:
    id: str
    startedAt: datetime
    finishedAt: datetime
    walkHistory: WalkHistoryType


def odmantic_to_strawberry_walk_history_item(odmantic_model: WalkHistoryItem) -> WalkHistoryItemType:
    return WalkHistoryItemType(latitude=odmantic_model.latitude, longitude=odmantic_model.longitude, timestamp=odmantic_model.timestamp)


def odmantic_to_strawberry_walk_history(odmantic_model: WalkHistory) -> WalkHistoryType:
    return WalkHistoryType(history=[odmantic_to_strawberry_walk_history_item(item) for item in odmantic_model.history])


def odmantic_to_strawberry_walk(odmantic_model: Walk) -> WalkType:
    return WalkType(id=str(odmantic_model.id), startedAt=odmantic_model.startedAt, finishedAt=odmantic_model.finishedAt, walkHistory=odmantic_to_strawberry_walk_history(odmantic_model.walkHistory))


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

    @strawberry.field
    async def get_walks(self) -> list[WalkType]:
        odmantic_walks = await engine.find(Walk)
        return [odmantic_to_strawberry_walk(walk) for walk in odmantic_walks]

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
