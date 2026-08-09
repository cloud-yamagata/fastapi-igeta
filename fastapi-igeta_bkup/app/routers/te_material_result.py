"""te_material_result API（一覧・登録/更新・削除。WPF MaterialRresult 相当）。"""
from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_session
from app.entities.te_material_result.model import TeMaterialResult
from app.entities.te_material_result.repository import TeMaterialResultRepository
from app.schemas.te_material_result import (
    TeMaterialResultDeletePayload,
    TeMaterialResultDeleteResponse,
    TeMaterialResultUpsertPayload,
    TeMaterialResultUpsertResponse,
)

router = APIRouter(tags=["te_material_result"])


def _cell(v: object) -> object:
    if v is None:
        return None
    if hasattr(v, "isoformat"):
        return v.isoformat()
    if isinstance(v, Decimal):
        return float(v)
    return v


def _apply_upsert_payload(row: TeMaterialResult, payload: TeMaterialResultUpsertPayload) -> TeMaterialResult:
    row.tea_type = payload.tea_type
    row.tea_life = payload.tea_life
    row.organic_class = payload.organic_class
    row.producer = payload.producer
    row.material_name = payload.material_name
    row.unit_weight = payload.unit_weight
    row.unit_number = payload.unit_number
    row.fraction_weight = payload.fraction_weight
    row.fraction_number = payload.fraction_number
    row.remarks = payload.remarks
    row.update_time = datetime.now()
    return row


@router.get("/te_material_result/", response_model=list[dict])
def list_te_material_result(session: Session = Depends(get_session)) -> list[dict]:
    rows = TeMaterialResultRepository.list_all(session)
    keys = [c.key for c in TeMaterialResult.__table__.columns]
    return [{k: _cell(getattr(r, k)) for k in keys} for r in rows]


@router.post("/te_material_result/upsert", response_model=TeMaterialResultUpsertResponse)
def upsert_te_material_result(
    payload: TeMaterialResultUpsertPayload,
    session: Session = Depends(get_session),
) -> TeMaterialResultUpsertResponse:
    existing = TeMaterialResultRepository.get_by_pk(
        session,
        payload.year,
        payload.purchase,
        payload.product_no,
        payload.purchase_date,
        payload.tea_rank,
        payload.rank,
    )
    if existing is None:
        row = TeMaterialResult(
            year=payload.year,
            purchase=payload.purchase,
            product_no=payload.product_no,
            purchase_date=payload.purchase_date,
            tea_rank=payload.tea_rank,
            rank=payload.rank,
            organic_class=payload.organic_class,
            material_name=payload.material_name,
            unit_weight=payload.unit_weight,
            unit_number=payload.unit_number,
            fraction_weight=payload.fraction_weight,
            fraction_number=payload.fraction_number,
        )
        _apply_upsert_payload(row, payload)
        TeMaterialResultRepository.create(session, row)
    else:
        _apply_upsert_payload(existing, payload)
        TeMaterialResultRepository.update(session, existing)
    return TeMaterialResultUpsertResponse(ok=True)


@router.post("/te_material_result/delete", response_model=TeMaterialResultDeleteResponse)
def delete_te_material_result(
    payload: TeMaterialResultDeletePayload,
    session: Session = Depends(get_session),
) -> TeMaterialResultDeleteResponse:
    deleted = TeMaterialResultRepository.delete_by_pk(
        session,
        payload.year,
        payload.purchase,
        payload.product_no,
        payload.purchase_date,
        payload.tea_rank,
        payload.rank,
    )
    if not deleted:
        raise HTTPException(status_code=404, detail="未登録の原料実績です")
    return TeMaterialResultDeleteResponse(ok=True)
