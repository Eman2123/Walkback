"""Engine and session factory. Reads DATABASE_URL from the environment."""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_engine():
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL is not set")
    return create_engine(url, pool_pre_ping=True)


def get_session_factory():
    return sessionmaker(bind=get_engine(), expire_on_commit=False)
