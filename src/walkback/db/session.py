"""Engine and session factory. The URL comes from the caller (DATABASE_URL in production)."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def make_session_factory(url: str, **engine_kwargs):
    engine = create_engine(url, pool_pre_ping=True, **engine_kwargs)
    return sessionmaker(bind=engine, expire_on_commit=False)
