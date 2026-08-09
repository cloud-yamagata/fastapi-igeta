"""te_material_result upsert / delete リクエスト"""
from __future__ import annotations

import datetime
from decimal import Decimal

from pydantic import BaseModel


class TeMaterialResultUpsertPayload(BaseModel):
    year: int
    purchase: str
    product_no: str
    purchase_date: datetime.date
    tea_rank: str
    rank: str
    tea_type: str | None = None
    tea_life: str | None = None
    organic_class: str
    producer: str | None = None
    material_name: str
    unit_weight: Decimal
    unit_number: int
    fraction_weight: Decimal
    fraction_number: int
    remarks: str | None = None


class TeMaterialResultUpsertResponse(BaseModel):
    ok: bool = True


class TeMaterialResultDeletePayload(BaseModel):
    year: int
    purchase: str
    product_no: str
    purchase_date: datetime.date
    tea_rank: str
    rank: str


class TeMaterialResultDeleteResponse(BaseModel):
    ok: bool = True
