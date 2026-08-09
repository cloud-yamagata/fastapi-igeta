"""
テーブル ``blend_no`` の SQLAlchemy モデル（DB辞書.tsv 自動生成）。
"""
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class BlendNo(Base):
    """仕上茶番号"""

    # table: blend_no | 仕上茶番号
    __tablename__ = "blend_no"

    serial_no: Mapped[int] = mapped_column(Integer(), primary_key=True)  # serial_no | 連番 | PK | NOT NULL
    create_date: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=False), nullable=True)  # create_date | 登録日時 |  | NULL可

