from config.authentication import check_authentication
from database.models import Dog
from graphql_utils.dog import CreateDogInput, DogType, UpdateDogInput
from graphql_utils.info import Info
from graphql_utils.user import UserType


async def me_resolver(self, info: Info) -> UserType:
    user = await check_authentication(info)
    return user.to_graphQL()


async def set_push_token(self, info: Info, token: str) -> UserType:
    user = await check_authentication(info)

    if not user.push_tokens:
        user.push_tokens = []

    if token not in user.push_tokens:
        user.push_tokens.append(token)
        info.context.session.commit()

    return user.to_graphQL()


# Dog resolvers
async def create_dog_resolver(self, info: Info, input: CreateDogInput) -> DogType:
    user = await check_authentication(info)
    if not user.id:
        raise Exception("User not found")

    dog = Dog(name=input.name, breed=input.breed, date_of_birth=input.dateOfBirth, sex=input.sex)

    info.context.session.add(dog)
    # Link dog to user via relationship
    user.dogs.append(dog)
    info.context.session.commit()
    info.context.session.refresh(dog)

    return dog.to_graphQL()


async def update_dog_resolver(self, info: Info, input: UpdateDogInput) -> DogType:
    user = await check_authentication(info)
    if not user.id:
        raise Exception("User not found")

    # Ensure the dog exists and belongs to the user
    dog = info.context.session.get(Dog, input.id)
    if not dog:
        raise Exception("Dog not found")

    # Ownership check
    owner_ids = {owner.id for owner in dog.owners}
    if user.id not in owner_ids:
        raise Exception("You are not allowed to modify this dog")

    if input.name is not None:
        dog.name = input.name
    if input.breed is not None:
        dog.breed = input.breed
    if input.dateOfBirth is not None:
        dog.date_of_birth = input.dateOfBirth
    if input.sex is not None:
        dog.sex = input.sex

    info.context.session.commit()
    info.context.session.refresh(dog)
    return dog.to_graphQL()


async def delete_dog_resolver(self, info: Info, id: str) -> bool:
    user = await check_authentication(info)
    if not user.id:
        raise Exception("User not found")

    dog = info.context.session.get(Dog, id)
    if not dog:
        return False

    # Ownership check
    owner_ids = {owner.id for owner in dog.owners}
    if user.id not in owner_ids:
        raise Exception("You are not allowed to delete this dog")

    # Remove association first (in case of many-to-many integrity)
    if dog in user.dogs:
        user.dogs.remove(dog)
    info.context.session.delete(dog)
    info.context.session.commit()
    return True
