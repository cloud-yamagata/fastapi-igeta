"""te_store_transfer_fa2 API（一覧・登録・変更。WPF StoreTransferFa2 相当）。"""
from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.deps import get_session
from app.entities.te_store_transfer_fa2.model import TeStoreTransferFa2
from app.entities.te_store_transfer_fa2.repository import TeStoreTransferFa2Repository
from app.schemas.te_store_transfer_fa2 import (
    TeStoreTransferFa2CreatePayload,
    TeStoreTransferFa2CreateResponse,
    TeStoreTransferFa2UpdatePayload,
    TeStoreTransferFa2UpdateResponse,
)

router = APIRouter(tags=["te_store_transfer_fa2"])


def _cell(v: object) -> object:
    if v is None:
        return None
    if hasattr(v, "isoformat"):
        return v.isoformat()
    if isinstance(v, Decimal):
        return float(v)
    return v


@router.get("/te_store_transfer_fa2", response_model=list[dict])
@router.get("/te_store_transfer_fa2/", response_model=list[dict])
def list_te_store_transfer_fa2(session: Session = Depends(get_session)) -> list[dict]:
    rows = TeStoreTransferFa2Repository.list_all(session)
    keys = [c.key for c in TeStoreTransferFa2.__table__.columns]
    return [{k: _cell(getattr(r, k)) for k in keys} for r in rows]


@router.post("/te_store_transfer_fa2/create", response_model=TeStoreTransferFa2CreateResponse)
def create_te_store_transfer_fa2(
    payload: TeStoreTransferFa2CreatePayload,
    session: Session = Depends(get_session),
) -> TeStoreTransferFa2CreateResponse:
    """登録モード（EditType=1）。WPF 入出庫情報登録相当。"""
    max_no = session.scalar(select(func.max(TeStoreTransferFa2.transfer_no))) or 0
    row = TeStoreTransferFa2(
        transfer_no=int(max_no) + 1,
        transfer_date=payload.transfer_date,
        lot_no=payload.lot_no,
        process_type=payload.process_type,
        product_no=payload.product_no,
        lot_name=payload.lot_name,
        transfer_type=payload.transfer_type,
        result_type=payload.result_type,
        lot_type=payload.lot_type,
        reason=payload.reason,
        unit_weight=payload.unit_weight,
        unit_number=payload.unit_number,
        fraction_weight=payload.fraction_weight,
        fraction_number=payload.fraction_number,
        transfer_quantity=payload.transfer_quantity,
        unit_type=payload.unit_type,
        remarks=payload.remarks,
        update_time=datetime.now(),
    )
    try:
        created = TeStoreTransferFa2Repository.create(session, row)
    except IntegrityError as exc:
        session.rollback()
        raise HTTPException(status_code=409, detail="入力した入出庫情報は既に使用されております。") from exc
    return TeStoreTransferFa2CreateResponse(ok=True, transfer_no=created.transfer_no)


@router.post("/te_store_transfer_fa2/update", response_model=TeStoreTransferFa2UpdateResponse)
def update_te_store_transfer_fa2(
    payload: TeStoreTransferFa2UpdatePayload,
    session: Session = Depends(get_session),
) -> TeStoreTransferFa2UpdateResponse:
    """変更モード（EditType=2）。WPF 入出庫情報更新相当。"""
    row = TeStoreTransferFa2Repository.get_by_pk(session, payload.transfer_no)
    if row is None:
        raise HTTPException(status_code=404, detail="未登録の入出庫情報です")

    if payload.transfer_date is not None:
        row.transfer_date = payload.transfer_date
    row.reason = payload.reason
    row.unit_weight = payload.unit_weight
    row.unit_number = payload.unit_number
    row.fraction_weight = payload.fraction_weight
    row.fraction_number = payload.fraction_number
    row.transfer_quantity = payload.transfer_quantity
    row.remarks = payload.remarks
    row.update_time = datetime.now()

    TeStoreTransferFa2Repository.update(session, row)
    return TeStoreTransferFa2UpdateResponse(ok=True)
