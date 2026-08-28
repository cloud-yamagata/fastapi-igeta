"""
テーブル ``te_monthly_product_plan`` の SQLAlchemy モデル。
"""
from __future__ import annotations

from sqlalchemy import Integer, SmallInteger, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TeMonthlyProductPlan(Base):
    """月別製造計画"""

    __tablename__ = "te_monthly_product_plan"

    year: Mapped[int] = mapped_column(SmallInteger(), primary_key=True)
    month: Mapped[int] = mapped_column(SmallInteger(), primary_key=True)
    item_no: Mapped[int] = mapped_column(SmallInteger(), primary_key=True)
    bulk_no: Mapped[int] = mapped_column(SmallInteger(), primary_key=True)
    sales_size: Mapped[int] = mapped_column(Integer())
    item_name: Mapped[str] = mapped_column(Text())
    package_size: Mapped[int] = mapped_column(SmallInteger())
    need_size: Mapped[int] = mapped_column(SmallInteger())
