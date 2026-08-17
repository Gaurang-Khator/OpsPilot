from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.core.config import get_settings

settings = get_settings()

# engine = the connection pool manager to Postgres, created once at import time
engine = create_engine(settings.database_url)

# SessionLocal = factory that creates a new DB session per request
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    """All ORM model classes will inherit from this."""
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()