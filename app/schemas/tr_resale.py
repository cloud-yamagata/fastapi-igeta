"""tr_resale API スキーマ（ResaleCorrect 相当）"""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TrResaleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    resale: str
    rate: int
    postage: int
    limit_price: int
    fixed_price: int
    calc_type: int
    remarks: str | None = None
    update_time: datetime | None = None


class TrResaleUpsertPayload(BaseModel):
    resale: str
    rate: int
    postage: int
    limit_price: int
    fixed_price: int
    calc_type: int
    remarks: str | None = None


class TrResaleUpsertResponse(BaseModel):
    ok: bool = True


class TrResaleDeletePayload(BaseModel):
    resale: str


class TrResaleDeleteResponse(BaseModel):
    ok: bool = True
