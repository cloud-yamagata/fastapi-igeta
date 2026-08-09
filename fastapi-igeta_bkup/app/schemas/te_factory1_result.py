"""te_factory1_result upsert / delete リクエスト"""
from __future__ import annotations

import datetime
from decimal import Decimal

from pydantic import BaseModel


class TeFactory1ResultUpsertPayload(BaseModel):
    lot_no: str
    year: int
    work_date: datetime.date
    variety: str
    tea_life: str
    grade: str
    tea_rank: str
    field_no: str
    unit_weight: Decimal
    unit_number: int
    fraction_weight: Decimal
    fraction_number: int
    target: str | None = None
    remarks: str | None = None


class TeFactory1ResultUpsertResponse(BaseModel):
    ok: bool = True


class TeFactory1ResultDeletePayload(BaseModel):
    lot_no: str


class TeFactory1ResultDeleteResponse(BaseModel):
    ok: bool = True
