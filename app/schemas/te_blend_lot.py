"""te_blend_lot API スキーマ"""
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class TeBlendLotRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_no: int
    lot_status: str
    organic_class: str
    work_date: datetime.date
    item_no: int | None
    item_name: str
    unit_weight: Decimal
    remarks: str | None
    lot_part_info: object | None


class BlendLotUpsertPayload(BaseModel):
    """フロントからの JSON は camelCase を許容"""

    model_config = ConfigDict(populate_by_name=True)

    product_no: int | None = Field(None, validation_alias=AliasChoices("productNo", "product_no"))
    lot_status: str | None = Field(None, validation_alias=AliasChoices("lotStatus", "lot_status"))
    organic_class: str | None = Field(None, validation_alias=AliasChoices("organicClass", "organic_class"))
    work_date: datetime.date = Field(validation_alias=AliasChoices("workDate", "work_date"))
    item_no: int | None = Field(None, validation_alias=AliasChoices("itemNo", "item_no"))
    item_name: str = Field(validation_alias=AliasChoices("itemName", "item_name"))
    unit_weight: Decimal = Field(validation_alias=AliasChoices("unitWeight", "unit_weight"))
    remarks: str | None = None
    lot_part_info: Any | None = Field(None, validation_alias=AliasChoices("lotPartInfo", "lot_part_info"))


class BlendLotDeleteRow(BaseModel):
    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    product_no: int | None = Field(None, validation_alias=AliasChoices("productNo", "product_no"))


class BlendLotDeleteRequest(BaseModel):
    lots: list[BlendLotDeleteRow] = Field(default_factory=list)


class BlendLotDeleteResponse(BaseModel):
    deleted_count: int


class BlendLotConfirmStockRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    product_no: int = Field(validation_alias=AliasChoices("productNo", "product_no"))


class BlendLotConfirmStockResponse(BaseModel):
    ok: bool = True
    product_no: int
    transfer_nos: list[int]
    lot_status: str = "3"
