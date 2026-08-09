"""te_purchase_transfer API 雛形（dict 応答・専用スキーマは後から分離可）。"""
from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_session
from app.entities.te_purchase_transfer.model import TePurchaseTransfer
from app.entities.te_purchase_transfer.repository import TePurchaseTransferRepository
from app.schemas.te_purchase_transfer import TePurchaseTransferUpsertPayload, TePurchaseTransferUpsertResponse

router = APIRouter(tags=["te_purchase_transfer"])


def _cell(v: object) -> object:
    if v is None:
        return None
    if hasattr(v, "isoformat"):
        return v.isoformat()
    if isinstance(v, Decimal):
        return float(v)
    return v


def _apply_upsert_payload(row: TePurchaseTransfer, payload: TePurchaseTransferUpsertPayload) -> TePurchaseTransfer:
    row.transfer_date = payload.transfer_date
    row.unit_weight = payload.unit_weight
    row.unit_number = payload.unit_number
    row.fraction_weight = payload.fraction_weight
    row.fraction_number = payload.fraction_number
    row.unit_price = payload.unit_price
    row.remarks = payload.remarks
    row.update_time = datetime.now()
    return row


@router.get("/te_purchase_transfer/", response_model=list[dict])
def list_te_purchase_transfer(session: Session = Depends(get_session)) -> list[dict]:
    rows = TePurchaseTransferRepository.list_all(session)
    keys = [c.key for c in TePurchaseTransfer.__table__.columns]
    return [{k: _cell(getattr(r, k)) for k in keys} for r in rows]


@router.post("/te_purchase_transfer/upsert", response_model=TePurchaseTransferUpsertResponse)
def upsert_te_purchase_transfer(
    payload: TePurchaseTransferUpsertPayload,
    session: Session = Depends(get_session),
) -> TePurchaseTransferUpsertResponse:
    existing = TePurchaseTransferRepository.get_by_pk(
        session,
        payload.year,
        payload.purchase,
        payload.bid_no,
        payload.result_type,
        payload.transfer,
    )
    if existing is None:
        row = TePurchaseTransfer(
            year=payload.year,
            purchase=payload.purchase,
            bid_no=payload.bid_no,
            result_type=payload.result_type,
            transfer=payload.transfer,
            transfer_date=payload.transfer_date,
            unit_weight=payload.unit_weight,
            unit_number=payload.unit_number,
            fraction_weight=payload.fraction_weight,
            fraction_number=payload.fraction_number,
            unit_price=payload.unit_price,
            remarks=payload.remarks,
        )
        _apply_upsert_payload(row, payload)
        TePurchaseTransferRepository.create(session, row)
    else:
        _apply_upsert_payload(existing, payload)
        TePurchaseTransferRepository.update(session, existing)
    return TePurchaseTransferUpsertResponse(ok=True)
