"""
テーブル ``te_material_purchase`` の SQLAlchemy モデル（DB辞書.tsv 自動生成）。
"""
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import DateTime, Integer, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TeMaterialPurchase(Base):
    """仕上品仕入情報"""

    # table: te_material_purchase | 仕上品仕入情報
    __tablename__ = "te_material_purchase"

    purchase_no: Mapped[int] = mapped_column(Integer(), primary_key=True)  # purchase_no | 仕入NO | PK | NOT NULL
    purchase_date: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=False), nullable=True)  # purchase_date | 仕入日 |  | NULL可
    item_no: Mapped[int] = mapped_column(Integer())  # item_no | 商品NO |  | NOT NULL
    item_name: Mapped[str | None] = mapped_column(Text(), nullable=True)  # item_name | 仕入品名 |  | NULL可
    purchase_lot_no: Mapped[str | None] = mapped_column(Text(), nullable=True)  # purchase_lot_no | 仕入ロットNO |  | NULL可
    purchase_quantity: Mapped[Decimal | None] = mapped_column(Numeric(6, 2), nullable=True)  # purchase_quantity | 仕入量 |  | NULL可
    supplier: Mapped[str | None] = mapped_column(Text(), nullable=True)  # supplier | 仕入先 |  | NULL可

