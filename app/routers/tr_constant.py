"""tr_constant API（一覧・登録/更新・削除。システム定数メンテナンス相当）。"""
from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.deps import get_session
from app.entities.tr_constant.model import TrConstant
from app.entities.tr_constant.repository import TrConstantRepository
from app.schemas.tr_constant import (
    TrConstantDeletePayload,
    TrConstantDeleteResponse,
    TrConstantRead,
    TrConstantUpsertPayload,
    TrConstantUpsertResponse,
)

router = APIRouter(tags=["tr_constant"])


@router.get("/tr_constant", response_model=list[TrConstantRead])
@router.get("/tr_constant/", response_model=list[TrConstantRead])
def read_tr_constant(
    const_field: Optional[str] = Query(None),
    session: Session = Depends(get_session),
) -> list[TrConstantRead]:
    """システム定数。const_field を指定したときはその項目のみ。並び: const → display_order"""
    rows = TrConstantRepository.list_filtered(session, const_field)
    return [TrConstantRead.model_validate(r) for r in rows]


@router.post("/tr_constant/upsert", response_model=TrConstantUpsertResponse)
def upsert_tr_constant(
    payload: TrConstantUpsertPayload,
    session: Session = Depends(get_session),
) -> TrConstantUpsertResponse:
    const_field = payload.const_field.strip()
    const_value = payload.const_value.strip()
    const_name = payload.const_name.strip()
    if not const_field or not const_value or not const_name:
        raise HTTPException(status_code=400, detail="定数項目・定数値・定数名は必須です")

    existing = TrConstantRepository.get_by_natural_key(session, const_field, const_value)
    try:
        if existing is None:
            row = TrConstant(
                const_field=const_field,
                const_value=const_value,
                const_name=const_name,
                display_order=payload.display_order,
                display=payload.display,
            )
            TrConstantRepository.create(session, row)
        else:
            existing.const_name = const_name
            existing.display_order = payload.display_order
            existing.display = payload.display
            TrConstantRepository.update(session, existing)
    except IntegrityError as exc:
        session.rollback()
        raise HTTPException(status_code=409, detail="システム定数の登録に失敗しました") from exc
    return TrConstantUpsertResponse(ok=True)


@router.post("/tr_constant/delete", response_model=TrConstantDeleteResponse)
def delete_tr_constant(
    payload: TrConstantDeletePayload,
    session: Session = Depends(get_session),
) -> TrConstantDeleteResponse:
    const_field = payload.const_field.strip()
    const_value = payload.const_value.strip()
    if not const_field or not const_value:
        raise HTTPException(status_code=400, detail="定数項目・定数値は必須です")

    deleted = TrConstantRepository.delete_by_natural_key(session, const_field, const_value)
    if not deleted:
        raise HTTPException(status_code=404, detail="未登録のシステム定数です")
    return TrConstantDeleteResponse(ok=True)
