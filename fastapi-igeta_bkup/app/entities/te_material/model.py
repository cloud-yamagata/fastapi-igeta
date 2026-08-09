"""
テーブル ``te_material`` の SQLAlchemy モデル。

論理名・列コメントは DB辞書.tsv を参照（移行時は辞書と差分確認すること）。
"""
from __future__ import annotations

import datetime
from decimal import Decimal

from sqlalchemy import Integer, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TeMaterial(Base):
    """原料情報。

    DB辞書: table_comment = 原料情報

    Attributes correspond to columns documented in DB辞書.tsv (te_material).
    """

    # table: te_material | 原料情報
    __tablename__ = "te_material"

    material_no: Mapped[int | None] = mapped_column(Integer, primary_key=True)  # material_no | 原料NO | PK | NOT NULL
    year: Mapped[int] = mapped_column(Integer)  # year | 年度 |  | NOT NULL
    purchase: Mapped[str] = mapped_column(Text)  # purchase | 仕入先 |  | NOT NULL
    purchase_no: Mapped[str] = mapped_column(Text)  # purchase_no | 仕入NO |  | NOT NULL
    purchase_date: Mapped[datetime.date] = mapped_column()  # purchase_date | 仕入日 |  | NOT NULL
    variety: Mapped[str | None] = mapped_column(Text, nullable=True)  # variety | 品種 |  | NULL可（辞書上 nullable）
    tea_life: Mapped[str | None] = mapped_column(Text, nullable=True)  # tea_life | 茶期 |  | NULL可（辞書上 nullable）
    organic_class: Mapped[str] = mapped_column(Text)  # organic_class | 有機区分 |  | NOT NULL
    tea_type: Mapped[str | None] = mapped_column(Text, nullable=True)  # tea_type | 茶種 |  | NULL可（辞書上 nullable）
    tea_rank: Mapped[str | None] = mapped_column(Text, nullable=True)  # tea_rank | 品柄 |  | NULL可（辞書上 nullable）
    field_no: Mapped[str | None] = mapped_column(Text, nullable=True)  # field_no | 圃場 |  | NULL可（辞書上 nullable）
    producer: Mapped[str | None] = mapped_column(Text, nullable=True)  # producer | 生産者 |  | NULL可（辞書上 nullable）
    cost: Mapped[int | None] = mapped_column(Integer, nullable=True)  # cost | 原価 |  | NULL可（実装・DBとも nullable）
    material_name: Mapped[str | None] = mapped_column(Text, nullable=True)  # material_name | 原料名 |  | NULL可（辞書上 nullable）
    unit_weight: Mapped[Decimal] = mapped_column(Numeric(6, 2))  # unit_weight | 梱包重量 |  | NOT NULL
    unit_number: Mapped[int] = mapped_column(Integer)  # unit_number | 梱包数 |  | NOT NULL
    fraction_weight: Mapped[Decimal] = mapped_column(Numeric(6, 2))  # fraction_weight | 端数重量 |  | NOT NULL
    fraction_number: Mapped[int] = mapped_column(Integer)  # fraction_number | 端数本数 |  | NOT NULL
    remarks: Mapped[str | None] = mapped_column(Text, nullable=True)  # remarks | 摘要 |  | NULL可（辞書上 nullable）
    update_time: Mapped[datetime.datetime | None] = mapped_column(nullable=True)  # update_time | #(論理名なし・DB辞書列コメント空) |  | NULL可
