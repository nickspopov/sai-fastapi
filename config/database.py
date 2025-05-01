import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session
from typing import Generator, Optional
from contextlib import contextmanager

# Load environment variables with force override
load_dotenv(override=True)

# Get PostgreSQL connection details from environment variables
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:postgres@localhost:5432/sai"
)

# Ensure URL uses the correct dialect name
if DATABASE_URL.startswith("postgres:"):
    DATABASE_URL = "postgresql" + DATABASE_URL[8:]

# Create SQLModel engine
engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    """Initialize the database and create all tables"""
    # SQLModel.metadata.create_all(engine)

@contextmanager
def get_session() -> Generator[Session, None, None]:
    """Get a database session"""
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
