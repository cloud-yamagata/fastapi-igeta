"""
テーブル ``te_lot_part`` の SQLAlchemy モデル（DB辞書.tsv 自動生成）。
"""
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import DateTime, Integer, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TeLotPart(Base):
    """使用部品"""

    # table: te_lot_part | 使用部品
    __tablename__ = "te_lot_part"

    lot_no: Mapped[int] = mapped_column(Integer(), primary_key=True)  # lot_no | ロットNO | PK | NOT NULL
    part_no: Mapped[int] = mapped_column(Integer(), primary_key=True)  # part_no | 部品NO | PK | NOT NULL
    use_quantity: Mapped[Decimal | None] = mapped_column(Numeric(6, 1), nullable=True)  # use_quantity | 投入量 |  | NULL可
    remarks: Mapped[str | None] = mapped_column(Text(), nullable=True)  # remarks | 摘要 |  | NULL可
    update_time: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=False), nullable=True)  # update_time | #(論理名なし・DB辞書列コメント空) |  | NULL可

