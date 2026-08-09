"""
テーブル ``tr_resale`` の SQLAlchemy モデル（DB辞書.tsv 自動生成）。
"""
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import DateTime, Integer, SmallInteger, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TrResale(Base):
    """転売先"""

    # table: tr_resale | 転売先
    __tablename__ = "tr_resale"

    resale: Mapped[str] = mapped_column(Text(), primary_key=True)  # resale | 転売先 | PK | NOT NULL
    rate: Mapped[int] = mapped_column(SmallInteger())  # rate | 手数料% |  | NOT NULL
    postage: Mapped[int] = mapped_column(Integer())  # postage | 送料 |  | NOT NULL
    limit_price: Mapped[int] = mapped_column(Integer())  # limit_price | 下限額 |  | NOT NULL
    fixed_price: Mapped[int] = mapped_column(Integer())  # fixed_price | 固定額 |  | NOT NULL
    calc_type: Mapped[int] = mapped_column(SmallInteger())  # calc_type | 計算区分 |  | NOT NULL
    remarks: Mapped[str | None] = mapped_column(Text(), nullable=True)  # remarks | 摘要 |  | NULL可
    update_time: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=False), nullable=True)  # update_time | 更新時間 |  | NULL可

