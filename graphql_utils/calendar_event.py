import strawberry
from datetime import datetime

@strawberry.type
class CalendarEventType:
    id: str
    name: str
    startedAt: datetime