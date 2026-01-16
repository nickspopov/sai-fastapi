from datetime import datetime, timedelta

from sqlmodel import select

from config.authentication import check_authentication
from database.models import CalendarEvent, CalendarEventJob
from graphql_utils.calendar_event import CalendarEventType, CreateEventInput
from graphql_utils.info import Info


async def get_event_resolver(self, info: Info, id: str) -> CalendarEventType | None:
    user = await check_authentication(info)
    if not user.id:
        raise Exception("User ID is required")

    # Use SQLModel select to query the event
    statement = select(CalendarEvent).where(
        CalendarEvent.id == id, CalendarEvent.user_id == user.id
    )
    event = info.context.session.exec(statement).first()

    if not event:
        raise Exception("Event not found or you don't have access")

    return event.to_graphQL()


async def get_events_resolver(
    self, info: Info, from_date: datetime, to_date: datetime
) -> list[CalendarEventType]:
    user = await check_authentication(info)
    if not user.id:
        raise Exception("User ID is required")

    # Use SQLModel select with date range filter
    statement = select(CalendarEvent).where(
        CalendarEvent.user_id == user.id,
        CalendarEvent.started_at >= from_date,
        CalendarEvent.started_at < to_date,
    )
    events = info.context.session.exec(statement).all()
    return [event.to_graphQL() for event in events]


async def create_event_resolver(self, info: Info, input: CreateEventInput) -> CalendarEventType:
    user = await check_authentication(info)
    if not user.id:
        raise Exception("User ID is required")

    # Create new calendar event
    event = CalendarEvent(
        title=input.title,
        notes=input.notes,
        started_at=input.startedAt,
        ended_at=input.endedAt,
        event_type=input.type.value.lower(),
        user_id=user.id,
    )
    info.context.session.add(event)
    info.context.session.commit()
    info.context.session.refresh(event)

    if not event.id:
        raise Exception("Failed to create event - no ID generated")

    # Create associated job
    job = CalendarEventJob(
        calendar_event_id=event.id,
        user_id=user.id,
        scheduled_at=input.startedAt - timedelta(minutes=15),
    )
    info.context.session.add(job)
    info.context.session.commit()

    return event.to_graphQL()
