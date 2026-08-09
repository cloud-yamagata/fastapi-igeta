"""
テーブル ``te_lot_bom`` の SQLAlchemy モデル（DB辞書.tsv 自動生成）。
"""
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TeLotBom(Base):
    """使用部品"""

    # table: te_lot_bom | 使用部品
    __tablename__ = "te_lot_bom"

    lot_no: Mapped[int] = mapped_column(Integer(), primary_key=True)  # lot_no | ロットNO | PK | NOT NULL
    part_no: Mapped[int] = mapped_column(Integer(), primary_key=True)  # part_no | 部品NO | PK | NOT NULL

