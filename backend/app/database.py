from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import urllib.parse

from .config import settings

# Support SQLite (local file) and PostgreSQL via DATABASE_URL
DATABASE_URL = settings.database_url

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    # SQLite needs this for use with SQLAlchemy in multithreaded apps
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, future=True, connect_args=connect_args)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
)
