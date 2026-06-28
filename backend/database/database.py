import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

# Load environment variables
load_dotenv(override=True)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    # Fallback default for local development if not set in environment
    DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/medshield_x"

# Configure SQLAlchemy engine with parameters optimized for MySQL
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
    pool_pre_ping=True
)

# Declarative base class for models
Base = declarative_base()
