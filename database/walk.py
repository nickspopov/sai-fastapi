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

    model_config = {
        "collection": "walks"
    }

    def to_graphQL(self):
        return WalkType(
            id=str(self.id), startedAt=self.startedAt, finishedAt=self.finishedAt, walkHistory=self.walkHistory.to_graphQL(),
            avgSpeed=self.get_avg_speed(), avgPace=self.get_avg_pace(), distance=self.get_distance(), duration=self.get_duration()
        )

    def get_distance_between_two_points(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        from math import cos, asin, sqrt
        p = 0.017453292519943295
        a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * \
            cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
        return 12742 * asin(sqrt(a))

    def get_distance(self) -> float:
        distance = 0.0
        for i in range(len(self.walkHistory.history) - 1):
            distance += self.get_distance_between_two_points(
                self.walkHistory.history[i].latitude, self.walkHistory.history[i].longitude, self.walkHistory.history[i + 1].latitude, self.walkHistory.history[i + 1].longitude)
        return distance

    def get_duration(self) -> float:
        return (self.finishedAt - self.startedAt).total_seconds()

    def get_avg_speed(self) -> float:
        duration = self.get_duration() / 3600
        if duration == 0:
            return 0.0
        return self.get_distance() / duration
    
    def get_avg_pace(self) -> float:
        distance = self.get_distance()
        if distance == 0:
            return 0.0
        return self.get_duration() / 60 / distance
