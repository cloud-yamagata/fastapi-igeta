"""tr_purchase API 雛形（dict 応答・専用スキーマは後から分離可）。"""
from __future__ import annotations

from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_session
from app.entities.tr_purchase.model import TrPurchase
from app.entities.tr_purchase.repository import TrPurchaseRepository

router = APIRouter(tags=["tr_purchase"])


def _cell(v: object) -> object:
    if v is None:
        return None
    if hasattr(v, "isoformat"):
        return v.isoformat()
    if isinstance(v, Decimal):
        return float(v)
    return v


@router.get("/tr_purchase/", response_model=list[dict])
def list_tr_purchase(session: Session = Depends(get_session)) -> list[dict]:
    rows = TrPurchaseRepository.list_all(session)
    keys = [c.key for c in TrPurchase.__table__.columns]
    return [{k: _cell(getattr(r, k)) for k in keys} for r in rows]
