"""
テーブル ``te_purchase_receive`` の SQLAlchemy モデル（DB辞書.tsv 自動生成）。
"""
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import Date, DateTime, Integer, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TePurchaseReceive(Base):
    """仕入受入実績"""

    # table: te_purchase_receive | 仕入受入実績
    __tablename__ = "te_purchase_receive"

    year: Mapped[int] = mapped_column(Integer(), primary_key=True)  # year | 年度 | PK | NOT NULL
    purchase: Mapped[str] = mapped_column(Text(), primary_key=True)  # purchase | 仕入先 | PK | NOT NULL
    bid_no: Mapped[str] = mapped_column(Text(), primary_key=True)  # bid_no | 入札NO | PK | NOT NULL
    receive_date: Mapped[datetime.date] = mapped_column(Date(), primary_key=True)  # receive_date | 受入日 | PK | NOT NULL
    unit_weight: Mapped[Decimal] = mapped_column(Numeric(6, 2))  # unit_weight | 梱包重量 |  | NOT NULL
    unit_number: Mapped[int] = mapped_column(Integer())  # unit_number | 梱包本数 |  | NOT NULL
    fraction_weight: Mapped[Decimal] = mapped_column(Numeric(6, 2))  # fraction_weight | 端数重量 |  | NOT NULL
    fraction_number: Mapped[int] = mapped_column(Integer())  # fraction_number | 端数本数 |  | NOT NULL
    remarks: Mapped[str | None] = mapped_column(Text(), nullable=True)  # remarks | 摘要 |  | NULL可
    update_time: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=False), nullable=True)  # update_time | #(論理名なし・DB辞書列コメント空) |  | NULL可

