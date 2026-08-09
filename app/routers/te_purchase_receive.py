"""te_purchase_receive API 雛形（dict 応答・専用スキーマは後から分離可）。"""
from __future__ import annotations

from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_session
from app.entities.te_purchase_receive.model import TePurchaseReceive
from app.entities.te_purchase_receive.repository import TePurchaseReceiveRepository

router = APIRouter(tags=["te_purchase_receive"])


def _cell(v: object) -> object:
    if v is None:
        return None
    if hasattr(v, "isoformat"):
        return v.isoformat()
    if isinstance(v, Decimal):
        return float(v)
    return v


@router.get("/te_purchase_receive/", response_model=list[dict])
def list_te_purchase_receive(session: Session = Depends(get_session)) -> list[dict]:
    rows = TePurchaseReceiveRepository.list_all(session)
    keys = [c.key for c in TePurchaseReceive.__table__.columns]
    return [{k: _cell(getattr(r, k)) for k in keys} for r in rows]
