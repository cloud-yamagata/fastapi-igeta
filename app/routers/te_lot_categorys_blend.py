"""te_lot_categorys_blend API 雛形（dict 応答・専用スキーマは後から分離可）。"""
from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_session
from app.entities.te_lot_categorys_blend.model import TeLotCategorysBlend
from app.entities.te_lot_categorys_blend.repository import TeLotCategorysBlendRepository
from app.schemas.te_lot_categorys_blend import (
    TeLotCategorysBlendUpsertPayload,
    TeLotCategorysBlendUpsertResponse,
)

router = APIRouter(tags=["te_lot_categorys_blend"])


def _cell(v: object) -> object:
    if v is None:
        return None
    if hasattr(v, "isoformat"):
        return v.isoformat()
    if isinstance(v, Decimal):
        return float(v)
    return v


def _apply_upsert_payload(row: TeLotCategorysBlend, payload: TeLotCategorysBlendUpsertPayload) -> TeLotCategorysBlend:
    row.sensual_test_color = payload.sensual_test_color
    row.sensual_test_taste = payload.sensual_test_taste
    row.sensual_test_aroma = payload.sensual_test_aroma
    row.remarks = payload.remarks
    row.update_time = datetime.now()
    return row


@router.get("/te_lot_categorys_blend/", response_model=list[dict])
def list_te_lot_categorys_blend(session: Session = Depends(get_session)) -> list[dict]:
    rows = TeLotCategorysBlendRepository.list_all(session)
    keys = [c.key for c in TeLotCategorysBlend.__table__.columns]
    return [{k: _cell(getattr(r, k)) for k in keys} for r in rows]


@router.post("/te_lot_categorys_blend/upsert", response_model=TeLotCategorysBlendUpsertResponse)
def upsert_te_lot_categorys_blend(
    payload: TeLotCategorysBlendUpsertPayload,
    session: Session = Depends(get_session),
) -> TeLotCategorysBlendUpsertResponse:
    existing = TeLotCategorysBlendRepository.get_by_pk(session, payload.lot_no)
    if existing is None:
        row = TeLotCategorysBlend(lot_no=payload.lot_no)
        _apply_upsert_payload(row, payload)
        TeLotCategorysBlendRepository.create(session, row)
    else:
        _apply_upsert_payload(existing, payload)
        TeLotCategorysBlendRepository.update(session, existing)
    return TeLotCategorysBlendUpsertResponse(ok=True, lot_no=payload.lot_no)
