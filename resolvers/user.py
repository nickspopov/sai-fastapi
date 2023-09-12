from config.authentication import check_authentication
from config.database import engine

from graphql_utils.types import Info
from graphql_utils.user import UserType


async def me_resolver(self, info: Info) -> UserType:
    user = await check_authentication(info)
    return user.to_graphQL()

async def set_push_token(self, info: Info, token: str) -> UserType:
    user = await check_authentication(info)
    
    if not user.pushTokens:
        user.pushTokens = []
    
    if token in user.pushTokens:
        return user.to_graphQL()
    
    user.pushTokens.append(token)
    await engine.save(user)
    return user.to_graphQL()