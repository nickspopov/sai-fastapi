from odmantic import Model

from graphql_utils.user import UserType

class User(Model):
    name: str

    class Config:
        collection = "users"

    def to_graphQL(self):
        return UserType(id=str(self.id), name=self.name)