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

user_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjE5MGFkMTE4YTk0MGFkYzlmMmY1Mzc2YjM1MjkyZmVkZThjMmQwZWUiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vc2FpLWlvcyIsImF1ZCI6InNhaS1pb3MiLCJhdXRoX3RpbWUiOjE2OTM4MTkxOTgsInVzZXJfaWQiOiI4czNiOHg4OTdzWm9CM01BazQzOVB4Y0luVEwyIiwic3ViIjoiOHMzYjh4ODk3c1pvQjNNQWs0MzlQeGNJblRMMiIsImlhdCI6MTY5MzgyNzQ4OCwiZXhwIjoxNjkzODMxMDg4LCJlbWFpbCI6ImNvc2F0MjBAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbImNvc2F0MjBAZ21haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.SvSSGuqQK1KAwNEEVFtqrrw-xcciEGNmtw4gm7-P0Vl5_wKFSQQCp8gMogsXGGSxagoNZpTl6ynJkd56XJDbA9uYACSog3ZWMacJL29Huf2tM7SILHNRtWATX2PndXgmzEgq2P6bgxXRSdW8ujBtNoZLdzd72xCwmEjfrfRAhQHtG6rexbO78UqJ5UJclY03MDcBsZZ1HxfpTk3v4dQtWk0-6lcDuedqWzrYRU8kwdYFgnlErJJFXHD9DtQTWUO5lSfz1bdmrVlnSNF-41qPV91o6eT4qh_spRU5f0d2F4inGpz-hPDYxkvJnCahw63qy64Ofw-qIgwdnkY4Uk0OzA"

class Context(BaseContext):
    @cached_property
    async def user(self) -> Optional[User]:
        if not self.request:
            return None

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