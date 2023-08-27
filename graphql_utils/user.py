from typing import List
import strawberry
from graphql_utils.dog import DogType

@strawberry.type
class UserType:
    from resolvers.dogs import dogs_from_user_resolver
    id: str
    name: str
    dogs: List[DogType] = strawberry.field(resolver=dogs_from_user_resolver)

