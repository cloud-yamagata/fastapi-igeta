"""te_store_transfer API（一覧・登録・変更。第3工場入出庫情報メンテナンス相当）。"""
from __future__ import annotations

from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.deps import get_session
from app.entities.te_store_transfer.model import TeStoreTransfer
from app.entities.te_store_transfer.repository import TeStoreTransferRepository
from app.schemas.te_store_transfer import (
    TeStoreTransferCreatePayload,
    TeStoreTransferCreateResponse,
    TeStoreTransferUpdatePayload,
    TeStoreTransferUpdateResponse,
)

router = APIRouter(tags=["te_store_transfer"])


def _cell(v: object) -> object:
    if v is None:
        return None
    if hasattr(v, "isoformat"):
        return v.isoformat()
    if isinstance(v, Decimal):
        return float(v)
    return v


@router.get("/te_store_transfer", response_model=list[dict])
@router.get("/te_store_transfer/", response_model=list[dict])
def list_te_store_transfer(session: Session = Depends(get_session)) -> list[dict]:
    rows = TeStoreTransferRepository.list_all(session)
    keys = [c.key for c in TeStoreTransfer.__table__.columns]
    return [{k: _cell(getattr(r, k)) for k in keys} for r in rows]


@router.post("/te_store_transfer/create", response_model=TeStoreTransferCreateResponse)
def create_te_store_transfer(
    payload: TeStoreTransferCreatePayload,
    session: Session = Depends(get_session),
) -> TeStoreTransferCreateResponse:
    """登録モード（EditType=1）。"""
    row = TeStoreTransfer(
        transfer_date=payload.transfer_date,
        item_no=payload.item_no,
        product_no=payload.product_no,
        transfer_type=payload.transfer_type,
        result_type=payload.result_type,
        lot_no=payload.lot_no,
        lot_type=payload.lot_type,
        reason=payload.reason,
        store_no=payload.store_no,
        store_party_name=payload.store_party_name,
        unit_weight=payload.unit_weight,
        unit_number=payload.unit_number,
        fraction_weight=payload.fraction_weight,
        fraction_number=payload.fraction_number,
        transfer_quantity=payload.transfer_quantity,
        unit_type=payload.unit_type,
        remarks=payload.remarks,
    )
    try:
        session.add(row)
        session.flush()
        if row.transfer_no is None:
            session.refresh(row)
        if row.transfer_no is None:
            raise HTTPException(
                status_code=500,
                detail="Failed to allocate transfer_no from DB sequence",
            )
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise HTTPException(status_code=409, detail="入力した入出庫情報は既に使用されております。") from exc
    except HTTPException:
        session.rollback()
        raise
    except Exception as exc:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return TeStoreTransferCreateResponse(ok=True, transfer_no=row.transfer_no)


@router.post("/te_store_transfer/update", response_model=TeStoreTransferUpdateResponse)
def update_te_store_transfer(
    payload: TeStoreTransferUpdatePayload,
    session: Session = Depends(get_session),
) -> TeStoreTransferUpdateResponse:
    """変更モード（EditType=2）。"""
    row = TeStoreTransferRepository.get_by_pk(session, payload.transfer_no)
    if row is None:
        raise HTTPException(status_code=404, detail="未登録の入出庫情報です")

    if payload.transfer_date is not None:
        row.transfer_date = payload.transfer_date
    row.reason = payload.reason
    row.store_party_name = payload.store_party_name
    if payload.unit_weight is not None:
        row.unit_weight = payload.unit_weight
    if payload.unit_number is not None:
        row.unit_number = payload.unit_number
    if payload.fraction_weight is not None:
        row.fraction_weight = payload.fraction_weight
    if payload.fraction_number is not None:
        row.fraction_number = payload.fraction_number
    row.transfer_quantity = payload.transfer_quantity
    row.remarks = payload.remarks

    try:
        TeStoreTransferRepository.update(session, row)
    except IntegrityError as exc:
        session.rollback()
        raise HTTPException(status_code=409, detail="入力した入出庫情報は既に使用されております。") from exc
    return TeStoreTransferUpdateResponse(ok=True)
