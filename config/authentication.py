import os
from functools import cached_property

import firebase_admin
from firebase_admin import credentials
from firebase_admin.auth import verify_id_token
from sqlmodel import Session, select
from strawberry.fastapi import BaseContext
from strawberry.types import Info as _Info
from strawberry.types.info import RootValueType

from config.database import engine
from database.models import User  # Updated import for SQLModel

# Configuration from environment variables
SKIP_AUTH = os.getenv("SKIP_AUTH", "false").lower() == "true"
DEFAULT_DEV_USER_EMAIL = os.getenv("DEFAULT_DEV_USER_EMAIL", "")
FIREBASE_CREDENTIALS_PATH = os.getenv("FIREBASE_CREDENTIALS_PATH", "")

# Initialize Firebase only if credentials are provided
if FIREBASE_CREDENTIALS_PATH and os.path.exists(FIREBASE_CREDENTIALS_PATH):
    cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred)
elif not SKIP_AUTH:
    # Firebase is required for production but credentials not found
    raise RuntimeError(
        "Firebase credentials not found. Set FIREBASE_CREDENTIALS_PATH or enable SKIP_AUTH for development."
    )


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
    async def user(self) -> User | None:
        if not self.request:
            return None

        if SKIP_AUTH:
            if not DEFAULT_DEV_USER_EMAIL:
                return None
            return self.session.exec(
                select(User).where(User.email == DEFAULT_DEV_USER_EMAIL)
            ).first()

        authorization = self.request.headers.get("Authorization", None)

        if not authorization:
            return None

        user_email = ""
        try:
            firebase_verification = verify_id_token(authorization)
            user_email = firebase_verification["email"]
        except Exception:
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
