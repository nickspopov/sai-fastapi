from datetime import datetime
from odmantic import Model

from bson import ObjectId

class CalendarEventJob(Model):
    calendarEventId: ObjectId
    userId: ObjectId
    scheduledAt: datetime

    model_config = {
        "collection": "calendar_event_jobs"
    }