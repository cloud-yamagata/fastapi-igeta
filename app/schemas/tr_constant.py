"""tr_constant API スキーマ"""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class TrConstantRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    const_field: str
    const_value: str
    const_name: str
    display_order: int | None
    display: bool | None


class TrConstantUpsertPayload(BaseModel):
    const_field: str = Field(min_length=1)
    const_value: str = Field(min_length=1)
    const_name: str = Field(min_length=1)
    display_order: int | None = None
    display: bool | None = True


class TrConstantUpsertResponse(BaseModel):
    ok: bool = True


class TrConstantDeletePayload(BaseModel):
    const_field: str = Field(min_length=1)
    const_value: str = Field(min_length=1)


class TrConstantDeleteResponse(BaseModel):
    ok: bool = True
