"""
テーブル ``te_lot_base`` の SQLAlchemy モデル（DB辞書.tsv 自動生成）。
"""
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import Date, DateTime, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TeLotBase(Base):
    """ロット基本情報"""

    # table: te_lot_base | ロット基本情報
    __tablename__ = "te_lot_base"

    lot_no: Mapped[int] = mapped_column(Integer(), primary_key=True)  # lot_no | ロットNO | PK | NOT NULL
    process_type: Mapped[str] = mapped_column(Text())  # process_type | 工程分類 |  | NOT NULL
    product_no: Mapped[int] = mapped_column(Integer())  # product_no | 製造NO |  | NOT NULL
    lot_status: Mapped[str] = mapped_column(String(1))  # lot_status | ロット状態 |  | NOT NULL
    lot_name: Mapped[str] = mapped_column(Text())  # lot_name | ロット名 |  | NOT NULL
    work_date: Mapped[datetime.date] = mapped_column(Date())  # work_date | 作業日 |  | NOT NULL
    organic_class: Mapped[str] = mapped_column(String(1))  # organic_class | 有機区分 |  | NOT NULL
    unit_weight: Mapped[Decimal] = mapped_column(Numeric(6, 2))  # unit_weight | 梱包重量 |  | NOT NULL
    unit_number: Mapped[int] = mapped_column(Integer())  # unit_number | 梱包数 |  | NOT NULL
    fraction_weight: Mapped[Decimal | None] = mapped_column(Numeric(6, 2), nullable=True)  # fraction_weight | 端数重量 |  | NULL可
    fraction_number: Mapped[int | None] = mapped_column(Integer(), nullable=True)  # fraction_number | 端数本数 |  | NULL可
    remarks: Mapped[str | None] = mapped_column(Text(), nullable=True)  # remarks | 摘要 |  | NULL可
    update_time: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=False), nullable=True)  # update_time | #(論理名なし・DB辞書列コメント空) |  | NULL可

