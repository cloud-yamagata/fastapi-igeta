"""
テーブル ``te_store_transfer`` の SQLAlchemy モデル（DB辞書.tsv 自動生成）。
"""
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import DateTime, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TeStoreTransfer(Base):
    """入出庫実績"""

    # table: te_store_transfer | 入出庫実績
    __tablename__ = "te_store_transfer"

    transfer_no: Mapped[int] = mapped_column(Integer(), primary_key=True)  # transfer_no | 入出庫NO | PK | NOT NULL
    transfer_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=False))  # transfer_date | 移動日 |  | NOT NULL
    item_no: Mapped[int] = mapped_column(Integer())  # item_no | 商品NO |  | NOT NULL
    product_no: Mapped[int] = mapped_column(Integer())  # product_no | 製造NO |  | NOT NULL
    transfer_type: Mapped[str] = mapped_column(String(1))  # transfer_type | 移動種別 |  | NOT NULL
    result_type: Mapped[str] = mapped_column(String(1))  # result_type | 実績種別 |  | NOT NULL
    lot_no: Mapped[str] = mapped_column(Text())  # lot_no | ロットNO |  | NOT NULL
    lot_type: Mapped[str] = mapped_column(String(1))  # lot_type | ロットタイプ |  | NOT NULL
    reason: Mapped[str | None] = mapped_column(Text(), nullable=True)  # reason | 事由 |  | NULL可
    store_no: Mapped[int] = mapped_column(Integer())  # store_no | 倉庫NO |  | NOT NULL
    store_party_name: Mapped[str | None] = mapped_column(Text(), nullable=True)  # store_party_name | 相手先名 |  | NULL可
    unit_weight: Mapped[Decimal] = mapped_column(Numeric(6, 2))  # unit_weight | 梱包重量 |  | NOT NULL
    unit_number: Mapped[int] = mapped_column(Integer())  # unit_number | 梱包数 |  | NOT NULL
    fraction_weight: Mapped[Decimal] = mapped_column(Numeric(6, 2))  # fraction_weight | 端数重量 |  | NOT NULL
    fraction_number: Mapped[int] = mapped_column(Integer())  # fraction_number | 端数梱包数 |  | NOT NULL
    transfer_quantity: Mapped[Decimal] = mapped_column(Numeric(7, 2))  # transfer_quantity | 移動量 |  | NOT NULL
    unit_type: Mapped[str | None] = mapped_column(Text(), nullable=True)  # unit_type | 単位 |  | NULL可
    remarks: Mapped[str | None] = mapped_column(Text(), nullable=True)  # remarks | 摘要 |  | NULL可

