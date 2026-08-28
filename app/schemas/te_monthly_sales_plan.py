"""te_monthly_sales_plan API スキーマ（月次販売計画）"""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class TeMonthlySalesPlanRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    year: int
    month: int
    item_no: int
    item_name: str
    sales_size: int
    remarks: str | None = None


class TeMonthlySalesPlanItemPayload(BaseModel):
    item_no: int
    item_name: str
    sales_size: int = 0
    remarks: str | None = None


class TeMonthlySalesPlanUpsertMonthPayload(BaseModel):
    year: int
    month: int
    items: list[TeMonthlySalesPlanItemPayload]


class TeMonthlySalesPlanUpsertMonthResponse(BaseModel):
    ok: bool = True
    count: int = 0


class TeMonthlySalesPlanDeleteMonthPayload(BaseModel):
    year: int
    month: int


class TeMonthlySalesPlanDeleteMonthResponse(BaseModel):
    ok: bool = True
    count: int = 0
