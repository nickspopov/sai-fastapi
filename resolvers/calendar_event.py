from datetime import datetime, timedelta
from typing import Union
from config.authentication import check_authentication
from database.calendar_event import CalendarEvent, CalendarEventTypeEnum
from database.calendar_event_job import CalendarEventJob

from graphql_utils.calendar_event import CalendarEventType, CreateEventInput
from config.database import engine

from bson import ObjectId

from graphql_utils.types import Info


async def get_event_resolver(self, info: Info, id: str) -> Union[CalendarEventType, None]:
    user = await check_authentication(info)

    odmantic_event = await engine.find_one(CalendarEvent, {"_id": ObjectId(id)})

    if odmantic_event and odmantic_event.userId == ObjectId(user.id):
        return odmantic_event.to_graphQL()
    else:
        raise Exception("You are not allowed to access this event")


async def get_events_resolver(self, info: Info, from_date: datetime, to_date: datetime) -> list[CalendarEventType]:
    user = await check_authentication(info)

    query = {"userId": ObjectId(user.id), "startedAt": {
        "$gte": from_date, "$lt": to_date}}
    odmantic_events = await engine.find(CalendarEvent, query)
    return [event.to_graphQL() for event in odmantic_events]


async def create_event_resolver(self, info: Info, input: CreateEventInput) -> CalendarEventType:
    user = await check_authentication(info)

    odmantic_event = await engine.save(CalendarEvent(
        title=input.title,
        notes=input.notes,
        startedAt=input.startedAt,
        type=CalendarEventTypeEnum.from_graphQL(input.type),
        endedAt=input.endedAt,
        userId=ObjectId(user.id)
    ))
    if odmantic_event:
        await engine.save(CalendarEventJob(
            calendarEventId=odmantic_event.id,
            userId=ObjectId(user.id),
            scheduledAt=input.startedAt - timedelta(minutes=15)
        ))
        return odmantic_event.to_graphQL()
    else:
        raise Exception("Failed to create event")
