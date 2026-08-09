"""
テーブル ``tr_purchase`` の SQLAlchemy モデル（DB辞書.tsv 自動生成）。
"""
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TrPurchase(Base):
    """仕入先"""

    # table: tr_purchase | 仕入先
    __tablename__ = "tr_purchase"

    purchase_no: Mapped[Decimal] = mapped_column(Numeric(8, 0), primary_key=True)  # purchase_no | 仕入先NO | PK | NOT NULL
    purchase_name: Mapped[str] = mapped_column(Text())  # purchase_name | 仕入先名 |  | NOT NULL
    purchase: Mapped[str] = mapped_column(Text())  # purchase | 仕入先 |  | NOT NULL
    purchase_short: Mapped[str] = mapped_column(Text())  # purchase_short | 仕入先略称 |  | NOT NULL
    purchase_kana: Mapped[str | None] = mapped_column(Text(), nullable=True)  # purchase_kana | 仕入先カナ |  | NULL可
    prefecture: Mapped[str | None] = mapped_column(Text(), nullable=True)  # prefecture | 県 |  | NULL可
    zip: Mapped[str | None] = mapped_column(Text(), nullable=True)  # zip | 郵便番号 |  | NULL可
    address: Mapped[str | None] = mapped_column(Text(), nullable=True)  # address | 住所 |  | NULL可
    phone_no: Mapped[str | None] = mapped_column(Text(), nullable=True)  # phone_no | 電話番号 |  | NULL可
    fax_no: Mapped[str | None] = mapped_column(Text(), nullable=True)  # fax_no | FAX番号 |  | NULL可

