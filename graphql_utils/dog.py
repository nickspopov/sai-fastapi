from datetime import datetime
from typing import Optional

import strawberry

@strawberry.type
class DogType:
    id: str
    name: str
    breed: str
    dateOfBirth: datetime
    sex: str


@strawberry.input
class CreateDogInput:
    name: str
    breed: str
    dateOfBirth: datetime
    sex: str


@strawberry.input
class UpdateDogInput:
    id: str
    name: Optional[str] = None
    breed: Optional[str] = None
    dateOfBirth: Optional[datetime] = None
    sex: Optional[str] = None
