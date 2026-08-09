"""
テーブル ``te_lot_divide`` の SQLAlchemy モデル（DB辞書.tsv 自動生成）。
"""
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import Date, DateTime, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TeLotDivide(Base):
    """ロット分割"""

    # table: te_lot_divide | ロット分割
    __tablename__ = "te_lot_divide"

    lot_no: Mapped[int] = mapped_column(Integer(), primary_key=True)  # lot_no | ロットNO | PK | NOT NULL
    divide_no: Mapped[int] = mapped_column(Integer(), primary_key=True)  # divide_no | 分割NO | PK | NOT NULL
    divide_date: Mapped[datetime.date] = mapped_column(Date())  # divide_date | 分割日 |  | NOT NULL
    divide_type: Mapped[str] = mapped_column(String(1))  # divide_type | 分割種別 |  | NOT NULL
    reason: Mapped[str | None] = mapped_column(Text(), nullable=True)  # reason | 事由 |  | NULL可
    divide_quantity: Mapped[Decimal | None] = mapped_column(Numeric(6, 1), nullable=True)  # divide_quantity | 分割量 |  | NULL可
    remarks: Mapped[str | None] = mapped_column(Text(), nullable=True)  # remarks | 摘要 |  | NULL可
    update_time: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=False), nullable=True)  # update_time | #(論理名なし・DB辞書列コメント空) |  | NULL可

