"""
テーブル ``tr_customer`` の SQLAlchemy モデル（DB辞書.tsv 自動生成）。
"""
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TrCustomer(Base):
    """得意先"""

    # table: tr_customer | 得意先
    __tablename__ = "tr_customer"

    customer_no: Mapped[int] = mapped_column(Integer(), primary_key=True)  # customer_no | 得意先NO | PK | NOT NULL
    customer_name: Mapped[str] = mapped_column(Text())  # customer_name | 得意先名 |  | NOT NULL
    customer_kana: Mapped[str | None] = mapped_column(Text(), nullable=True)  # customer_kana | 得意先カナ |  | NULL可
    zip: Mapped[str | None] = mapped_column(String(8), nullable=True)  # zip | 郵便番号 |  | NULL可
    address: Mapped[str | None] = mapped_column(Text(), nullable=True)  # address | 住所 |  | NULL可
    phone_no: Mapped[str | None] = mapped_column(Text(), nullable=True)  # phone_no | 電話番号 |  | NULL可
    fax_no: Mapped[str | None] = mapped_column(Text(), nullable=True)  # fax_no | FAX番号 |  | NULL可
    prefecture: Mapped[int | None] = mapped_column(Integer(), nullable=True)  # prefecture | 県 |  | NULL可
    region: Mapped[int | None] = mapped_column(Integer(), nullable=True)  # region | 地域 |  | NULL可
    channel: Mapped[int | None] = mapped_column(Integer(), nullable=True)  # channel | 販売チャネル |  | NULL可
    age_group: Mapped[int | None] = mapped_column(Integer(), nullable=True)  # age_group | 年齢層 |  | NULL可

