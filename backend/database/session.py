from typing import Generator
from sqlalchemy.orm import sessionmaker, Session
from backend.database.database import engine

# Configure SessionLocal factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a database session and handles closure."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
