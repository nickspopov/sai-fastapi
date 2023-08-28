import strawberry

# Utils
from datetime import datetime
from typing import List


@strawberry.type
class WalkHistoryItemType:
    latitude: float
    longitude: float
    timestamp: datetime


@strawberry.type
class WalkHistoryType:
    history: List[WalkHistoryItemType]


@strawberry.type
class WalkType:
    id: str
    startedAt: datetime
    finishedAt: datetime
    walkHistory: WalkHistoryType


@strawberry.input
class CreateWalkHistoryItemType:
    latitude: float
    longitude: float
    timestamp: datetime


@strawberry.input
class CreateWalkHistoryType:
    history: List[CreateWalkHistoryItemType]


@strawberry.input
class CreateWalkInput:
    startedAt: datetime
    finishedAt: datetime
    walkHistory: CreateWalkHistoryType
