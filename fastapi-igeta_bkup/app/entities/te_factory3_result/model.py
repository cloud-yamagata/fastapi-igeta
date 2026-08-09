"""
テーブル ``te_factory3_result`` の SQLAlchemy モデル（DB辞書.tsv 自動生成）。
"""
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import Date, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TeFactory3Result(Base):
    """第3工場作業実績"""

    # table: te_factory3_result | 第3工場作業実績
    __tablename__ = "te_factory3_result"

    work_date: Mapped[datetime.date] = mapped_column(Date(), primary_key=True)  # work_date | 作業日 | PK | NOT NULL
    item_no: Mapped[int] = mapped_column(Integer(), primary_key=True)  # item_no | 商品NO | PK | NOT NULL
    quantity: Mapped[int] = mapped_column(Integer())  # quantity | 生産量 |  | NOT NULL
    sample_quantity: Mapped[int] = mapped_column(Integer())  # sample_quantity | 保管サンプル |  | NOT NULL
    use_tea_no: Mapped[int] = mapped_column(Integer())  # use_tea_no | 使用茶NO |  | NOT NULL
    use_quantity: Mapped[Decimal] = mapped_column(Numeric(6, 1))  # use_quantity | 使用量 |  | NOT NULL
    result_type: Mapped[str] = mapped_column(String(1))  # result_type | 実績種別 |  | NOT NULL
    remarks: Mapped[str | None] = mapped_column(Text(), nullable=True)  # remarks | 備考 |  | NULL可

