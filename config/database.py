from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine, Model, Field, EmbeddedModel
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get MongoDB connection details from environment variables
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
MONGODB_DB = os.getenv("MONGODB_DB", "sai")

# Create MongoDB client
client = AsyncIOMotorClient(MONGODB_URL)

# Create ODMantic engine
engine = AIOEngine(client=client, database=MONGODB_DB)

# Export models and engine
__all__ = ["Model", "Field", "EmbeddedModel", "engine"]