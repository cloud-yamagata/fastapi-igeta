"""パッケージ製造報告書登録（登録・変更・削除）API スキーマ。"""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class PackageLotPartInfoPayload(BaseModel):
    part_lot_no: int
    out_quantity: float | None = None
    rem_quantity: float | None = None
    use_quantity: float | None = None


class PackageLotBaseFieldsPayload(BaseModel):
    lot_status: str
    organic_class: str
    item_no: int
    product_name: str
    work_date: str
    complete_quantity: int = 0
    sample_quantity: int = 0
    fail_quantity: int = 0
    use_tea_no: int | None = None
    part_name: str | None = None
    remarks: str | None = None
    lot_part_info: list[PackageLotPartInfoPayload] | None = None


class PackageLotCategoryFieldsPayload(BaseModel):
    temperature: str | None = None
    humidity: str | None = None
    packing_start_hh: str | None = None
    packing_start_mm: str | None = None
    packing_end_hh: str | None = None
    packing_end_mm: str | None = None
    work_before_cleaning_start_hh: str | None = None
    work_before_cleaning_start_mm: str | None = None
    work_before_cleaning_end_hh: str | None = None
    work_before_cleaning_end_mm: str | None = None
    work_end_cleaning_start_hh: str | None = None
    work_end_cleaning_start_mm: str | None = None
    work_end_cleaning_end_hh: str | None = None
    work_end_cleaning_end_mm: str | None = None
    hp500_no1_chk: bool | None = None
    hp500_no2_chk: bool | None = None
    fr2_chk: bool | None = None
    fpg_chk: bool | None = None
    uba_chk: bool | None = None
    lift_cleaning_before_chk: bool | None = None
    lift_cleaning_after_chk: bool | None = None
    lift_operation_before_chk: bool | None = None
    lift_operation_after_chk: bool | None = None
    lift_rem_before_chk: bool | None = None
    lift_rem_after_chk: bool | None = None
    packing_filter_before_chk: bool | None = None
    packing_filter_after_chk: bool | None = None
    packing_seal_before_chk: bool | None = None
    packing_seal_after_chk: bool | None = None
    packing_conveyor_before_chk: bool | None = None
    packing_conveyor_after_chk: bool | None = None
    packing_magnet_before_chk: bool | None = None
    packing_magnet_after_chk: bool | None = None
    packing_operation_before_chk: bool | None = None
    packing_operation_after_chk: bool | None = None
    packing_rem_before_chk: bool | None = None
    packing_rem_after_chk: bool | None = None
    tool_cleaning_before_chk: bool | None = None
    tool_cleaning_after_chk: bool | None = None
    uba3_cleaning_before_chk: bool | None = None
    uba3_cleaning_after_chk: bool | None = None
    weight_test_before_chk: str | None = None
    weight_test_after_chk: str | None = None
    residual_oxygen_am: str | None = None
    residual_oxygen_pm: str | None = None
    weight_no_1: str | None = None
    weight_no_2: str | None = None
    weight_no_3: str | None = None
    weight_no_4: str | None = None
    weight_no_5: str | None = None
    weight_chk_1: str | None = None
    weight_chk_2: str | None = None
    weight_chk_3: str | None = None
    weight_chk_4: str | None = None
    weight_chk_5: str | None = None
    remarks: str | None = None


class PackageLotCreateRequest(BaseModel):
    base_fields: PackageLotBaseFieldsPayload
    category_fields: PackageLotCategoryFieldsPayload = Field(
        default_factory=PackageLotCategoryFieldsPayload
    )


class PackageLotUpdateRequest(BaseModel):
    product_no: int
    base_fields: PackageLotBaseFieldsPayload
    category_fields: PackageLotCategoryFieldsPayload


class PackageLotDeleteRequest(BaseModel):
    product_no: int


class PackageLotConfirmStockTransferRowPayload(BaseModel):
    """入出庫1行分（使用ロット1件）。"""

    item_no: int
    lot_no: int
    transfer_quantity: float


class PackageLotConfirmStockRequest(BaseModel):
    product_no: int
    transfer_rows: list[PackageLotConfirmStockTransferRowPayload] = Field(
        ..., min_length=1, max_length=3
    )


class PackageLotMutationResponse(BaseModel):
    ok: bool = True
    product_no: int


class PackageLotConfirmStockResponse(BaseModel):
    ok: bool = True
    product_no: int
    transfer_nos: list[int]
    lot_status: str = "3"
