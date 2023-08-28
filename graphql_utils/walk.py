import strawberry

# Utils
from datetime import datetime
from typing import List

# General Types
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
    distance: float
    duration: float
    avgSpeed: float
    avgPace: float

# Inputs
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


# Queries
@strawberry.type
class WalkDayActivity:
    totalDistance: float
    totalDuration: float
    avgSpeed: float
    avgPace: float
    date: datetime

@strawberry.type
class WalkIntervalActivityItem:
    duration: float

@strawberry.type
class WalkIntervalActivity:
    totalDistance: float
    totalDuration: float
    items: List[WalkIntervalActivityItem]