"""
テーブル ``te_monthly_plan`` の SQLAlchemy モデル。

論理名・列コメントは DB辞書.tsv を参照。
"""
from __future__ import annotations

import datetime
from typing import Any

from sqlalchemy import Integer, SmallInteger, Text, Time
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TeMonthlyPlan(Base):
    """月別製造計画情報。

    DB辞書: table_comment = 月別製造計画情報
    """

    # table: te_monthly_plan | 月別製造計画情報
    __tablename__ = "te_monthly_plan"

    plan_no: Mapped[int | None] = mapped_column(Integer, primary_key=True)  # plan_no | 計画NO | PK | NOT NULL
    year: Mapped[int] = mapped_column(SmallInteger)  # year | 年 |  | NOT NULL
    month: Mapped[int] = mapped_column(SmallInteger)  # month | 月 |  | NOT NULL
    process_type: Mapped[str] = mapped_column(Text)  # process_type | 工程分類 |  | NOT NULL
    lot_name: Mapped[str] = mapped_column(Text)  # lot_name | ロット名 |  | NOT NULL
    work_date: Mapped[datetime.date] = mapped_column()  # work_date | 作業日 |  | NOT NULL
    work_time: Mapped[datetime.time | None] = mapped_column(Time, nullable=True)  # work_time | 作業時間 |  | NULL可（辞書上 nullable）
    unit_weight: Mapped[int] = mapped_column(Integer)  # unit_weight | 梱包重量 |  | NOT NULL
    item_no: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)  # item_no | 商品NO |  | NULL可（辞書上 nullable）
    remarks: Mapped[str | None] = mapped_column(Text, nullable=True)  # remarks | 摘要 |  | NULL可（辞書上 nullable）
    lot_part_info: Mapped[Any | None] = mapped_column(
        JSONB,
        nullable=True,
        default=None,
    )  # lot_part_info | 使用部品情報 |  | NULL可 | #(辞書:列データ型セル空→jsonb想定)
