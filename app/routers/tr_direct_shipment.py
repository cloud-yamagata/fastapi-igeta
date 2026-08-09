"""tr_direct_shipment API（一覧・登録/更新・削除。WPF ShipmentCorrect 相当）。"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.deps import get_session
from app.entities.tr_direct_shipment.model import TrDirectShipment
from app.entities.tr_direct_shipment.repository import TrDirectShipmentRepository
from app.schemas.tr_direct_shipment import (
    TrDirectShipmentDeletePayload,
    TrDirectShipmentDeleteResponse,
    TrDirectShipmentRead,
    TrDirectShipmentUpsertPayload,
    TrDirectShipmentUpsertResponse,
)

router = APIRouter(tags=["tr_direct_shipment"])


@router.get("/tr_direct_shipment", response_model=list[TrDirectShipmentRead])
@router.get("/tr_direct_shipment/", response_model=list[TrDirectShipmentRead])
def list_tr_direct_shipment(session: Session = Depends(get_session)) -> list[TrDirectShipmentRead]:
    rows = TrDirectShipmentRepository.list_all(session)
    return [TrDirectShipmentRead.model_validate(r) for r in rows]


def _apply_payload(row: TrDirectShipment, payload: TrDirectShipmentUpsertPayload) -> TrDirectShipment:
    row.direct_shipment_name = payload.direct_shipment_name
    row.direct_shipment_kana = payload.direct_shipment_kana
    row.zip = payload.zip
    row.address = payload.address
    row.phone_no = payload.phone_no
    row.fax_no = payload.fax_no
    row.display_order = payload.display_order
    row.remarks = payload.remarks
    return row


@router.post("/tr_direct_shipment/upsert", response_model=TrDirectShipmentUpsertResponse)
def upsert_tr_direct_shipment(
    payload: TrDirectShipmentUpsertPayload,
    session: Session = Depends(get_session),
) -> TrDirectShipmentUpsertResponse:
    existing = TrDirectShipmentRepository.get_by_pk(session, payload.direct_shipment_no)
    try:
        if existing is None:
            row = TrDirectShipment(direct_shipment_no=payload.direct_shipment_no)
            _apply_payload(row, payload)
            TrDirectShipmentRepository.create(session, row)
        else:
            _apply_payload(existing, payload)
            TrDirectShipmentRepository.update(session, existing)
    except IntegrityError as exc:
        session.rollback()
        raise HTTPException(status_code=409, detail="直送先マスタの登録に失敗しました") from exc
    return TrDirectShipmentUpsertResponse(ok=True)


@router.post("/tr_direct_shipment/delete", response_model=TrDirectShipmentDeleteResponse)
def delete_tr_direct_shipment(
    payload: TrDirectShipmentDeletePayload,
    session: Session = Depends(get_session),
) -> TrDirectShipmentDeleteResponse:
    deleted = TrDirectShipmentRepository.delete_by_pk(session, payload.direct_shipment_no)
    if not deleted:
        raise HTTPException(status_code=404, detail="未登録の直送先マスタです")
    return TrDirectShipmentDeleteResponse(ok=True)
