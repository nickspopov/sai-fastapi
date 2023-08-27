from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine, Model, Field, EmbeddedModel

client = AsyncIOMotorClient("mongodb://<user>:<password>@cluster0.lxu2tdn.mongodb.net/")
engine = AIOEngine(client=client, database="sai")