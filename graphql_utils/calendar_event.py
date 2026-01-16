from datetime import datetime
from enum import Enum

import strawberry


@strawberry.enum
class CalendarEventTypeEnumType(Enum):
    walking = "walking"
    food = "food"
    pills = "pills"
    grooming = "grooming"
    vet = "vet"
    other = "other"


@strawberry.type
class CalendarEventType:
    id: str
    title: str
    notes: str
    startedAt: datetime
    endedAt: datetime
    type: CalendarEventTypeEnumType


@strawberry.input
class CreateEventInput:
    title: str
    notes: str
    startedAt: datetime
    endedAt: datetime
    type: CalendarEventTypeEnumType
