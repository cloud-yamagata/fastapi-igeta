"""
テーブル ``tr_report`` の SQLAlchemy モデル（DB辞書.tsv 自動生成）。
"""
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import DateTime, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TrReport(Base):
    """レポート管理マスタ"""

    # table: tr_report | レポート管理マスタ
    __tablename__ = "tr_report"

    report_no: Mapped[int] = mapped_column(Integer(), primary_key=True)  # report_no | レポートNo | PK | NOT NULL
    report_name: Mapped[str] = mapped_column(Text())  # report_name | レポート名 |  | NOT NULL
    start_row: Mapped[int] = mapped_column(Integer())  # start_row | 開始行 |  | NOT NULL
    start_column: Mapped[int] = mapped_column(Integer())  # start_column | 開始列 |  | NOT NULL
    right_end_cell: Mapped[str] = mapped_column(Text())  # right_end_cell | 右端セル位置 |  | NOT NULL
    update_time: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=False), nullable=True)  # update_time | 更新時間 |  | NULL可

