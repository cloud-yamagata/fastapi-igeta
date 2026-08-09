"""
テーブル ``te_lot_categorys_common`` の SQLAlchemy モデル（DB辞書.tsv 自動生成）。
"""
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import Boolean, DateTime, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TeLotCategorysCommon(Base):
    """共通情報"""

    # table: te_lot_categorys_common | 共通情報
    __tablename__ = "te_lot_categorys_common"

    lot_no: Mapped[int] = mapped_column(Integer(), primary_key=True)  # lot_no | ロットNO | PK | NOT NULL
    temperature: Mapped[str | None] = mapped_column(Text(), nullable=True)  # temperature | 室内温度 |  | NULL可
    humidity: Mapped[str | None] = mapped_column(Text(), nullable=True)  # humidity | 湿度 |  | NULL可
    work_start_hh: Mapped[str | None] = mapped_column(Text(), nullable=True)  # work_start_hh | 製造開始_時 |  | NULL可
    work_start_mm: Mapped[str | None] = mapped_column(Text(), nullable=True)  # work_start_mm | 製造開始_分 |  | NULL可
    work_end_hh: Mapped[str | None] = mapped_column(Text(), nullable=True)  # work_end_hh | 製造終了_時 |  | NULL可
    work_end_mm: Mapped[str | None] = mapped_column(Text(), nullable=True)  # work_end_mm | 製造終了_時 |  | NULL可
    work_before_cleaning_start_hh: Mapped[str | None] = mapped_column(Text(), nullable=True)  # work_before_cleaning_start_hh | 作業前清掃開始_時 |  | NULL可
    work_before_cleaning_start_mm: Mapped[str | None] = mapped_column(Text(), nullable=True)  # work_before_cleaning_start_mm | 作業前清掃開始_分 |  | NULL可
    work_before_cleaning_end_hh: Mapped[str | None] = mapped_column(Text(), nullable=True)  # work_before_cleaning_end_hh | 作業前清掃終了_時 |  | NULL可
    work_before_cleaning_end_mm: Mapped[str | None] = mapped_column(Text(), nullable=True)  # work_before_cleaning_end_mm | 作業前清掃終了_分 |  | NULL可
    work_end_cleaning_start_hh: Mapped[str | None] = mapped_column(Text(), nullable=True)  # work_end_cleaning_start_hh | 作業後清掃開始_時 |  | NULL可
    work_end_cleaning_start_mm: Mapped[str | None] = mapped_column(Text(), nullable=True)  # work_end_cleaning_start_mm | 作業後清掃開始_分 |  | NULL可
    work_end_cleaning_end_hh: Mapped[str | None] = mapped_column(Text(), nullable=True)  # work_end_cleaning_end_hh | 作業前後清掃終了_時 |  | NULL可
    work_end_cleaning_end_mm: Mapped[str | None] = mapped_column(Text(), nullable=True)  # work_end_cleaning_end_mm | 作業前後清掃終了_分 |  | NULL可
    work_before_cleaning_chk: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)  # work_before_cleaning_chk | 作業前清掃確認 |  | NULL可
    work_after_cleaning_chk: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)  # work_after_cleaning_chk | 作業後清掃確認 |  | NULL可
    device_chk: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)  # device_chk | 装置設定確認 |  | NULL可
    operation_chk: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)  # operation_chk | 空動作確認 |  | NULL可
    rest_chk: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)  # rest_chk | 残留物確認 |  | NULL可
    magnet_cleaning_chk: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)  # magnet_cleaning_chk | 磁石清掃確認 |  | NULL可
    use_device_unit1_chk: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)  # use_device_unit1_chk | 使用機械確認1 |  | NULL可
    use_device_unit2_chk: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)  # use_device_unit2_chk | 使用機械確認2 |  | NULL可
    use_device_unit3_chk: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)  # use_device_unit3_chk | 使用機械確認3 |  | NULL可
    packing_case1_chk: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)  # packing_case1_chk | 梱包形態確認1 |  | NULL可
    packing_case2_chk: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)  # packing_case2_chk | 梱包形態確認2 |  | NULL可
    remarks: Mapped[str | None] = mapped_column(Text(), nullable=True)  # remarks | 摘要 |  | NULL可
    update_time: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=False), nullable=True)  # update_time | #(論理名なし・DB辞書列コメント空) |  | NULL可

