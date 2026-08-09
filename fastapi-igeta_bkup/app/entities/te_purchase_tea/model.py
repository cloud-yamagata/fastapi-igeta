"""
テーブル ``te_purchase_tea`` の SQLAlchemy モデル（DB辞書.tsv 自動生成）。
"""
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import Date, DateTime, Integer, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TePurchaseTea(Base):
    """仕入実績"""

    # table: te_purchase_tea | 仕入実績
    __tablename__ = "te_purchase_tea"

    year: Mapped[int] = mapped_column(Integer(), primary_key=True)  # year | 年度 | PK | NOT NULL
    purchase: Mapped[str] = mapped_column(Text(), primary_key=True)  # purchase | 仕入先 | PK | NOT NULL
    bid_no: Mapped[str] = mapped_column(Text(), primary_key=True)  # bid_no | 入札NO | PK | NOT NULL
    purchase_date: Mapped[datetime.date] = mapped_column(Date())  # purchase_date | 仕入日 |  | NOT NULL
    variety: Mapped[str | None] = mapped_column(Text(), nullable=True)  # variety | 品種 |  | NULL可
    tea_life: Mapped[str | None] = mapped_column(Text(), nullable=True)  # tea_life | 茶期 |  | NULL可
    grade: Mapped[str | None] = mapped_column(Text(), nullable=True)  # grade | 格付 |  | NULL可
    tea_type: Mapped[str | None] = mapped_column(Text(), nullable=True)  # tea_type | 茶種 |  | NULL可
    tea_rank: Mapped[str | None] = mapped_column(Text(), nullable=True)  # tea_rank | 品柄 |  | NULL可
    field_no: Mapped[str | None] = mapped_column(Text(), nullable=True)  # field_no | 圃場 |  | NULL可
    producer: Mapped[str | None] = mapped_column(Text(), nullable=True)  # producer | 生産者 |  | NULL可
    cost: Mapped[int | None] = mapped_column(Integer(), nullable=True)  # cost | 原価 |  | NULL可
    unit_weight: Mapped[Decimal] = mapped_column(Numeric(6, 2))  # unit_weight | 梱包重量 |  | NOT NULL
    unit_number: Mapped[int] = mapped_column(Integer())  # unit_number | 梱包数 |  | NOT NULL
    fraction_weight: Mapped[Decimal] = mapped_column(Numeric(6, 2))  # fraction_weight | 端数重量 |  | NOT NULL
    fraction_number: Mapped[int] = mapped_column(Integer())  # fraction_number | 端数数 |  | NOT NULL
    discount: Mapped[int] = mapped_column(Integer())  # discount | 粉引 |  | NOT NULL
    target: Mapped[str | None] = mapped_column(Text(), nullable=True)  # target | 用途 |  | NULL可
    target_plan: Mapped[str | None] = mapped_column(Text(), nullable=True)  # target_plan | 予定用途 |  | NULL可
    lot_no: Mapped[str | None] = mapped_column(Text(), nullable=True)  # lot_no | ロットNO |  | NULL可
    remarks: Mapped[str | None] = mapped_column(Text(), nullable=True)  # remarks | 摘要 |  | NULL可
    update_time: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=False), nullable=True)  # update_time | 更新時間 |  | NULL可

