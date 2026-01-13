from functools import cached_property
from typing import Optional
import os

from strawberry.fastapi import BaseContext
from strawberry.types import Info as _Info
from strawberry.types.info import RootValueType

from sqlmodel import Session, select
from config.database import engine, get_session
from database.models import User, Dog  # Updated import for SQLModel

import firebase_admin
from firebase_admin import credentials
from firebase_admin.auth import verify_id_token

directory = os.getcwd()

cred = credentials.Certificate(directory + "/config/sai-ios-firebase-adminsdk-dmgtl-2dcabece02.json")
firebase_admin.initialize_app(cred)

SKIP_AUTH = True

class Context(BaseContext):
    def __init__(self):
        super().__init__()
        self._session = None

    @property
    def session(self) -> Session:
        if self._session is None:
            self._session = Session(engine)
        return self._session

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if self._session is not None:
            if exc_type is not None:
                self._session.rollback()
            else:
                self._session.commit()
            self._session.close()
            self._session = None

    @cached_property
    async def user(self) -> Optional[User]:
        if not self.request:
            return None

        if SKIP_AUTH:
            return self.session.exec(select(User).where(User.email == "dev@example.com")).first()

        authorization = self.request.headers.get("Authorization", None) 

        if not authorization:
            return None
        
        user_email = ""
        try:
            firebase_verification = verify_id_token(authorization)
            user_email = firebase_verification["email"]
        except:
            return None
        
        user_db = self.session.exec(select(User).where(User.email == user_email)).first()
        if not user_db:
            return None

        # Eager loading of dogs relationship
        # dogs = session.exec(select(Dog).join(Dog.owners).where(User.id == user_db.id)).all()
        
        return user_db
    

async def check_authentication(info: _Info[Context, RootValueType]) -> User:
    db_user = await info.context.user
    if not db_user:
        raise Exception("Not authenticated")
    return db_user