from odmantic import Model

from datetime import datetime
from graphql_utils.calendar_event import CalendarEventType

class CalendarEvent(Model):
    name: str
    startedAt: datetime

    class Config:
        collection = "calendar_events"

    def to_graphQL(self):
        return CalendarEventType(id=str(self.id), name=self.name, startedAt=self.startedAt)