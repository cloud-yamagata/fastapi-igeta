"""
テーブル ``tr_direct_shipment`` の SQLAlchemy モデル（DB辞書.tsv 自動生成）。
"""
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import Integer, SmallInteger, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TrDirectShipment(Base):
    """直送先"""

    # table: tr_direct_shipment | 直送先
    __tablename__ = "tr_direct_shipment"

    direct_shipment_no: Mapped[int] = mapped_column(Integer(), primary_key=True)  # direct_shipment_no | 直送先NO | PK | NOT NULL
    direct_shipment_name: Mapped[str] = mapped_column(Text())  # direct_shipment_name | 直送先名 |  | NOT NULL
    direct_shipment_kana: Mapped[str | None] = mapped_column(Text(), nullable=True)  # direct_shipment_kana | 直送先カナ |  | NULL可
    zip: Mapped[str | None] = mapped_column(Text(), nullable=True)  # zip | 郵便番号 |  | NULL可
    address: Mapped[str | None] = mapped_column(Text(), nullable=True)  # address | 住所 |  | NULL可
    phone_no: Mapped[str | None] = mapped_column(Text(), nullable=True)  # phone_no | 電話番号 |  | NULL可
    fax_no: Mapped[str | None] = mapped_column(Text(), nullable=True)  # fax_no | FAX番号 |  | NULL可
    display_order: Mapped[int | None] = mapped_column(SmallInteger(), nullable=True)  # display_order | 表示順 |  | NULL可
    remarks: Mapped[str | None] = mapped_column(Text(), nullable=True)  # remarks | #(論理名なし・DB辞書列コメント空) |  | NULL可

