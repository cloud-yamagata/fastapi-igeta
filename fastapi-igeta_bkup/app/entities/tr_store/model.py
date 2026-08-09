"""
テーブル ``tr_store`` の SQLAlchemy モデル（DB辞書.tsv 自動生成）。
"""
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TrStore(Base):
    """倉庫"""

    # table: tr_store | 倉庫
    __tablename__ = "tr_store"

    store_no: Mapped[int] = mapped_column(Integer(), primary_key=True)  # store_no | 倉庫NO | PK | NOT NULL
    store_name: Mapped[str] = mapped_column(Text())  # store_name | 倉庫名 |  | NOT NULL

