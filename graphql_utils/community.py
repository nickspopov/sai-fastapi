from datetime import datetime

import strawberry

from graphql_utils.user import UserType


@strawberry.type
class CommunityPlaceType:
    id: str
    name: str
    lat: float
    lon: float


@strawberry.type
class CommunityMemberLastCheckinType:
    date: datetime
    place: CommunityPlaceType


@strawberry.type
class CommunityMemberType:
    user: UserType
    lastCheckin: CommunityMemberLastCheckinType | None


@strawberry.type
class CommunityType:
    id: str
    name: str
    owner: UserType
    members: list[CommunityMemberType]
    places: list[CommunityPlaceType]


@strawberry.input
class CommunityPlaceInput:
    communityId: str
    name: str
    lat: float
    lon: float
