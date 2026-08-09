"""
テーブル ``te_lot_categorys_blend`` の SQLAlchemy モデル（DB辞書.tsv 自動生成）。
"""
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import DateTime, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TeLotCategorysBlend(Base):
    """配合個別情報"""

    # table: te_lot_categorys_blend | 配合個別情報
    __tablename__ = "te_lot_categorys_blend"

    lot_no: Mapped[int] = mapped_column(Integer(), primary_key=True)  # lot_no | ロットNO | PK | NOT NULL
    sensual_test_color: Mapped[str | None] = mapped_column(Text(), nullable=True)  # sensual_test_color | 水色 |  | NULL可
    sensual_test_taste: Mapped[str | None] = mapped_column(Text(), nullable=True)  # sensual_test_taste | 味 |  | NULL可
    sensual_test_aroma: Mapped[str | None] = mapped_column(Text(), nullable=True)  # sensual_test_aroma | 香 |  | NULL可
    remarks: Mapped[str | None] = mapped_column(Text(), nullable=True)  # remarks | #(論理名なし・DB辞書列コメント空) |  | NULL可
    update_time: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=False), nullable=True)  # update_time | #(論理名なし・DB辞書列コメント空) |  | NULL可

