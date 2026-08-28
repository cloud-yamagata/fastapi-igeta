"""
テーブル ``tr_sales_plan_item`` の SQLAlchemy モデル。
"""
from __future__ import annotations

from sqlalchemy import Boolean, SmallInteger, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TrSalesPlanItem(Base):
    """販売計画商品マスタ"""

    __tablename__ = "tr_sales_plan_item"

    item_no: Mapped[int] = mapped_column(SmallInteger(), primary_key=True)
    display_order: Mapped[int | None] = mapped_column(SmallInteger(), nullable=True)
    display: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)
    remarks: Mapped[str | None] = mapped_column(Text(), nullable=True)
