from typing import List, TYPE_CHECKING, Annotated

import strawberry

from datetime import datetime

if TYPE_CHECKING:
    from graphql_utils.dog import DogType
    from graphql_utils.user import UserType

async def dogs_from_user_resolver(root: Annotated["UserType", strawberry.lazy("graphql_utils.user")]) -> List[Annotated["DogType", strawberry.lazy("graphql_utils.dog")]]:
    from graphql_utils.dog import DogType

    return [
        
    ]