from bson import ObjectId

from typing import List
from odmantic import Model
from database.dogs import Dog

from graphql_utils.user import UserType

class User(Model):
    email: str
    name: str
    dogs: List[ObjectId]

    populatedDogs: List[Dog] = []

    class Config:
        collection = "users"

    def to_graphQL(self):
        return UserType(id=str(self.id), name=self.name, dogs=[item.to_graphQL() for item in self.populatedDogs])