from typing import List
import strawberry
from graphql_utils.dog import DogType

@strawberry.type
class UserType:
    id: str
    name: str
    dogs: List[DogType]

