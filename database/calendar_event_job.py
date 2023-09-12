from datetime import datetime
from odmantic import Model

from bson import ObjectId

class CalendarEventJob(Model):
    calendarEventId: ObjectId
    userId: ObjectId
    scheduledAt: datetime

    class Config:
        collection = "calendar_event_jobs"