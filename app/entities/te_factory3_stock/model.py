"""
テーブル ``te_factory3_stock`` の SQLAlchemy モデル（DB辞書.tsv 自動生成）。
"""
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import Date, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TeFactory3Stock(Base):
    """第3工場受入実績"""

    # table: te_factory3_stock | 第3工場受入実績
    __tablename__ = "te_factory3_stock"

    stock_date: Mapped[datetime.date] = mapped_column(Date(), primary_key=True)  # stock_date | 受入日 | PK | NOT NULL
    use_tea_no: Mapped[int] = mapped_column(Integer(), primary_key=True)  # use_tea_no | 使用茶NO | PK | NOT NULL
    make_year: Mapped[int] = mapped_column(Integer(), primary_key=True)  # make_year | 年 | PK | NOT NULL
    count: Mapped[int] = mapped_column(Integer(), primary_key=True)  # count | 回数 | PK | NOT NULL
    stock_quantity: Mapped[Decimal] = mapped_column(Numeric(6, 1))  # stock_quantity | 受入量 |  | NOT NULL
    stock_type: Mapped[str] = mapped_column(String(1))  # stock_type | 受入種別 |  | NOT NULL
    remarks: Mapped[str | None] = mapped_column(Text(), nullable=True)  # remarks | 備考 |  | NULL可

