from backend.database.database import engine, Base
import backend.database.base  # Ensures all models are registered on Base

def init_db() -> None:
    """Creates all database tables in MySQL if they do not exist."""
    Base.metadata.create_all(bind=engine)
