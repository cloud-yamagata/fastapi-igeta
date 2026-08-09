"""tr_item_bom API スキーマ（ItemBomCorrect 相当）"""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class TrItemBomRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    parent_item_no: int
    child_item_no: int


class TrItemBomUpsertPayload(BaseModel):
    parent_item_no: int
    child_item_no: int


class TrItemBomUpsertResponse(BaseModel):
    ok: bool = True


class TrItemBomDeletePayload(BaseModel):
    parent_item_no: int


class TrItemBomDeleteResponse(BaseModel):
    ok: bool = True
