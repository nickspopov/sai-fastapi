from config.authentication import check_authentication
from config.database import engine
from sqlmodel import Session, select

from graphql_utils.types import Info
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