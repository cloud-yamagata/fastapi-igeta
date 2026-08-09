"""te_material API スキーマ"""
from __future__ import annotations

import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, field_validator


class TeMaterialRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    material_no: int | None
    year: int
    purchase: str
    purchase_no: str
    purchase_date: datetime.date
    variety: str | None
    tea_life: str | None
    organic_class: str
    tea_type: str | None
    tea_rank: str | None
    field_no: str | None
    producer: str | None
    cost: int | None
    material_name: str | None
    unit_weight: float
    unit_number: int
    fraction_weight: float
    fraction_number: int
    remarks: str | None
    update_time: datetime.datetime | None

    @field_validator("unit_weight", "fraction_weight", mode="before")
    @classmethod
    def _decimal_to_float(cls, v: object) -> object:
        if isinstance(v, Decimal):
            return float(v)
        return v
