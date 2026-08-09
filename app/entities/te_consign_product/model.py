"""
テーブル ``te_consign_product`` の SQLAlchemy モデル（DB辞書.tsv 自動生成）。
"""
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import DateTime, Integer, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TeConsignProduct(Base):
    """外部委託実績情報"""

    # table: te_consign_product | 外部委託実績情報
    __tablename__ = "te_consign_product"

    consign_no: Mapped[int] = mapped_column(Integer(), primary_key=True)  # consign_no | 委託NO | PK | NOT NULL
    consign_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=False))  # consign_date | 委託日 |  | NOT NULL
    item_no: Mapped[int] = mapped_column(Integer())  # item_no | 商品NO |  | NOT NULL
    item_name: Mapped[str] = mapped_column(Text())  # item_name | 商品名 |  | NOT NULL
    delivery_date: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=False), nullable=True)  # delivery_date | 納品日 |  | NULL可
    consign_quantity: Mapped[Decimal | None] = mapped_column(Numeric(6, 2), nullable=True)  # consign_quantity | 委託量 |  | NULL可
    consign_lot_no: Mapped[str | None] = mapped_column(Text(), nullable=True)  # consign_lot_no | 委託先ロットNO |  | NULL可
    supplier: Mapped[str | None] = mapped_column(Text(), nullable=True)  # supplier | 委託先 |  | NULL可
    supply_item_no: Mapped[int | None] = mapped_column(Integer(), nullable=True)  # supply_item_no | 支給品NO |  | NULL可
    supply_product_no: Mapped[int | None] = mapped_column(Integer(), nullable=True)  # supply_product_no | 支給品製造NO |  | NULL可
    supply_item_name: Mapped[str | None] = mapped_column(Text(), nullable=True)  # supply_item_name | 支給品名 |  | NULL可
    supply_quantity: Mapped[Decimal | None] = mapped_column(Numeric(6, 2), nullable=True)  # supply_quantity | 支給品数量 |  | NULL可

