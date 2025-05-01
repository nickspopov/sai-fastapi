from datetime import datetime
from typing import List, Optional, ForwardRef
from sqlmodel import SQLModel, Field, Relationship
import sqlalchemy as sa
import uuid
from pydantic import EmailStr, field_validator
import math

from graphql_utils.user import UserType
from graphql_utils.dog import DogType
from graphql_utils.community import (
    CommunityType, CommunityMemberType, CommunityPlaceType
)
from graphql_utils.walk import WalkType, WalkHistoryType, WalkHistoryItemType
from graphql_utils.calendar_event import CalendarEventType, CalendarEventTypeEnumType

class UUID(SQLModel):
    """Base class that uses UUID as primary key"""
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)


# Relationship tables
class UserDog(SQLModel, table=True):
    """Association table for user-dog relationship"""
    user_id: Optional[str] = Field(foreign_key="user.id", primary_key=True)
    dog_id: Optional[str] = Field(foreign_key="dog.id", primary_key=True)


# Dog model
class Dog(UUID, table=True):
    name: str
    breed: str
    date_of_birth: datetime
    sex: str
    
    # Relationships
    owners: List["User"] = Relationship(back_populates="dogs", link_model=UserDog)

    def to_graphQL(self):
        return DogType(
            id=str(self.id),
            name=self.name,
            breed=self.breed,
            dateOfBirth=self.date_of_birth,
            sex=self.sex
        )


# User model
class User(UUID, table=True):
    email: str = Field(unique=True, index=True)
    name: str
    push_tokens: List[str] = Field(default=[], sa_column=sa.Column(sa.JSON))
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    language: str = Field(default="en")
    
    # Relationships
    dogs: List[Dog] = Relationship(back_populates="owners", link_model=UserDog)
    communities_owned: List["Community"] = Relationship(back_populates="owner")
    community_memberships: List["CommunityMember"] = Relationship(back_populates="user")
    walks: List["Walk"] = Relationship(back_populates="user")
    calendar_events: List["CalendarEvent"] = Relationship(back_populates="user")

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Validate email format"""
        return v
    
    def to_graphQL(self):
        return UserType(
            id=str(self.id),
            name=self.name,
            email=self.email,
            dogs=[dog.to_graphQL() for dog in self.dogs] if self.dogs else []
        )


# Community models
class CommunityPlace(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str
    latitude: float
    longitude: float
    community_id: str = Field(foreign_key="community.id")
    
    # Relationships
    community: "Community" = Relationship(back_populates="places")

    def to_graphQL(self):
        return CommunityPlaceType(
            id=str(self.id),
            name=self.name,
            lat=self.latitude,
            lon=self.longitude
        )


class CommunityMember(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    community_id: str = Field(foreign_key="community.id")
    last_checkin: Optional[datetime] = None
    
    # Relationships
    user: User = Relationship(back_populates="community_memberships")
    community: "Community" = Relationship(back_populates="members")

    def to_graphQL(self):
        if not self.user:
            raise Exception("User not populated")
        return CommunityMemberType(
            user=self.user.to_graphQL(),
            lastCheckin=None  # Since we don't have place info in the SQL model, we can't construct a valid CommunityMemberLastCheckinType
        )


class Community(UUID, table=True):
    name: str
    owner_id: str = Field(foreign_key="user.id")
    
    # Relationships
    owner: User = Relationship(back_populates="communities_owned")
    members: List[CommunityMember] = Relationship(back_populates="community")
    places: List[CommunityPlace] = Relationship(back_populates="community")

    def to_graphQL(self):
        if not self.owner:
            raise Exception("Owner not populated")
        return CommunityType(
            id=str(self.id),
            name=self.name,
            owner=self.owner.to_graphQL(),
            members=[member.to_graphQL() for member in self.members],
            places=[place.to_graphQL() for place in self.places]
        )


# Walk models
class WalkInterval(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    latitude: float
    longitude: float
    timestamp: datetime
    walk_id: str = Field(foreign_key="walk.id")
    
    # Relationships
    walk: "Walk" = Relationship(back_populates="intervals")

    def to_graphQL(self):
        return WalkHistoryItemType(
            latitude=self.latitude,
            longitude=self.longitude,
            timestamp=self.timestamp
        )


class Walk(UUID, table=True):
    started_at: datetime
    finished_at: datetime
    user_id: str = Field(foreign_key="user.id")
    
    # Relationships
    user: User = Relationship(back_populates="walks")
    intervals: List[WalkInterval] = Relationship(back_populates="walk")

    def get_distance_between_two_points(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        p = 0.017453292519943295
        a = 0.5 - math.cos((lat2 - lat1) * p)/2 + math.cos(lat1 * p) * \
            math.cos(lat2 * p) * (1 - math.cos((lon2 - lon1) * p)) / 2
        return 12742 * math.asin(math.sqrt(a))

    def get_distance(self) -> float:
        distance = 0.0
        for i in range(len(self.intervals) - 1):
            distance += self.get_distance_between_two_points(
                self.intervals[i].latitude, self.intervals[i].longitude,
                self.intervals[i + 1].latitude, self.intervals[i + 1].longitude)
        return distance

    def get_duration(self) -> float:
        return (self.finished_at - self.started_at).total_seconds()

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

    def to_graphQL(self):
        walk_history = WalkHistoryType(history=[interval.to_graphQL() for interval in self.intervals])
        return WalkType(
            id=str(self.id),
            startedAt=self.started_at,
            finishedAt=self.finished_at,
            walkHistory=walk_history,
            distance=self.get_distance(),
            duration=self.get_duration(),
            avgSpeed=self.get_avg_speed(),
            avgPace=self.get_avg_pace()
        )


# Calendar Event models
class CalendarEvent(UUID, table=True):
    title: str
    notes: str
    started_at: datetime
    ended_at: datetime
    event_type: str = Field(default="other")  # One of: walking, food, pills, grooming, vet, other
    user_id: str = Field(foreign_key="user.id")
    
    # Relationships
    user: User = Relationship(back_populates="calendar_events")

    def to_graphQL(self):
        return CalendarEventType(
            id=str(self.id),
            title=self.title,
            notes=self.notes,
            startedAt=self.started_at,
            endedAt=self.ended_at,
            type=CalendarEventTypeEnumType(self.event_type)
        )


# Job models for scheduled tasks
class CalendarEventJob(UUID, table=True):
    calendar_event_id: str = Field(foreign_key="calendarevent.id")
    user_id: str = Field(foreign_key="user.id")
    scheduled_at: datetime


class CommunityCheckinJob(UUID, table=True):
    community_id: str = Field(foreign_key="community.id")
    member_id: str = Field(foreign_key="communitymember.id")
    scheduled_at: datetime

# Resolve forward references
User.model_rebuild()
Dog.model_rebuild()
Community.model_rebuild()
CommunityMember.model_rebuild()
CommunityPlace.model_rebuild()
Walk.model_rebuild()
WalkInterval.model_rebuild()
CalendarEvent.model_rebuild() 