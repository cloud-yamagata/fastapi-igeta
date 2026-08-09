"""te_factory1_result API（一覧・登録/更新・削除。WPF Factory1Rresult 相当）。"""
from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_session
from app.entities.te_factory1_result.model import TeFactory1Result
from app.entities.te_factory1_result.repository import TeFactory1ResultRepository
from app.entities.te_factory1_transfer.repository import TeFactory1TransferRepository
from app.schemas.te_factory1_result import (
    TeFactory1ResultDeletePayload,
    TeFactory1ResultDeleteResponse,
    TeFactory1ResultUpsertPayload,
    TeFactory1ResultUpsertResponse,
)

router = APIRouter(tags=["te_factory1_result"])


def _cell(v: object) -> object:
    if v is None:
        return None
    if hasattr(v, "isoformat"):
        return v.isoformat()
    if isinstance(v, Decimal):
        return float(v)
    return v


def _apply_upsert_payload(row: TeFactory1Result, payload: TeFactory1ResultUpsertPayload) -> TeFactory1Result:
    row.year = payload.year
    row.work_date = payload.work_date
    row.variety = payload.variety
    row.tea_life = payload.tea_life
    row.grade = payload.grade
    row.tea_rank = payload.tea_rank
    row.field_no = payload.field_no
    row.unit_weight = payload.unit_weight
    row.unit_number = payload.unit_number
    row.fraction_weight = payload.fraction_weight
    row.fraction_number = payload.fraction_number
    row.target = payload.target
    row.remarks = payload.remarks
    row.update_time = datetime.now()
    return row


@router.get("/te_factory1_result/", response_model=list[dict])
def list_te_factory1_result(session: Session = Depends(get_session)) -> list[dict]:
    rows = TeFactory1ResultRepository.list_all(session)
    keys = [c.key for c in TeFactory1Result.__table__.columns]
    return [{k: _cell(getattr(r, k)) for k in keys} for r in rows]


@router.post("/te_factory1_result/upsert", response_model=TeFactory1ResultUpsertResponse)
def upsert_te_factory1_result(
    payload: TeFactory1ResultUpsertPayload,
    session: Session = Depends(get_session),
) -> TeFactory1ResultUpsertResponse:
    existing = TeFactory1ResultRepository.get_by_pk(session, payload.lot_no)
    if existing is None:
        row = TeFactory1Result(
            lot_no=payload.lot_no,
            year=payload.year,
            work_date=payload.work_date,
            variety=payload.variety,
            tea_life=payload.tea_life,
            grade=payload.grade,
            tea_rank=payload.tea_rank,
            field_no=payload.field_no,
            unit_weight=payload.unit_weight,
            unit_number=payload.unit_number,
            fraction_weight=payload.fraction_weight,
            fraction_number=payload.fraction_number,
        )
        _apply_upsert_payload(row, payload)
        TeFactory1ResultRepository.create(session, row)
    else:
        _apply_upsert_payload(existing, payload)
        TeFactory1ResultRepository.update(session, existing)
    return TeFactory1ResultUpsertResponse(ok=True)


@router.post("/te_factory1_result/delete", response_model=TeFactory1ResultDeleteResponse)
def delete_te_factory1_result(
    payload: TeFactory1ResultDeletePayload,
    session: Session = Depends(get_session),
) -> TeFactory1ResultDeleteResponse:
    # WPF: te_factory1_result + te_factory1_transfer を削除
    deleted = TeFactory1ResultRepository.delete_by_pk(session, payload.lot_no)
    if not deleted:
        raise HTTPException(status_code=404, detail="未登録の第1工場生産実績です")
    TeFactory1TransferRepository.delete_by_pk(session, payload.lot_no)
    return TeFactory1ResultDeleteResponse(ok=True)
