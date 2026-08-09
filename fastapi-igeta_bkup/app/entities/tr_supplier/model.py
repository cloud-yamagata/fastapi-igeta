"""
テーブル ``tr_supplier`` の SQLAlchemy モデル（DB辞書.tsv 自動生成）。
"""
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TrSupplier(Base):
    """委託先"""

    # table: tr_supplier | 委託先
    __tablename__ = "tr_supplier"

    supplier_no: Mapped[int] = mapped_column(Integer(), primary_key=True)  # supplier_no | 委託先NO | PK | NOT NULL
    supplier_type: Mapped[str] = mapped_column(String(1))  # supplier_type | 委託区分 |  | NOT NULL
    supplier_name: Mapped[str] = mapped_column(Text())  # supplier_name | 委託先名 |  | NOT NULL
    supplier_kana: Mapped[str | None] = mapped_column(Text(), nullable=True)  # supplier_kana | 委託先カナ |  | NULL可

