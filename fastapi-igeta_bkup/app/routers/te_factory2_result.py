"""te_factory2_result API 雛形（dict 応答・専用スキーマは後から分離可）。"""
from __future__ import annotations

from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_session
from app.entities.te_factory2_result.model import TeFactory2Result
from app.entities.te_factory2_result.repository import TeFactory2ResultRepository

router = APIRouter(tags=["te_factory2_result"])


def _cell(v: object) -> object:
    if v is None:
        return None
    if hasattr(v, "isoformat"):
        return v.isoformat()
    if isinstance(v, Decimal):
        return float(v)
    return v


@router.get("/te_factory2_result/", response_model=list[dict])
def list_te_factory2_result(session: Session = Depends(get_session)) -> list[dict]:
    rows = TeFactory2ResultRepository.list_all(session)
    keys = [c.key for c in TeFactory2Result.__table__.columns]
    return [{k: _cell(getattr(r, k)) for k in keys} for r in rows]
