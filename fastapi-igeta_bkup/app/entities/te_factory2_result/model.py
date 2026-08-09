"""
テーブル ``te_factory2_result`` の SQLAlchemy モデル（DB辞書.tsv 自動生成）。
"""
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import Date, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TeFactory2Result(Base):
    """第2工場作業実績"""

    # table: te_factory2_result | 第2工場作業実績
    __tablename__ = "te_factory2_result"

    work_date: Mapped[datetime.date] = mapped_column(Date(), primary_key=True)  # work_date | 作業日 | PK | NOT NULL
    use_tea_no: Mapped[int] = mapped_column(Integer(), primary_key=True)  # use_tea_no | 使用茶NO | PK | NOT NULL
    make_year: Mapped[int] = mapped_column(Integer(), primary_key=True)  # make_year | 年 | PK | NOT NULL
    count: Mapped[int] = mapped_column(Integer(), primary_key=True)  # count | 回数 | PK | NOT NULL
    quantity: Mapped[Decimal] = mapped_column(Numeric(6, 1))  # quantity | 生産量 |  | NOT NULL
    result_type: Mapped[str] = mapped_column(String(1))  # result_type | 実績種別 |  | NOT NULL
    remarks: Mapped[str | None] = mapped_column(Text(), nullable=True)  # remarks | 備考 |  | NULL可

