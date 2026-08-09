"""
テーブル ``te_store_transfer_fa2`` の SQLAlchemy モデル（DB辞書.tsv 自動生成）。
"""
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import DateTime, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TeStoreTransferFa2(Base):
    """入出庫実績"""

    # table: te_store_transfer_fa2 | 入出庫実績
    __tablename__ = "te_store_transfer_fa2"

    transfer_no: Mapped[int] = mapped_column(Integer(), primary_key=True)  # transfer_no | 入出庫NO | PK | NOT NULL
    transfer_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=False))  # transfer_date | 移動日 |  | NOT NULL
    lot_no: Mapped[int] = mapped_column(Integer())  # lot_no | ロットNO |  | NOT NULL
    process_type: Mapped[str] = mapped_column(String(2))  # process_type | 工程種別 |  | NOT NULL
    product_no: Mapped[int] = mapped_column(Integer())  # product_no | 製造NO |  | NOT NULL
    lot_name: Mapped[str | None] = mapped_column(Text(), nullable=True)  # lot_name | ロット名 |  | NULL可
    transfer_type: Mapped[str] = mapped_column(String(1))  # transfer_type | 移動種別 |  | NOT NULL
    result_type: Mapped[str] = mapped_column(String(1))  # result_type | 実績種別 |  | NOT NULL
    lot_type: Mapped[str] = mapped_column(String(1))  # lot_type | ロットタイプ |  | NOT NULL
    reason: Mapped[str | None] = mapped_column(Text(), nullable=True)  # reason | 事由 |  | NULL可
    unit_weight: Mapped[Decimal | None] = mapped_column(Numeric(6, 2), nullable=True)  # unit_weight | 梱包重量 |  | NULL可
    unit_number: Mapped[int | None] = mapped_column(Integer(), nullable=True)  # unit_number | 梱包本数 |  | NULL可
    fraction_weight: Mapped[Decimal | None] = mapped_column(Numeric(6, 2), nullable=True)  # fraction_weight | 端数重量 |  | NULL可
    fraction_number: Mapped[int | None] = mapped_column(Integer(), nullable=True)  # fraction_number | 端数本数 |  | NULL可
    transfer_quantity: Mapped[Decimal] = mapped_column(Numeric(7, 2))  # transfer_quantity | 移動量 |  | NOT NULL
    unit_type: Mapped[str | None] = mapped_column(Text(), nullable=True)  # unit_type | 単位 |  | NULL可
    remarks: Mapped[str | None] = mapped_column(Text(), nullable=True)  # remarks | 摘要 |  | NULL可
    update_time: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=False), nullable=True)  # update_time | #(論理名なし・DB辞書列コメント空) |  | NULL可

