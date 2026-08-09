"""vi_factory2_stock API（第二工場ロット在庫ビュー・在庫重量>0のみ）。"""
from __future__ import annotations

from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_session
from app.entities.vi_factory2_stock.model import ViFactory2Stock
from app.entities.vi_factory2_stock.repository import ViFactory2StockRepository

router = APIRouter(tags=["vi_factory2_stock"])


def _cell(v: object) -> object:
    if v is None:
        return None
    if hasattr(v, "isoformat"):
        return v.isoformat()
    if isinstance(v, Decimal):
        return float(v)
    return v


@router.get("/vi_factory2_stock/", response_model=list[dict])
def list_vi_factory2_stock(session: Session = Depends(get_session)) -> list[dict]:
    rows = ViFactory2StockRepository.list_in_stock(session)
    keys = [c.key for c in ViFactory2Stock.__table__.columns]
    return [{k: _cell(r.get(k)) for k in keys} for r in rows]
