"""
テーブル ``te_lot`` の SQLAlchemy モデル（DB辞書.tsv 自動生成）。
"""
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TeLot(Base):
    """ロット情報"""

    # table: te_lot | ロット情報
    __tablename__ = "te_lot"

    lot_no: Mapped[int] = mapped_column(Integer(), primary_key=True)  # lot_no | ロットNO | PK | NOT NULL
    product_no: Mapped[int | None] = mapped_column(Integer(), nullable=True)  # product_no | 製造NO |  | NULL可
    work_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=False))  # work_date | 作業日 |  | NOT NULL
    process_type: Mapped[str] = mapped_column(String(2))  # process_type | 工程分類 |  | NOT NULL
    process_name: Mapped[str | None] = mapped_column(Text(), nullable=True)  # process_name | 工程名 |  | NULL可
    lot_name: Mapped[str | None] = mapped_column(Text(), nullable=True)  # lot_name | ロット名 |  | NULL可
    lot_description: Mapped[str | None] = mapped_column(Text(), nullable=True)  # lot_description | ロット通称名 |  | NULL可

