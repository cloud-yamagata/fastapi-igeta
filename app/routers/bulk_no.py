"""bulk_no API 雛形（dict 応答・専用スキーマは後から分離可）。"""
from __future__ import annotations

from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_session
from app.entities.bulk_no.model import BulkNo
from app.entities.bulk_no.repository import BulkNoRepository

router = APIRouter(tags=["bulk_no"])


def _cell(v: object) -> object:
    if v is None:
        return None
    if hasattr(v, "isoformat"):
        return v.isoformat()
    if isinstance(v, Decimal):
        return float(v)
    return v


@router.get("/bulk_no/", response_model=list[dict])
def list_bulk_no(session: Session = Depends(get_session)) -> list[dict]:
    rows = BulkNoRepository.list_all(session)
    keys = [c.key for c in BulkNo.__table__.columns]
    return [{k: _cell(getattr(r, k)) for k in keys} for r in rows]
