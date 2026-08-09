"""vi_factory3_stoc API（第3工場仕上茶在庫ビュー）。"""
from __future__ import annotations

from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_session
from app.entities.vi_factory3_stoc.model import ViFactory3Stoc
from app.entities.vi_factory3_stoc.repository import ViFactory3StocRepository

router = APIRouter(tags=["vi_factory3_stoc"])


def _cell(v: object) -> object:
    if v is None:
        return None
    if hasattr(v, "isoformat"):
        return v.isoformat()
    if isinstance(v, Decimal):
        return float(v)
    return v


@router.get("/vi_factory3_stoc/", response_model=list[dict])
def list_vi_factory3_stoc(session: Session = Depends(get_session)) -> list[dict]:
    rows = ViFactory3StocRepository.list_all(session)
    keys = [c.key for c in ViFactory3Stoc.__table__.columns]
    return [{k: _cell(getattr(r, k)) for k in keys} for r in rows]
