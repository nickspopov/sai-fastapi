from config.authentication import check_authentication
from graphql_utils.types import Info
from graphql_utils.user import UserType


async def me_resolver(self, info: Info) -> UserType:
    user = await check_authentication(info)
    return user.to_graphQL()