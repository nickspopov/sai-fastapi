from database.walk import Walk
from graphql_utils.walk import WalkType
from config.database import engine

async def get_walks_resolver(self) -> list[WalkType]:
    odmantic_walks = await engine.find(Walk)
    return [walk.to_graphQL() for walk in odmantic_walks]