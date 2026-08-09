"""tr_constant API スキーマ"""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class TrConstantRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    const_field: str
    const_value: str
    const_name: str
    display_order: int | None
    display: bool | None
