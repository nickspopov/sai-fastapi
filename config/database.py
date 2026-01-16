import os
from collections.abc import Generator
from contextlib import contextmanager

from dotenv import load_dotenv
from sqlmodel import Session, create_engine

# Load environment variables from .env file (don't override existing env vars from Docker)
load_dotenv(override=False)

# Get PostgreSQL connection details from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/sai")

# Ensure URL uses the correct dialect name
if DATABASE_URL.startswith("postgres:"):
    DATABASE_URL = "postgresql" + DATABASE_URL[8:]

# Create SQLModel engine
SQL_ECHO = os.getenv("SQL_ECHO", "false").lower() == "true"
engine = create_engine(DATABASE_URL, echo=SQL_ECHO)


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
