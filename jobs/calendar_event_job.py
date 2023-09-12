from config.database import engine
from database.calendar_event import CalendarEvent
from database.calendar_event_job import CalendarEventJob

from datetime import datetime, timedelta

from database.user import User

from service.notifications import send_push_notification_to_tokens_list

async def calendar_event_push_job() -> None:
    jobs = await engine.find(CalendarEventJob, {"scheduledAt": {"$lte": datetime.now()}})

    if len(jobs) == 0:
        return

    for job in jobs:
  
        user = await engine.find_one(User, {"_id": job.userId})
        event = await engine.find_one(CalendarEvent, {"_id": job.calendarEventId})
        
        if user is None or event is None:
            await engine.delete(job)
            continue
        
        result = send_push_notification_to_tokens_list(user.pushTokens, "Event reminder", f"Event {event.title} is about to start")

        if result:
            await engine.delete(job)
        
        

