"""
テーブル ``te_factory1_transfer`` の SQLAlchemy モデル（DB辞書.tsv 自動生成）。
"""
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import Date, DateTime, Integer, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TeFactory1Transfer(Base):
    """第1工場移動実績"""

    # table: te_factory1_transfer | 第1工場移動実績
    __tablename__ = "te_factory1_transfer"

    lot_no: Mapped[str] = mapped_column(Text(), primary_key=True)  # lot_no | ロットNO | PK | NOT NULL
    transfer_date: Mapped[datetime.date] = mapped_column(Date())  # transfer_date | 移動日 |  | NOT NULL
    transfer: Mapped[str] = mapped_column(Text())  # transfer | 移動先 |  | NOT NULL
    unit_weight: Mapped[Decimal] = mapped_column(Numeric(6, 2))  # unit_weight | 梱包重量 |  | NOT NULL
    unit_number: Mapped[int] = mapped_column(Integer())  # unit_number | 梱包本数 |  | NOT NULL
    fraction_weight: Mapped[Decimal] = mapped_column(Numeric(6, 2))  # fraction_weight | 端数重量 |  | NOT NULL
    fraction_number: Mapped[int] = mapped_column(Integer())  # fraction_number | 端数本数 |  | NOT NULL
    remarks: Mapped[str | None] = mapped_column(Text(), nullable=True)  # remarks | 摘要 |  | NULL可
    update_time: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=False), nullable=True)  # update_time | 更新時間 |  | NULL可

