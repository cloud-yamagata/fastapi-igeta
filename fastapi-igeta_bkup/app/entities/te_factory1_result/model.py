"""
テーブル ``te_factory1_result`` の SQLAlchemy モデル（DB辞書.tsv 自動生成）。
"""
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import Date, DateTime, Integer, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TeFactory1Result(Base):
    """第1工場生産実績"""

    # table: te_factory1_result | 第1工場生産実績
    __tablename__ = "te_factory1_result"

    lot_no: Mapped[str] = mapped_column(Text(), primary_key=True)  # lot_no | ロットNO | PK | NOT NULL
    year: Mapped[int] = mapped_column(Integer())  # year | 年度 |  | NOT NULL
    work_date: Mapped[datetime.date] = mapped_column(Date())  # work_date | 生産日 |  | NOT NULL
    variety: Mapped[str] = mapped_column(Text())  # variety | 品種 |  | NOT NULL
    tea_life: Mapped[str] = mapped_column(Text())  # tea_life | 茶期 |  | NOT NULL
    grade: Mapped[str] = mapped_column(Text())  # grade | 格付 |  | NOT NULL
    tea_rank: Mapped[str] = mapped_column(Text())  # tea_rank | 品柄 |  | NOT NULL
    field_no: Mapped[str] = mapped_column(Text())  # field_no | 圃場 |  | NOT NULL
    unit_weight: Mapped[Decimal] = mapped_column(Numeric(6, 2))  # unit_weight | 梱包重量 |  | NOT NULL
    unit_number: Mapped[int] = mapped_column(Integer())  # unit_number | 梱包数 |  | NOT NULL
    fraction_weight: Mapped[Decimal] = mapped_column(Numeric(6, 2))  # fraction_weight | 端数重量 |  | NOT NULL
    fraction_number: Mapped[int] = mapped_column(Integer())  # fraction_number | 端数数 |  | NOT NULL
    target: Mapped[str | None] = mapped_column(Text(), nullable=True)  # target | 用途 |  | NULL可
    remarks: Mapped[str | None] = mapped_column(Text(), nullable=True)  # remarks | 摘要 |  | NULL可
    update_time: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=False), nullable=True)  # update_time | 更新時間 |  | NULL可

