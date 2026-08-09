"""SQLAlchemy engine・セッション・DeclarativeBase。"""
from __future__ import annotations

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    """全 Entity ORM の基底。"""


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://igeta:igeta@localhost:5432/igeta_new",
)

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
