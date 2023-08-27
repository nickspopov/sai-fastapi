from datetime import datetime
from typing import Union
from database.calendar_event import CalendarEvent

from graphql_utils.calendar_event import CalendarEventType
from config.database import engine

from bson import ObjectId


async def get_event_resolver(self, id: str) -> Union[CalendarEventType, None]:
    odmantic_event = await engine.find_one(CalendarEvent, {"_id": ObjectId(id)})
    return odmantic_event.to_graphQL() if odmantic_event else None


async def get_all_events_resolver(self) -> list[Union[CalendarEventType, None]]:
    odmantic_events = await engine.find(CalendarEvent)
    return [event.to_graphQL() for event in odmantic_events]


async def create_event_resolver(self, name: str, started_at: datetime) -> CalendarEventType:
  odmantic_event = await engine.save(CalendarEvent(name=name, startedAt=started_at))
  if odmantic_event:
      return odmantic_event.to_graphQL()
  else:
      raise Exception("Failed to create event")