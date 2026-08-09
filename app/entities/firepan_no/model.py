"""
テーブル ``firepan_no`` の SQLAlchemy モデル（DB辞書.tsv 自動生成）。
"""
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class FirepanNo(Base):
    """火入番号"""

    # table: firepan_no | 火入番号
    __tablename__ = "firepan_no"

    serial_no: Mapped[int] = mapped_column(Integer(), primary_key=True)  # serial_no | 連番 | PK | NOT NULL
    create_date: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=False), nullable=True)  # create_date | 登録日時 |  | NULL可

