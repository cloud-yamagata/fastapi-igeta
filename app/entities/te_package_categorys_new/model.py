"""
テーブル ``te_package_categorys_new`` の SQLAlchemy モデル。
"""
from __future__ import annotations

from sqlalchemy import Boolean, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TePackageCategorysNew(Base):
    """パッケージ個別情報（新）"""

    __tablename__ = "te_package_categorys_new"

    product_no: Mapped[int] = mapped_column(Integer(), primary_key=True)
    temperature: Mapped[str | None] = mapped_column(Text(), nullable=True)
    humidity: Mapped[str | None] = mapped_column(Text(), nullable=True)
    packing_start_hh: Mapped[str | None] = mapped_column(Text(), nullable=True)
    packing_start_mm: Mapped[str | None] = mapped_column(Text(), nullable=True)
    packing_end_hh: Mapped[str | None] = mapped_column(Text(), nullable=True)
    packing_end_mm: Mapped[str | None] = mapped_column(Text(), nullable=True)
    work_before_cleaning_start_hh: Mapped[str | None] = mapped_column(Text(), nullable=True)
    work_before_cleaning_start_mm: Mapped[str | None] = mapped_column(Text(), nullable=True)
    work_before_cleaning_end_hh: Mapped[str | None] = mapped_column(Text(), nullable=True)
    work_before_cleaning_end_mm: Mapped[str | None] = mapped_column(Text(), nullable=True)
    work_end_cleaning_start_hh: Mapped[str | None] = mapped_column(Text(), nullable=True)
    work_end_cleaning_start_mm: Mapped[str | None] = mapped_column(Text(), nullable=True)
    work_end_cleaning_end_hh: Mapped[str | None] = mapped_column(Text(), nullable=True)
    work_end_cleaning_end_mm: Mapped[str | None] = mapped_column(Text(), nullable=True)
    hp500_no1_chk: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)
    hp500_no2_chk: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)
    fr2_chk: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)
    fpg_chk: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)
    uba_chk: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)
    lift_cleaning_before_chk: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)
    lift_cleaning_after_chk: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)
    lift_operation_before_chk: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)
    lift_operation_after_chk: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)
    lift_rem_before_chk: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)
    lift_rem_after_chk: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)
    packing_filter_before_chk: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)
    packing_filter_after_chk: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)
    packing_seal_before_chk: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)
    packing_seal_after_chk: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)
    packing_conveyor_before_chk: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)
    packing_conveyor_after_chk: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)
    packing_magnet_before_chk: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)
    packing_magnet_after_chk: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)
    packing_operation_before_chk: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)
    packing_operation_after_chk: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)
    packing_rem_before_chk: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)
    packing_rem_after_chk: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)
    tool_cleaning_before_chk: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)
    tool_cleaning_after_chk: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)
    uba3_cleaning_before_chk: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)
    uba3_cleaning_after_chk: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)
    weight_test_before_chk: Mapped[str | None] = mapped_column(Text(), nullable=True)
    weight_test_after_chk: Mapped[str | None] = mapped_column(Text(), nullable=True)
    residual_oxygen_am: Mapped[str | None] = mapped_column(Text(), nullable=True)
    residual_oxygen_pm: Mapped[str | None] = mapped_column(Text(), nullable=True)
    weight_no_1: Mapped[str | None] = mapped_column(Text(), nullable=True)
    weight_no_2: Mapped[str | None] = mapped_column(Text(), nullable=True)
    weight_no_3: Mapped[str | None] = mapped_column(Text(), nullable=True)
    weight_no_4: Mapped[str | None] = mapped_column(Text(), nullable=True)
    weight_no_5: Mapped[str | None] = mapped_column(Text(), nullable=True)
    weight_chk_1: Mapped[str | None] = mapped_column(Text(), nullable=True)
    weight_chk_2: Mapped[str | None] = mapped_column(Text(), nullable=True)
    weight_chk_3: Mapped[str | None] = mapped_column(Text(), nullable=True)
    weight_chk_4: Mapped[str | None] = mapped_column(Text(), nullable=True)
    weight_chk_5: Mapped[str | None] = mapped_column(Text(), nullable=True)
    remarks: Mapped[str | None] = mapped_column(Text(), nullable=True)
