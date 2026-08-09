"""
テーブル ``te_lot_categorys_firepan`` の SQLAlchemy モデル（DB辞書.tsv 自動生成）。
"""
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import DateTime, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TeLotCategorysFirepan(Base):
    """火入個別情報"""

    # table: te_lot_categorys_firepan | 火入個別情報
    __tablename__ = "te_lot_categorys_firepan"

    lot_no: Mapped[int] = mapped_column(Integer(), primary_key=True)  # lot_no | ロットNO | PK | NOT NULL
    fir_value_1: Mapped[str | None] = mapped_column(Text(), nullable=True)  # fir_value_1 | 排気 |  | NULL可
    fir_value_2: Mapped[str | None] = mapped_column(Text(), nullable=True)  # fir_value_2 | 本機 |  | NULL可
    fir_value_3a: Mapped[str | None] = mapped_column(Text(), nullable=True)  # fir_value_3a | 設定温度左 |  | NULL可
    fir_value_3b: Mapped[str | None] = mapped_column(Text(), nullable=True)  # fir_value_3b | 設定温度右 |  | NULL可
    fir_value_4a: Mapped[str | None] = mapped_column(Text(), nullable=True)  # fir_value_4a | バーナON左 |  | NULL可
    fir_value_4b: Mapped[str | None] = mapped_column(Text(), nullable=True)  # fir_value_4b | バーナON中 |  | NULL可
    fir_value_4c: Mapped[str | None] = mapped_column(Text(), nullable=True)  # fir_value_4c | バーナON右 |  | NULL可
    fir_value_5: Mapped[str | None] = mapped_column(Text(), nullable=True)  # fir_value_5 | 遠赤 |  | NULL可
    fir_value_6: Mapped[str | None] = mapped_column(Text(), nullable=True)  # fir_value_6 | 火入投入量 |  | NULL可
    fir_value_7: Mapped[str | None] = mapped_column(Text(), nullable=True)  # fir_value_7 | 温度 |  | NULL可
    sensual_test_color_before: Mapped[str | None] = mapped_column(Text(), nullable=True)  # sensual_test_color_before | 火入前水色 |  | NULL可
    sensual_test_taste_before: Mapped[str | None] = mapped_column(Text(), nullable=True)  # sensual_test_taste_before | 火入前味 |  | NULL可
    sensual_test_aroma_before: Mapped[str | None] = mapped_column(Text(), nullable=True)  # sensual_test_aroma_before | 火入前香 |  | NULL可
    sensual_test_comment_before: Mapped[str | None] = mapped_column(Text(), nullable=True)  # sensual_test_comment_before | 火入初見 |  | NULL可
    sensual_test_color_after: Mapped[str | None] = mapped_column(Text(), nullable=True)  # sensual_test_color_after | 火入後水色 |  | NULL可
    sensual_test_taste_after: Mapped[str | None] = mapped_column(Text(), nullable=True)  # sensual_test_taste_after | 火入後味 |  | NULL可
    sensual_test_aroma_after: Mapped[str | None] = mapped_column(Text(), nullable=True)  # sensual_test_aroma_after | 火入後香 |  | NULL可
    sensual_test_comment_after: Mapped[str | None] = mapped_column(Text(), nullable=True)  # sensual_test_comment_after | 火入初見 |  | NULL可
    remarks: Mapped[str | None] = mapped_column(Text(), nullable=True)  # remarks | 摘要 |  | NULL可
    update_time: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=False), nullable=True)  # update_time | #(論理名なし・DB辞書列コメント空) |  | NULL可

