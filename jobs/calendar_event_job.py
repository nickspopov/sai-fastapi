from sqlmodel import Session, select
from config.database import engine

from datetime import datetime, timedelta


from service.notifications import send_push_notification_to_tokens_list

async def calendar_event_push_job() -> None:
    # with Session(engine) as session:
    #     jobs = session.exec(select(CalendarEventJob).where(CalendarEventJob.scheduled_at <= datetime.now())).all()

    #     if len(jobs) == 0:
    #         return

    #     for job in jobs:
    
    #         user = session.exec(select(User).where(User.id == job.user_id)).first()
    #         event = session.exec(select(CalendarEvent).where(CalendarEvent.id == job.calendar_event_id)).first()
            
    #         if user is None or event is None:
    #             session.delete(job)
    #             session.commit()
    #             continue
            
    #         result = send_push_notification_to_tokens_list(user.pushTokens, "Event reminder", f"Event {event.title} is about to start")

    #         if result:
    #             session.delete(job)
    #             session.commit()
        
        

