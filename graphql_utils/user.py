import strawberry

from graphql_utils.dog import DogType


@strawberry.type
class UserType:
    id: str
    name: str
    email: str
    dogs: list[DogType]
