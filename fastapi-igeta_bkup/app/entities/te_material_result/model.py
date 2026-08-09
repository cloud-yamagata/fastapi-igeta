"""
テーブル ``te_material_result`` の SQLAlchemy モデル（DB辞書.tsv 自動生成）。
"""
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import Date, DateTime, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TeMaterialResult(Base):
    """原料実績情報"""

    # table: te_material_result | 原料実績情報
    __tablename__ = "te_material_result"

    year: Mapped[int] = mapped_column(Integer(), primary_key=True)  # year | #(論理名なし・DB辞書列コメント空) | PK | NOT NULL
    purchase: Mapped[str] = mapped_column(Text(), primary_key=True)  # purchase | #(論理名なし・DB辞書列コメント空) | PK | NOT NULL
    product_no: Mapped[str] = mapped_column(Text(), primary_key=True)  # product_no | #(論理名なし・DB辞書列コメント空) | PK | NOT NULL
    purchase_date: Mapped[datetime.date] = mapped_column(Date(), primary_key=True)  # purchase_date | #(論理名なし・DB辞書列コメント空) | PK | NOT NULL
    tea_rank: Mapped[str] = mapped_column(Text(), primary_key=True)  # tea_rank | #(論理名なし・DB辞書列コメント空) | PK | NOT NULL
    rank: Mapped[str] = mapped_column(Text(), primary_key=True)  # rank | #(論理名なし・DB辞書列コメント空) | PK | NOT NULL
    tea_type: Mapped[str | None] = mapped_column(Text(), nullable=True)  # tea_type | #(論理名なし・DB辞書列コメント空) |  | NULL可
    tea_life: Mapped[str | None] = mapped_column(Text(), nullable=True)  # tea_life | #(論理名なし・DB辞書列コメント空) |  | NULL可
    organic_class: Mapped[str] = mapped_column(String(1))  # organic_class | #(論理名なし・DB辞書列コメント空) |  | NOT NULL
    producer: Mapped[str | None] = mapped_column(Text(), nullable=True)  # producer | #(論理名なし・DB辞書列コメント空) |  | NULL可
    material_name: Mapped[str] = mapped_column(Text())  # material_name | #(論理名なし・DB辞書列コメント空) |  | NOT NULL
    unit_weight: Mapped[Decimal] = mapped_column(Numeric(6, 2))  # unit_weight | #(論理名なし・DB辞書列コメント空) |  | NOT NULL
    unit_number: Mapped[int] = mapped_column(Integer())  # unit_number | #(論理名なし・DB辞書列コメント空) |  | NOT NULL
    fraction_weight: Mapped[Decimal] = mapped_column(Numeric(6, 2))  # fraction_weight | #(論理名なし・DB辞書列コメント空) |  | NOT NULL
    fraction_number: Mapped[int] = mapped_column(Integer())  # fraction_number | #(論理名なし・DB辞書列コメント空) |  | NOT NULL
    remarks: Mapped[str | None] = mapped_column(Text(), nullable=True)  # remarks | #(論理名なし・DB辞書列コメント空) |  | NULL可
    update_time: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=False), nullable=True)  # update_time | #(論理名なし・DB辞書列コメント空) |  | NULL可

