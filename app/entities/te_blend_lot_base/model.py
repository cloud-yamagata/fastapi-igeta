"""
テーブル ``te_blend_lot_base`` の SQLAlchemy モデル（DB辞書.tsv 自動生成）。
"""
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import Date, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TeBlendLotBase(Base):
    """ブレンドロット基本情報"""

    # table: te_blend_lot_base | ブレンドロット基本情報
    __tablename__ = "te_blend_lot_base"

    product_no: Mapped[int] = mapped_column(Integer(), primary_key=True)  # product_no | 製造NO | PK | NOT NULL
    organic_class: Mapped[str] = mapped_column(String(1))  # organic_class | 有機区分 |  | NOT NULL
    store_no: Mapped[int] = mapped_column(Integer())  # store_no | 倉庫NO |  | NOT NULL
    item_no: Mapped[int | None] = mapped_column(Integer(), nullable=True)  # item_no | 仕上品NO |  | NULL可
    work_date: Mapped[datetime.date] = mapped_column(Date())  # work_date | #(論理名なし・DB辞書列コメント空) |  | NOT NULL
    product_name: Mapped[str] = mapped_column(Text())  # product_name | 製造名 |  | NOT NULL
    make_year: Mapped[str | None] = mapped_column(Text(), nullable=True)  # make_year | 年度 |  | NULL可
    count: Mapped[str | None] = mapped_column(Text(), nullable=True)  # count | 回数 |  | NULL可
    unit_weight: Mapped[Decimal] = mapped_column(Numeric(6, 2))  # unit_weight | 梱包重量 |  | NOT NULL
    unit_number: Mapped[int] = mapped_column(Integer())  # unit_number | 梱包数 |  | NOT NULL
    fraction_weight: Mapped[Decimal] = mapped_column(Numeric(6, 2))  # fraction_weight | 端数重量 |  | NOT NULL
    fraction_number: Mapped[int] = mapped_column(Integer())  # fraction_number | 端数梱包数 |  | NOT NULL
    remarks: Mapped[str | None] = mapped_column(Text(), nullable=True)  # remarks | 摘要 |  | NULL可

