"""
テーブル ``package_no`` の SQLAlchemy モデル。
"""
from __future__ import annotations

import datetime

from sqlalchemy import DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class PackageNo(Base):
    """パケージ番号"""

    __tablename__ = "package_no"

    serial_no: Mapped[int] = mapped_column(Integer(), primary_key=True)
    create_date: Mapped[datetime.datetime | None] = mapped_column(
        DateTime(timezone=False), nullable=True
    )
