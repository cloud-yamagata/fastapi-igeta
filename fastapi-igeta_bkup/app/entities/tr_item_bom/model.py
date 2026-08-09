"""
テーブル ``tr_item_bom`` の SQLAlchemy モデル（DB辞書.tsv 自動生成）。
"""
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TrItemBom(Base):
    """商品原料対照表"""

    # table: tr_item_bom | 商品原料対照表
    __tablename__ = "tr_item_bom"

    parent_item_no: Mapped[int] = mapped_column(Integer(), primary_key=True)  # parent_item_no | 商品茶NO | PK | NOT NULL
    child_item_no: Mapped[int] = mapped_column(Integer())  # child_item_no | 原料茶NO |  | NOT NULL

