"""
テーブル ``te_package_base`` の SQLAlchemy モデル（DB辞書.tsv 自動生成）。
"""
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import Date, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TePackageBase(Base):
    """パッケージ基本情報"""

    # table: te_package_base | パッケージ基本情報
    __tablename__ = "te_package_base"

    product_no: Mapped[int] = mapped_column(Integer(), primary_key=True)  # product_no | 製造NO | PK | NOT NULL
    organic_class: Mapped[str] = mapped_column(String(1))  # organic_class | 有機区分 |  | NOT NULL
    item_no: Mapped[int] = mapped_column(Integer())  # item_no | 商品NO |  | NOT NULL
    product_name: Mapped[str] = mapped_column(Text())  # product_name | 製造名 |  | NOT NULL
    work_date: Mapped[datetime.date] = mapped_column(Date())  # work_date | 作業日 |  | NOT NULL
    complete_quantity: Mapped[int] = mapped_column(Integer())  # complete_quantity | 生産量 |  | NOT NULL
    sample_quantity: Mapped[int] = mapped_column(Integer())  # sample_quantity | 保管サンプル |  | NOT NULL
    fail_quantity: Mapped[int] = mapped_column(Integer())  # fail_quantity | 不良数 |  | NOT NULL
    use_tea_no: Mapped[int | None] = mapped_column(Integer(), nullable=True)  # use_tea_no | 使用茶NO |  | NULL可
    part_name: Mapped[str | None] = mapped_column(Text(), nullable=True)  # part_name | 原料名 |  | NULL可
    part_lot_no_1: Mapped[int | None] = mapped_column(Integer(), nullable=True)  # part_lot_no_1 | 部品ロットNO1 |  | NULL可
    out_quantity_1: Mapped[Decimal | None] = mapped_column(Numeric(6, 2), nullable=True)  # out_quantity_1 | 出庫数量1 |  | NULL可
    rem_quantity_1: Mapped[Decimal | None] = mapped_column(Numeric(6, 2), nullable=True)  # rem_quantity_1 | 使用残数1 |  | NULL可
    part_lot_no_2: Mapped[int | None] = mapped_column(Integer(), nullable=True)  # part_lot_no_2 | 部品ロットNO2 |  | NULL可
    out_quantity_2: Mapped[Decimal | None] = mapped_column(Numeric(6, 2), nullable=True)  # out_quantity_2 | 出庫数量2 |  | NULL可
    rem_quantity_2: Mapped[Decimal | None] = mapped_column(Numeric(6, 2), nullable=True)  # rem_quantity_2 | 使用残数2 |  | NULL可
    part_lot_no_3: Mapped[int | None] = mapped_column(Integer(), nullable=True)  # part_lot_no_3 | 部品ロットNO3 |  | NULL可
    out_quantity_3: Mapped[Decimal | None] = mapped_column(Numeric(6, 2), nullable=True)  # out_quantity_3 | 出庫数量3 |  | NULL可
    rem_quantity_3: Mapped[Decimal | None] = mapped_column(Numeric(6, 2), nullable=True)  # rem_quantity_3 | 使用残数3 |  | NULL可
    grade_no: Mapped[int | None] = mapped_column(Integer(), nullable=True)  # grade_no | 格付NO |  | NULL可
    remarks: Mapped[str | None] = mapped_column(Text(), nullable=True)  # remarks | 摘要 |  | NULL可

