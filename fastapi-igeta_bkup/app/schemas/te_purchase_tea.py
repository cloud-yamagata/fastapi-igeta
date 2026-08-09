"""te_purchase_tea upsert リクエスト"""
from __future__ import annotations

import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class TePurchaseTeaUpsertPayload(BaseModel):
    year: int
    purchase: str
    bid_no: str = Field(alias="bid_no")
    purchase_date: datetime.date
    variety: str | None = None
    tea_life: str | None = None
    grade: str | None = None
    tea_type: str | None = None
    tea_rank: str | None = None
    field_no: str | None = None
    producer: str | None = None
    cost: int | None = None
    unit_weight: Decimal
    unit_number: int
    fraction_weight: Decimal
    fraction_number: int
    discount: int
    target: str | None = None
    target_plan: str | None = None
    lot_no: str | None = None
    remarks: str | None = None

    model_config = {"populate_by_name": True}


class TePurchaseTeaUpsertResponse(BaseModel):
    ok: bool = True
