"""tr_sales_plan_item API スキーマ（SalesPlanItemCorrect 相当）"""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class TrSalesPlanItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    item_no: int
    display_order: int | None = None
    display: bool | None = None
    remarks: str | None = None


class TrSalesPlanItemUpsertPayload(BaseModel):
    item_no: int
    display_order: int | None = 5
    display: bool = True
    remarks: str | None = None


class TrSalesPlanItemUpsertResponse(BaseModel):
    ok: bool = True


class TrSalesPlanItemDeletePayload(BaseModel):
    item_no: int


class TrSalesPlanItemDeleteResponse(BaseModel):
    ok: bool = True
