"""te_factory3_stock API 雛形（dict 応答・専用スキーマは後から分離可）。"""
from __future__ import annotations

from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_session
from app.entities.te_factory3_stock.model import TeFactory3Stock
from app.entities.te_factory3_stock.repository import TeFactory3StockRepository

router = APIRouter(tags=["te_factory3_stock"])


def _cell(v: object) -> object:
    if v is None:
        return None
    if hasattr(v, "isoformat"):
        return v.isoformat()
    if isinstance(v, Decimal):
        return float(v)
    return v


@router.get("/te_factory3_stock/", response_model=list[dict])
def list_te_factory3_stock(session: Session = Depends(get_session)) -> list[dict]:
    rows = TeFactory3StockRepository.list_all(session)
    keys = [c.key for c in TeFactory3Stock.__table__.columns]
    return [{k: _cell(getattr(r, k)) for k in keys} for r in rows]
