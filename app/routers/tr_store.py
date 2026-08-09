"""tr_store API 雛形（dict 応答・専用スキーマは後から分離可）。"""
from __future__ import annotations

from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_session
from app.entities.tr_store.model import TrStore
from app.entities.tr_store.repository import TrStoreRepository

router = APIRouter(tags=["tr_store"])


def _cell(v: object) -> object:
    if v is None:
        return None
    if hasattr(v, "isoformat"):
        return v.isoformat()
    if isinstance(v, Decimal):
        return float(v)
    return v


@router.get("/tr_store/", response_model=list[dict])
def list_tr_store(session: Session = Depends(get_session)) -> list[dict]:
    rows = TrStoreRepository.list_all(session)
    keys = [c.key for c in TrStore.__table__.columns]
    return [{k: _cell(getattr(r, k)) for k in keys} for r in rows]
