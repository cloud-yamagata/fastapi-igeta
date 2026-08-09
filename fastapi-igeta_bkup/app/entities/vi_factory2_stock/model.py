"""
ビュー ``vi_factory2_stock``（第二工場ロット在庫）の SQLAlchemy モデル。
"""
from __future__ import annotations

import datetime
from decimal import Decimal

from sqlalchemy import Date, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ViFactory2Stock(Base):
    """第二工場ロット在庫（ビュー）"""

    __tablename__ = "vi_factory2_stock"
    __table_args__ = {"info": {"is_view": True}}

    lot_no: Mapped[int] = mapped_column(Integer(), primary_key=True)
    process_type: Mapped[str] = mapped_column(Text(), primary_key=True)
    product_no: Mapped[int] = mapped_column(Integer(), primary_key=True)
    process_type_name: Mapped[str | None] = mapped_column(Text(), nullable=True)
    product_date: Mapped[datetime.date | None] = mapped_column(Date(), nullable=True)
    item_name: Mapped[str | None] = mapped_column(Text(), nullable=True)
    lot_name: Mapped[str | None] = mapped_column(Text(), nullable=True)
    organic_class: Mapped[str | None] = mapped_column(String(1), nullable=True)
    make_year: Mapped[str | None] = mapped_column(Text(), nullable=True)
    count: Mapped[str | None] = mapped_column(Text(), nullable=True)
    product_quantity: Mapped[Decimal | None] = mapped_column(Numeric(), nullable=True)
    factory2_stock: Mapped[Decimal | None] = mapped_column(Numeric(), nullable=True)
