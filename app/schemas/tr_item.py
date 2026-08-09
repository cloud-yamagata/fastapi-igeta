"""tr_item API スキーマ"""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, field_validator


class TrItemRead(BaseModel):
    """DB の display（boolean 等）をフロント互換の文字列に揃える。"""

    model_config = ConfigDict(from_attributes=True)

    item_no: int | None
    system_class: str
    organic_class: str
    item_group_no: int
    item_name: str
    jan_code: str
    package_size: int
    display_order: int
    display: str
    remarks: str | None

    @field_validator("display", mode="before")
    @classmethod
    def _display_to_str(cls, v: object) -> str:
        if v is True:
            return "true"
        if v is False:
            return "false"
        if v is None:
            return ""
        return str(v)


class TrItemUpsertPayload(BaseModel):
    item_no: int
    system_class: str
    organic_class: str
    item_group_no: int
    item_name: str
    jan_code: str = ""
    package_size: int = 100
    display_order: int = 5
    display: bool = True
    remarks: str | None = None


class TrItemUpsertResponse(BaseModel):
    ok: bool = True


class TrItemDeletePayload(BaseModel):
    item_no: int


class TrItemDeleteResponse(BaseModel):
    ok: bool = True
