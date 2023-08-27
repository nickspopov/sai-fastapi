from functools import cached_property
from bson import ObjectId

from strawberry.fastapi import BaseContext
from strawberry.types import Info as _Info
from strawberry.types.info import RootValueType

from database.user import User
from typing import Optional
from config.database import engine


class Context(BaseContext):
    @cached_property
    async def user(self) -> Optional[User]:
        if not self.request:
            return None

        authorization = self.request.headers.get("Authorization", None)

        if not authorization:
            return None
        
        user_db = await engine.find_one(User, {"_id": ObjectId("64eb42c7b7c18dad6bc17185")})
        return user_db if user_db else None
    

async def check_authentication(info: _Info[Context, RootValueType]) -> User:
    db_user = await info.context.user
    if not db_user:
        raise Exception("Not authenticated")
    return db_user