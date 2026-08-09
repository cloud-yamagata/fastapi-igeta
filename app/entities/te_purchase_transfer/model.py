"""
テーブル ``te_purchase_transfer`` の SQLAlchemy モデル（DB辞書.tsv 自動生成）。
"""
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import Date, DateTime, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TePurchaseTransfer(Base):
    """仕入移動実績"""

    # table: te_purchase_transfer | 仕入移動実績
    __tablename__ = "te_purchase_transfer"

    year: Mapped[int] = mapped_column(Integer(), primary_key=True)  # year | 年度 | PK | NOT NULL
    purchase: Mapped[str] = mapped_column(Text(), primary_key=True)  # purchase | 仕入先 | PK | NOT NULL
    bid_no: Mapped[str] = mapped_column(Text(), primary_key=True)  # bid_no | 入札NO | PK | NOT NULL
    result_type: Mapped[str] = mapped_column(String(1), primary_key=True)  # result_type | 実績種別 | PK | NOT NULL
    transfer: Mapped[str] = mapped_column(Text(), primary_key=True)  # transfer | 移動先 | PK | NOT NULL
    transfer_date: Mapped[datetime.date] = mapped_column(Date())  # transfer_date | 移動日 |  | NOT NULL
    unit_weight: Mapped[Decimal] = mapped_column(Numeric(6, 2))  # unit_weight | 梱包重量 |  | NOT NULL
    unit_number: Mapped[int] = mapped_column(Integer())  # unit_number | 梱包本数 |  | NOT NULL
    fraction_weight: Mapped[Decimal] = mapped_column(Numeric(6, 2))  # fraction_weight | 端数重量 |  | NOT NULL
    fraction_number: Mapped[int] = mapped_column(Integer())  # fraction_number | 端数本数 |  | NOT NULL
    unit_price: Mapped[Decimal | None] = mapped_column(Numeric(7, 2), nullable=True)  # unit_price | 単価 |  | NULL可
    remarks: Mapped[str | None] = mapped_column(Text(), nullable=True)  # remarks | 摘要 |  | NULL可
    update_time: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=False), nullable=True)  # update_time | 更新時間 |  | NULL可

