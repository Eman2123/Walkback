"""Data access for runs. Cache lookup is by param_hash (see walkback/params.py once written)."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Run


def get_run_by_hash(session: Session, param_hash: str) -> Run | None:
    return session.execute(select(Run).where(Run.param_hash == param_hash)).scalar_one_or_none()


def get_run(session: Session, run_id: str) -> Run | None:
    return session.get(Run, run_id)
