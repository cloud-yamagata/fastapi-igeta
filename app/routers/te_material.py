"""te_material API"""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_session
from app.entities.te_material.repository import TeMaterialRepository
from app.schemas.te_material import TeMaterialRead

router = APIRouter(tags=["te_material"])


@router.get("/te_material", response_model=list[TeMaterialRead])
@router.get("/te_material/", response_model=list[TeMaterialRead])
def read_te_material(session: Session = Depends(get_session)) -> list[TeMaterialRead]:
    rows = TeMaterialRepository.list_all(session)
    return [TeMaterialRead.model_validate(r) for r in rows]
