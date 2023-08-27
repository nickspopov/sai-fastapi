import strawberry

@strawberry.type
class UserType:
    id: str
    name: str