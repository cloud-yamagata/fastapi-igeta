"""FastAPI 依存注入用 DB セッション。"""
from __future__ import annotations

from collections.abc import Generator

from sqlalchemy.orm import Session

from app.db.base import SessionLocal


def get_session() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session
