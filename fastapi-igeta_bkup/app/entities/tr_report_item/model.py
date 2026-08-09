"""
テーブル ``tr_report_item`` の SQLAlchemy モデル（DB辞書.tsv 自動生成）。
"""
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import DateTime, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TrReportItem(Base):
    """レポート項目マスタ"""

    # table: tr_report_item | レポート項目マスタ
    __tablename__ = "tr_report_item"

    report_no: Mapped[int] = mapped_column(Integer(), primary_key=True)  # report_no | レポートNo | PK | NOT NULL
    field_no: Mapped[int] = mapped_column(Integer(), primary_key=True)  # field_no | 項目No | PK | NOT NULL
    field_name: Mapped[str] = mapped_column(Text())  # field_name | 項目名 |  | NOT NULL
    field_title: Mapped[str] = mapped_column(Text())  # field_title | タイトル |  | NOT NULL
    field_column: Mapped[int] = mapped_column(Integer())  # field_column | カラム位置 |  | NOT NULL
    update_time: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=False), nullable=True)  # update_time | 更新時間 |  | NULL可

