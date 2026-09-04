"""tr_resale API（一覧・登録/更新・削除。WPF ResaleCorrect 相当）。"""
from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.deps import get_session
from app.entities.tr_resale.model import TrResale
from app.entities.tr_resale.repository import TrResaleRepository
from app.schemas.tr_resale import (
    TrResaleDeletePayload,
    TrResaleDeleteResponse,
    TrResaleRead,
    TrResaleUpsertPayload,
    TrResaleUpsertResponse,
)

router = APIRouter(tags=["tr_resale"])


@router.get("/tr_resale", response_model=list[TrResaleRead])
@router.get("/tr_resale/", response_model=list[TrResaleRead])
def list_tr_resale(session: Session = Depends(get_session)) -> list[TrResaleRead]:
    rows = TrResaleRepository.list_all(session)
    return [TrResaleRead.model_validate(r) for r in rows]


def _apply_payload(row: TrResale, payload: TrResaleUpsertPayload) -> TrResale:
    row.rate = payload.rate
    row.postage = payload.postage
    row.limit_price = payload.limit_price
    row.fixed_price = payload.fixed_price
    row.calc_type = payload.calc_type
    row.remarks = payload.remarks
    row.update_time = datetime.now()
    return row


@router.post("/tr_resale/upsert", response_model=TrResaleUpsertResponse)
def upsert_tr_resale(
    payload: TrResaleUpsertPayload,
    session: Session = Depends(get_session),
) -> TrResaleUpsertResponse:
    resale = payload.resale.strip()
    if not resale:
        raise HTTPException(status_code=400, detail="転売先名を入力してください")
    existing = TrResaleRepository.get_by_pk(session, resale)
    try:
        if existing is None:
            row = TrResale(resale=resale)
            _apply_payload(row, payload)
            TrResaleRepository.create(session, row)
        else:
            _apply_payload(existing, payload)
            TrResaleRepository.update(session, existing)
    except IntegrityError as exc:
        session.rollback()
        raise HTTPException(status_code=409, detail="転売先マスタの登録に失敗しました") from exc
    return TrResaleUpsertResponse(ok=True)


@router.post("/tr_resale/delete", response_model=TrResaleDeleteResponse)
def delete_tr_resale(
    payload: TrResaleDeletePayload,
    session: Session = Depends(get_session),
) -> TrResaleDeleteResponse:
    deleted = TrResaleRepository.delete_by_pk(session, payload.resale.strip())
    if not deleted:
        raise HTTPException(status_code=404, detail="未登録の転売先マスタです")
    return TrResaleDeleteResponse(ok=True)
