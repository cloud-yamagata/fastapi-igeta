"""te_grade API 雛形（dict 応答・専用スキーマは後から分離可）。"""
from __future__ import annotations

from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_session
from app.entities.te_grade.model import TeGrade
from app.entities.te_grade.repository import TeGradeRepository

router = APIRouter(tags=["te_grade"])


def _cell(v: object) -> object:
    if v is None:
        return None
    if hasattr(v, "isoformat"):
        return v.isoformat()
    if isinstance(v, Decimal):
        return float(v)
    return v


@router.get("/te_grade/", response_model=list[dict])
def list_te_grade(session: Session = Depends(get_session)) -> list[dict]:
    rows = TeGradeRepository.list_all(session)
    keys = [c.key for c in TeGrade.__table__.columns]
    return [{k: _cell(getattr(r, k)) for k in keys} for r in rows]
