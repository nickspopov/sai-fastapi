from enum import Enum
from bson import ObjectId
from odmantic import Model

from datetime import datetime
from graphql_utils.calendar_event import CalendarEventType, CalendarEventTypeEnumType

class CalendarEventTypeEnum(Enum):
    walking = "walking"
    food = "food"
    pills = "pills"
    grooming = "grooming"
    vet = "vet"
    other = "other"

    @staticmethod
    def from_graphQL(graphQL_type: CalendarEventTypeEnumType):
        return CalendarEventTypeEnum(graphQL_type.value)

    def to_graphQL(self):
        return CalendarEventTypeEnumType(self.value)

class CalendarEvent(Model):
    title: str
    notes: str
    type: CalendarEventTypeEnum
    startedAt: datetime
    endedAt: datetime
    userId: ObjectId

    class Config:
        collection = "calendar_events"

    def to_graphQL(self):
        return CalendarEventType(id=str(self.id), title=self.title, type=self.type.to_graphQL(), startedAt=self.startedAt, endedAt=self.endedAt, notes=self.notes)