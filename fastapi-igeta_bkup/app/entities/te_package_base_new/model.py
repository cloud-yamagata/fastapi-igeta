"""
テーブル ``te_package_base_new`` の SQLAlchemy モデル。
"""
from __future__ import annotations

import datetime
from typing import Any

from sqlalchemy import Date, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TePackageBaseNew(Base):
    """パッケージ基本情報（新）"""

    __tablename__ = "te_package_base_new"

    product_no: Mapped[int] = mapped_column(Integer(), primary_key=True)
    lot_status: Mapped[str] = mapped_column(String(1))
    organic_class: Mapped[str] = mapped_column(String(1))
    item_no: Mapped[int] = mapped_column(Integer())
    product_name: Mapped[str] = mapped_column(Text())
    work_date: Mapped[datetime.date] = mapped_column(Date())
    complete_quantity: Mapped[int] = mapped_column(Integer())
    sample_quantity: Mapped[int] = mapped_column(Integer())
    fail_quantity: Mapped[int] = mapped_column(Integer())
    use_tea_no: Mapped[int | None] = mapped_column(Integer(), nullable=True)
    part_name: Mapped[str | None] = mapped_column(Text(), nullable=True)
    remarks: Mapped[str | None] = mapped_column(Text(), nullable=True)
    lot_part_info: Mapped[Any | None] = mapped_column(JSONB, nullable=True)
