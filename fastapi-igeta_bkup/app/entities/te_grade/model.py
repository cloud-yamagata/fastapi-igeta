"""
テーブル ``te_grade`` の SQLAlchemy モデル（DB辞書.tsv 自動生成）。
"""
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TeGrade(Base):
    """ロット格付NO対象表"""

    # table: te_grade | ロット格付NO対象表
    __tablename__ = "te_grade"

    grade_no: Mapped[int] = mapped_column(Integer(), primary_key=True)  # grade_no | 格付NO | PK | NOT NULL
    lot_no: Mapped[int] = mapped_column(Integer())  # lot_no | ロットNO |  | NOT NULL

