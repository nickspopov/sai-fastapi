from datetime import datetime

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
    name: str | None = None
    breed: str | None = None
    dateOfBirth: datetime | None = None
    sex: str | None = None
