"""te_lot_categorys_blend upsert リクエスト"""
from __future__ import annotations

from pydantic import BaseModel


class TeLotCategorysBlendUpsertPayload(BaseModel):
    lot_no: int
    sensual_test_color: str | None = None
    sensual_test_taste: str | None = None
    sensual_test_aroma: str | None = None
    remarks: str | None = None


class TeLotCategorysBlendUpsertResponse(BaseModel):
    ok: bool = True
    lot_no: int
