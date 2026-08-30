"""
テーブル ``te_blend_lot`` の SQLAlchemy モデル。
"""
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import Date, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TeBlendLot(Base):
    """ブレンドロット情報。

    PK: product_no（serial）
    """

    # table: te_blend_lot | ブレンドロット情報
    __tablename__ = "te_blend_lot"

    product_no: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    lot_status: Mapped[str] = mapped_column(String(1), nullable=False)
    organic_class: Mapped[str] = mapped_column(String(1), nullable=False)
    work_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    item_no: Mapped[int | None] = mapped_column(Integer, nullable=True)
    item_name: Mapped[str] = mapped_column(Text, nullable=False)
    unit_weight: Mapped[Decimal] = mapped_column(Numeric(6, 2), nullable=False)
    remarks: Mapped[str | None] = mapped_column(Text, nullable=True)
    lot_part_info: Mapped[Any | None] = mapped_column(JSONB, nullable=True, default=None)
