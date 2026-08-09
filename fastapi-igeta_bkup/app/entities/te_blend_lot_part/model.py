"""
テーブル ``te_blend_lot_part`` の SQLAlchemy モデル（DB辞書.tsv 自動生成）。
"""
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TeBlendLotPart(Base):
    """ブレンドロット部品情報"""

    # table: te_blend_lot_part | ブレンドロット部品情報
    __tablename__ = "te_blend_lot_part"

    product_no: Mapped[int] = mapped_column(Integer(), primary_key=True)  # product_no | 製造NO | PK | NOT NULL
    part_lot_no: Mapped[str] = mapped_column(Text(), primary_key=True)  # part_lot_no | 使用ロットNO | PK | NOT NULL
    organic_class: Mapped[str] = mapped_column(String(1))  # organic_class | 有機区分 |  | NOT NULL
    lot_class: Mapped[str] = mapped_column(String(1))  # lot_class | ロット区分 |  | NOT NULL
    firepan_no: Mapped[str | None] = mapped_column(Text(), nullable=True)  # firepan_no | 火入表NO |  | NULL可
    finish_no: Mapped[str | None] = mapped_column(Text(), nullable=True)  # finish_no | 仕入表NO |  | NULL可
    blend_no: Mapped[str | None] = mapped_column(Text(), nullable=True)  # blend_no | ブレンドNO |  | NULL可
    material_no: Mapped[str | None] = mapped_column(Text(), nullable=True)  # material_no | 原料NO |  | NULL可
    material_name_base: Mapped[str] = mapped_column(Text())  # material_name_base | 原料基本名 |  | NOT NULL
    make_year: Mapped[str | None] = mapped_column(Text(), nullable=True)  # make_year | 年度 |  | NULL可
    count: Mapped[str | None] = mapped_column(Text(), nullable=True)  # count | 回数 |  | NULL可
    use_quantity: Mapped[Decimal] = mapped_column(Numeric(6, 2))  # use_quantity | 使用数量 |  | NOT NULL
    remarks: Mapped[str | None] = mapped_column(Text(), nullable=True)  # remarks | 摘要 |  | NULL可

