"""te_purchase_tea API 雛形（dict 応答・専用スキーマは後から分離可）。"""
from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_session
from app.entities.te_purchase_tea.model import TePurchaseTea
from app.entities.te_purchase_tea.repository import TePurchaseTeaRepository
from app.schemas.te_purchase_tea import TePurchaseTeaUpsertPayload, TePurchaseTeaUpsertResponse

router = APIRouter(tags=["te_purchase_tea"])


def _cell(v: object) -> object:
    if v is None:
        return None
    if hasattr(v, "isoformat"):
        return v.isoformat()
    if isinstance(v, Decimal):
        return float(v)
    return v


def _apply_upsert_payload(row: TePurchaseTea, payload: TePurchaseTeaUpsertPayload) -> TePurchaseTea:
    row.purchase_date = payload.purchase_date
    row.variety = payload.variety
    row.tea_life = payload.tea_life
    row.grade = payload.grade
    row.tea_type = payload.tea_type
    row.tea_rank = payload.tea_rank
    row.field_no = payload.field_no
    row.producer = payload.producer
    row.cost = payload.cost
    row.unit_weight = payload.unit_weight
    row.unit_number = payload.unit_number
    row.fraction_weight = payload.fraction_weight
    row.fraction_number = payload.fraction_number
    row.discount = payload.discount
    row.target = payload.target
    row.target_plan = payload.target_plan
    row.lot_no = payload.lot_no
    row.remarks = payload.remarks
    row.update_time = datetime.now()
    return row


@router.get("/te_purchase_tea/", response_model=list[dict])
def list_te_purchase_tea(session: Session = Depends(get_session)) -> list[dict]:
    rows = TePurchaseTeaRepository.list_all(session)
    keys = [c.key for c in TePurchaseTea.__table__.columns]
    return [{k: _cell(getattr(r, k)) for k in keys} for r in rows]


@router.post("/te_purchase_tea/upsert", response_model=TePurchaseTeaUpsertResponse)
def upsert_te_purchase_tea(
    payload: TePurchaseTeaUpsertPayload,
    session: Session = Depends(get_session),
) -> TePurchaseTeaUpsertResponse:
    existing = TePurchaseTeaRepository.get_by_pk(session, payload.year, payload.purchase, payload.bid_no)
    if existing is None:
        row = TePurchaseTea(
            year=payload.year,
            purchase=payload.purchase,
            bid_no=payload.bid_no,
            purchase_date=payload.purchase_date,
            unit_weight=payload.unit_weight,
            unit_number=payload.unit_number,
            fraction_weight=payload.fraction_weight,
            fraction_number=payload.fraction_number,
            discount=payload.discount,
        )
        _apply_upsert_payload(row, payload)
        TePurchaseTeaRepository.create(session, row)
    else:
        _apply_upsert_payload(existing, payload)
        TePurchaseTeaRepository.update(session, existing)
    return TePurchaseTeaUpsertResponse(ok=True)
