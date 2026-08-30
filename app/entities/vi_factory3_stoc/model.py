"""
ビュー ``vi_factory3_stoc``（第3工場仕上茶在庫）の SQLAlchemy モデル。
"""
from __future__ import annotations

from decimal import Decimal

from sqlalchemy import Integer, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ViFactory3Stoc(Base):
    """第3工場仕上茶在庫（ビュー）"""

    __tablename__ = "vi_factory3_stoc"
    __table_args__ = {"info": {"is_view": True}}

    item_no: Mapped[int] = mapped_column(Integer(), primary_key=True)
    product_no: Mapped[int] = mapped_column(Integer(), primary_key=True)
    item_name: Mapped[str | None] = mapped_column(Text(), nullable=True)
    organic_class: Mapped[str | None] = mapped_column(Text(), nullable=True)
    item_group_no: Mapped[int | None] = mapped_column(Integer(), nullable=True)
    stoc_quantity: Mapped[Decimal | None] = mapped_column(Numeric(), nullable=True)
