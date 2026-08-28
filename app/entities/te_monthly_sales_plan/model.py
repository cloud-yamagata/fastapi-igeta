"""
テーブル ``te_monthly_sales_plan`` の SQLAlchemy モデル。
"""
from __future__ import annotations

from sqlalchemy import Integer, SmallInteger, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TeMonthlySalesPlan(Base):
    """月別販売計画"""

    __tablename__ = "te_monthly_sales_plan"

    year: Mapped[int] = mapped_column(SmallInteger(), primary_key=True)
    month: Mapped[int] = mapped_column(SmallInteger(), primary_key=True)
    item_no: Mapped[int] = mapped_column(SmallInteger(), primary_key=True)
    item_name: Mapped[str] = mapped_column(Text())
    sales_size: Mapped[int] = mapped_column(Integer())
    remarks: Mapped[str | None] = mapped_column(Text(), nullable=True)
