"""te_package_categorys_new API（dict 応答）。"""
from __future__ import annotations

from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_session
from app.entities.te_package_categorys_new.model import TePackageCategorysNew
from app.entities.te_package_categorys_new.repository import TePackageCategorysNewRepository

router = APIRouter(tags=["te_package_categorys_new"])


def _cell(v: object) -> object:
    if v is None:
        return None
    if hasattr(v, "isoformat"):
        return v.isoformat()
    if isinstance(v, Decimal):
        return float(v)
    if isinstance(v, (dict, list)):
        return v
    return v


@router.get("/te_package_categorys_new/", response_model=list[dict])
def list_te_package_categorys_new(session: Session = Depends(get_session)) -> list[dict]:
    rows = TePackageCategorysNewRepository.list_all(session)
    keys = [c.key for c in TePackageCategorysNew.__table__.columns]
    return [{k: _cell(getattr(r, k)) for k in keys} for r in rows]
