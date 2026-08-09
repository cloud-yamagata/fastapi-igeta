"""tr_constant API"""
from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.deps import get_session
from app.entities.tr_constant.repository import TrConstantRepository
from app.schemas.tr_constant import TrConstantRead

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
