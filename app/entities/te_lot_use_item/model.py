"""
テーブル ``te_lot_use_item`` の SQLAlchemy モデル（DB辞書.tsv 自動生成）。
"""
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TeLotUseItem(Base):
    """仕上げ茶ロット対象表"""

    # table: te_lot_use_item | 仕上げ茶ロット対象表
    __tablename__ = "te_lot_use_item"

    lot_no: Mapped[int] = mapped_column(Integer(), primary_key=True)  # lot_no | ロットNO | PK | NOT NULL
    use_no: Mapped[int] = mapped_column(Integer())  # use_no | 仕上茶NO |  | NOT NULL
    use_name: Mapped[str | None] = mapped_column(Text(), nullable=True)  # use_name | 仕上茶名 |  | NULL可
    make_year: Mapped[str | None] = mapped_column(Text(), nullable=True)  # make_year | 年度 |  | NULL可
    count: Mapped[str | None] = mapped_column(Text(), nullable=True)  # count | 回数 |  | NULL可

