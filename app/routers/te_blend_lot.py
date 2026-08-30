"""te_blend_lot API（一覧・登録・更新・削除。BlendLot 画面相当）。"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_session
from app.entities.te_blend_lot.model import TeBlendLot
from app.entities.te_blend_lot.repository import TeBlendLotRepository
from app.schemas.te_blend_lot import (
    BlendLotConfirmStockRequest,
    BlendLotConfirmStockResponse,
    BlendLotDeleteRequest,
    BlendLotDeleteResponse,
    BlendLotUpsertPayload,
    TeBlendLotRead,
)
from app.services.blend_lot_confirm_stock_service import confirm_blend_lot_stock

router = APIRouter(tags=["te_blend_lot"])

DEFAULT_LOT_STATUS = "1"
DEFAULT_ORGANIC_CLASS = "C"


def _normalize_status_code(value: str | None, default: str) -> str:
    code = (value or default).strip()
    return code if code else default


def apply_blend_lot_payload(row: TeBlendLot, payload: BlendLotUpsertPayload) -> TeBlendLot:
    if payload.lot_status is not None:
        row.lot_status = _normalize_status_code(payload.lot_status, row.lot_status)
    if payload.organic_class is not None:
        row.organic_class = _normalize_status_code(payload.organic_class, row.organic_class)
    row.work_date = payload.work_date
    row.item_no = payload.item_no
    row.item_name = payload.item_name.strip()
    row.unit_weight = payload.unit_weight
    row.remarks = payload.remarks
    row.lot_part_info = payload.lot_part_info if payload.lot_part_info is not None else []
    return row


@router.get("/te_blend_lot", response_model=list[TeBlendLotRead])
@router.get("/te_blend_lot/", response_model=list[TeBlendLotRead])
def read_te_blend_lot(session: Session = Depends(get_session)) -> list[TeBlendLotRead]:
    rows = TeBlendLotRepository.list_all(session)
    return [TeBlendLotRead.model_validate(r) for r in rows]


@router.post("/te_blend_lot/delete", response_model=BlendLotDeleteResponse)
def delete_te_blend_lot(
    payload: BlendLotDeleteRequest,
    session: Session = Depends(get_session),
) -> BlendLotDeleteResponse:
    product_nos: list[int] = []
    for target in payload.lots:
        if target.product_no is not None and isinstance(target.product_no, int):
            product_nos.append(target.product_no)
    deleted_count = TeBlendLotRepository.delete_by_product_nos(session, product_nos)
    return BlendLotDeleteResponse(deleted_count=deleted_count)


@router.post("/te_blend_lot/create", response_model=TeBlendLotRead)
def create_te_blend_lot(
    payload: BlendLotUpsertPayload,
    session: Session = Depends(get_session),
) -> TeBlendLotRead:
    if not payload.item_name.strip():
        raise HTTPException(status_code=400, detail="itemName is required")
    row = TeBlendLot(
        lot_status=_normalize_status_code(payload.lot_status, DEFAULT_LOT_STATUS),
        organic_class=_normalize_status_code(payload.organic_class, DEFAULT_ORGANIC_CLASS),
        work_date=payload.work_date,
        item_no=payload.item_no,
        item_name=payload.item_name.strip(),
        unit_weight=payload.unit_weight,
        remarks=payload.remarks,
        lot_part_info=payload.lot_part_info if payload.lot_part_info is not None else [],
    )
    saved = TeBlendLotRepository.persist(session, row)
    return TeBlendLotRead.model_validate(saved)


@router.post("/te_blend_lot/update", response_model=TeBlendLotRead)
def update_te_blend_lot(
    payload: BlendLotUpsertPayload,
    session: Session = Depends(get_session),
) -> TeBlendLotRead:
    if payload.product_no is None:
        raise HTTPException(status_code=400, detail="productNo is required")
    if not payload.item_name.strip():
        raise HTTPException(status_code=400, detail="itemName is required")

    row = TeBlendLotRepository.get_by_product_no(session, payload.product_no)
    if row is None:
        raise HTTPException(status_code=404, detail="Blend lot not found")

    row = apply_blend_lot_payload(row, payload)
    saved = TeBlendLotRepository.persist(session, row)
    return TeBlendLotRead.model_validate(saved)


@router.post("/te_blend_lot/confirm_stock", response_model=BlendLotConfirmStockResponse)
def confirm_te_blend_lot_stock(
    payload: BlendLotConfirmStockRequest,
    session: Session = Depends(get_session),
) -> BlendLotConfirmStockResponse:
    product_no, transfer_nos = confirm_blend_lot_stock(session, payload.product_no)
    return BlendLotConfirmStockResponse(
        ok=True,
        product_no=product_no,
        transfer_nos=transfer_nos,
        lot_status="3",
    )
