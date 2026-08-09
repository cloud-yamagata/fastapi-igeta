"""finish_no API 雛形（dict 応答・専用スキーマは後から分離可）。"""
from __future__ import annotations

from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_session
from app.entities.finish_no.model import FinishNo
from app.entities.finish_no.repository import FinishNoRepository

router = APIRouter(tags=["finish_no"])


def _cell(v: object) -> object:
    if v is None:
        return None
    if hasattr(v, "isoformat"):
        return v.isoformat()
    if isinstance(v, Decimal):
        return float(v)
    return v


@router.get("/finish_no/", response_model=list[dict])
def list_finish_no(session: Session = Depends(get_session)) -> list[dict]:
    rows = FinishNoRepository.list_all(session)
    keys = [c.key for c in FinishNo.__table__.columns]
    return [{k: _cell(getattr(r, k)) for k in keys} for r in rows]
