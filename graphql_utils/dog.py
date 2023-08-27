from datetime import datetime

import strawberry

@strawberry.type
class DogType:
    id: str
    name: str
    breed: str
    dateOfBirth: datetime
    sex: str
