from bson import ObjectId

from odmantic import Model, Field, EmbeddedModel

# Utils
from datetime import datetime
from typing import List

from graphql_utils.walk import CreateWalkHistoryType, WalkHistoryItemType, WalkHistoryType, WalkType

class WalkHistoryItem(EmbeddedModel):
    latitude: float = Field(...)
    longitude: float = Field(...)
    timestamp: datetime = Field(...)

    def to_graphQL(self):
        return WalkHistoryItemType(latitude=self.latitude, longitude=self.longitude, timestamp=self.timestamp)


class WalkHistory(EmbeddedModel):
    history: List[WalkHistoryItem] = Field([])

    def to_graphQL(self):
        return WalkHistoryType(history=[item.to_graphQL() for item in self.history])
    
    @staticmethod
    def from_graphQL_input_type(graphQLWalkHistory: CreateWalkHistoryType) -> "WalkHistory":
        return WalkHistory(history=[WalkHistoryItem(latitude=item.latitude, longitude=item.longitude, timestamp=item.timestamp) for item in graphQLWalkHistory.history])


class Walk(Model):
    startedAt: datetime = Field(...)
    finishedAt: datetime = Field(...)
    walkHistory: WalkHistory = Field(WalkHistory(history=[]))
    userId: ObjectId

    class Config:
        collection = "walks"
    
    def to_graphQL(self):
        return WalkType(id=str(self.id), startedAt=self.startedAt, finishedAt=self.finishedAt, walkHistory=self.walkHistory.to_graphQL())