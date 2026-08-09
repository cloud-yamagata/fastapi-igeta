"""第二工場ロット製造登録（変更・削除）API スキーマ。"""
from __future__ import annotations

from pydantic import BaseModel, Field


class Factory2LotBaseFieldsPayload(BaseModel):
    lot_name: str
    work_date: str
    unit_weight: float
    unit_number: int
    fraction_weight: float | None = None
    fraction_number: int | None = None
    remarks: str | None = None
    make_year: str = ""
    count: str = ""
    use_name: str = ""


class Factory2LotCategoryFieldsPayload(BaseModel):
    temperature: str | None = None
    humidity: str | None = None
    work_start_hh: str | None = None
    work_start_mm: str | None = None
    work_end_hh: str | None = None
    work_end_mm: str | None = None
    work_before_cleaning_start_hh: str | None = None
    work_before_cleaning_start_mm: str | None = None
    work_before_cleaning_end_hh: str | None = None
    work_before_cleaning_end_mm: str | None = None
    work_end_cleaning_start_hh: str | None = None
    work_end_cleaning_start_mm: str | None = None
    work_end_cleaning_end_hh: str | None = None
    work_end_cleaning_end_mm: str | None = None
    work_before_cleaning_chk: bool = False
    work_after_cleaning_chk: bool = False
    device_chk: bool = False
    operation_chk: bool = False
    rest_chk: bool = False
    magnet_cleaning_chk: bool = False
    use_device_unit1_chk: bool = False
    use_device_unit2_chk: bool = False
    use_device_unit3_chk: bool = False
    packing_case1_chk: bool = False
    packing_case2_chk: bool = False


class Factory2LotPartRowPayload(BaseModel):
    lot_no: int
    part_no: int
    part_name: str | None = None
    make_year: str | None = None
    count: str | None = None
    use_quantity: float | None = None
    remarks: str | None = None


class Factory2LotUpdateRequest(BaseModel):
    parent_lot_no: int
    organic_class: str = "C"
    base_fields: Factory2LotBaseFieldsPayload
    category_fields: Factory2LotCategoryFieldsPayload
    part_rows: list[Factory2LotPartRowPayload] = Field(default_factory=list)


class Factory2LotCreateRequest(BaseModel):
    process_type: str
    organic_class: str = "C"
    base_fields: Factory2LotBaseFieldsPayload
    category_fields: Factory2LotCategoryFieldsPayload = Field(default_factory=Factory2LotCategoryFieldsPayload)
    part_rows: list[Factory2LotPartRowPayload] = Field(default_factory=list)


class Factory2LotDeleteRequest(BaseModel):
    lot_no: int


class Factory2LotMutationResponse(BaseModel):
    ok: bool = True
    lot_no: int
    product_no: int | None = None
