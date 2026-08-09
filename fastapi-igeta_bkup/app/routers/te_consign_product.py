"""te_consign_product API 雛形（dict 応答・専用スキーマは後から分離可）。"""
from __future__ import annotations

from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_session
from app.entities.te_consign_product.model import TeConsignProduct
from app.entities.te_consign_product.repository import TeConsignProductRepository

router = APIRouter(tags=["te_consign_product"])


def _cell(v: object) -> object:
    if v is None:
        return None
    if hasattr(v, "isoformat"):
        return v.isoformat()
    if isinstance(v, Decimal):
        return float(v)
    return v


@router.get("/te_consign_product/", response_model=list[dict])
def list_te_consign_product(session: Session = Depends(get_session)) -> list[dict]:
    rows = TeConsignProductRepository.list_all(session)
    keys = [c.key for c in TeConsignProduct.__table__.columns]
    return [{k: _cell(getattr(r, k)) for k in keys} for r in rows]
