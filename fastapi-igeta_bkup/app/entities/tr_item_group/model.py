"""
テーブル ``tr_item_group`` の SQLAlchemy モデル（DB辞書.tsv 自動生成）。
"""
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import SmallInteger, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TrItemGroup(Base):
    """商品分類"""

    # table: tr_item_group | 商品分類
    __tablename__ = "tr_item_group"

    item_group_no: Mapped[int] = mapped_column(SmallInteger(), primary_key=True)  # item_group_no | 商品分類NO | PK | NOT NULL
    item_group_name: Mapped[str | None] = mapped_column(Text(), nullable=True)  # item_group_name | 商品分類名 |  | NULL可

