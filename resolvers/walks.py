from datetime import datetime
from typing import Optional
from bson import ObjectId
from config.authentication import check_authentication
from database.walk import Walk, WalkHistory
from graphql_utils.types import Info
from graphql_utils.walk import CreateWalkInput, WalkType
from config.database import engine


async def get_walks_resolver(self, info: Info) -> list[WalkType]:
    user = await check_authentication(info)

    db_walks = await engine.find(Walk, {"userId": {"$in": [ObjectId(user.id)]}})

    return [walk.to_graphQL() for walk in db_walks]


async def get_walk_resolver(self, info: Info, id: str) -> Optional[WalkType]:
    user = await check_authentication(info)
    db_walk = await engine.find_one(Walk, {"_id": ObjectId(id)})

    if not db_walk:
        return None

    if db_walk.userId != ObjectId(user.id):
        raise Exception("You are not allowed to access this walk")

    return db_walk.to_graphQL()


async def create_walk_resolver(self, info: Info, input: CreateWalkInput) -> WalkType:
    user = await check_authentication(info)
    db_walk = await engine.save(
        Walk(
            startedAt=input.startedAt,
            finishedAt=input.finishedAt,
            walkHistory=WalkHistory.from_graphQL_input_type(input.walkHistory),
            userId=ObjectId(user.id)
        )
    )
    if db_walk:
        return db_walk.to_graphQL()
    else:
        raise Exception("Failed to create walk")
