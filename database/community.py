from enum import Enum
from typing import Optional, Union
from bson import ObjectId
from odmantic import Model, EmbeddedModel

from datetime import datetime

from pydantic import BaseModel
from database.user import User
from graphql_utils.community import CommunityMemberLastCheckinType, CommunityMemberType, CommunityPlaceType, CommunityType

from utils.pydantic import PydanticObjectId


class CommunityPlace(EmbeddedModel):
    id: PydanticObjectId
    name: str
    lat: float
    lon: float

    def to_graphQL(self):
        return CommunityPlaceType(
            id=str(self.id),
            name=self.name,
            lat=self.lat,
            lon=self.lon
        )


class CommunityMemberLastCheckin(BaseModel):
    date: datetime
    placeId: PydanticObjectId

    place: Optional[CommunityPlace] = None

    def to_graphQL(self):
        if self.place is None:
            raise Exception("Place not populated")

        return CommunityMemberLastCheckinType(
            date=self.date,
            place=self.place.to_graphQL()
        )


class CommunityMember(EmbeddedModel):
    userId: ObjectId
    lastCheckin: Optional[CommunityMemberLastCheckin]

    user: Optional[User] = None

    def to_graphQL(self):
        if self.user is None:
            raise Exception("User not populated")

        return CommunityMemberType(
            user=self.user.to_graphQL(),
            lastCheckin=self.lastCheckin.to_graphQL() if self.lastCheckin else None
        )


class Community(Model):
    name: str
    ownerId: ObjectId
    members: list[CommunityMember]
    places: list[CommunityPlace]

    owner: Optional[User] = None

    class Config:
        collection = "communities"

    def to_graphQL(self):
        if self.owner is None:
            raise Exception("Owner not populated")

        return CommunityType(
            id=str(self.id),
            name=self.name,
            owner=self.owner.to_graphQL(),
            members=[member.to_graphQL() for member in self.members],
            places=[place.to_graphQL() for place in self.places]
        )
