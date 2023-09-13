from functools import cached_property
from bson import ObjectId

from strawberry.fastapi import BaseContext
from strawberry.types import Info as _Info
from strawberry.types.info import RootValueType
from database.dogs import Dog

from database.user import User
from typing import Optional
from config.database import engine
import firebase_admin
from firebase_admin import credentials
from firebase_admin.auth import verify_id_token
import os
directory = os.getcwd()

cred = credentials.Certificate(directory + "/config/sai-ios-firebase-adminsdk-dmgtl-2dcabece02.json")
firebase_admin.initialize_app(cred)

SKIP_AUTH = False

class Context(BaseContext):
    @cached_property
    async def user(self) -> Optional[User]:
        if not self.request:
            return None

        if SKIP_AUTH:
            return await engine.find_one(User, {"email": "dev@example.com"})

        authorization = self.request.headers.get("Authorization", None) 

        if not authorization:
            return None
        
        user_email = ""
        try:
            firebase_verification = verify_id_token(authorization)
            user_email = firebase_verification["email"]
        except:
            return None
        
        user_db = await engine.find_one(User, {"email": user_email})
        if not user_db:
            return None
        dogs = await engine.find(Dog, {"_id": {"$in": [ObjectId(dog) for dog in user_db.dogs]}})
        user_db.populatedDogs = dogs
        return user_db if user_db else None
    

async def check_authentication(info: _Info[Context, RootValueType]) -> User:
    db_user = await info.context.user
    if not db_user:
        raise Exception("Not authenticated")
    return db_user