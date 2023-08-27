from datetime import datetime
from graphql_utils.dog import DogType
from odmantic import Model

class Dog(Model):
    id: str
    name: str
    breed: str
    dateOfBirth: datetime
    sex: str

    class Config:
      collection = "dogs"

    def to_graphQL(self) -> DogType:
       return DogType(id=str(self.id), name=self.name, breed=self.breed, dateOfBirth=self.dateOfBirth, sex=self.sex)
