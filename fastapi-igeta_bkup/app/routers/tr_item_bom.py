"""tr_item_bom API（一覧・登録/更新・削除。WPF ItemBomCorrect 相当）。"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.deps import get_session
from app.entities.tr_item_bom.model import TrItemBom
from app.entities.tr_item_bom.repository import TrItemBomRepository
from app.schemas.tr_item_bom import (
    TrItemBomDeletePayload,
    TrItemBomDeleteResponse,
    TrItemBomRead,
    TrItemBomUpsertPayload,
    TrItemBomUpsertResponse,
)

router = APIRouter(tags=["tr_item_bom"])


@router.get("/tr_item_bom", response_model=list[TrItemBomRead])
@router.get("/tr_item_bom/", response_model=list[TrItemBomRead])
def list_tr_item_bom(session: Session = Depends(get_session)) -> list[TrItemBomRead]:
    rows = TrItemBomRepository.list_all(session)
    return [TrItemBomRead.model_validate(r) for r in rows]


@router.post("/tr_item_bom/upsert", response_model=TrItemBomUpsertResponse)
def upsert_tr_item_bom(
    payload: TrItemBomUpsertPayload,
    session: Session = Depends(get_session),
) -> TrItemBomUpsertResponse:
    existing = TrItemBomRepository.get_by_pk(session, payload.parent_item_no)
    try:
        if existing is None:
            row = TrItemBom(
                parent_item_no=payload.parent_item_no,
                child_item_no=payload.child_item_no,
            )
            TrItemBomRepository.create(session, row)
        else:
            existing.child_item_no = payload.child_item_no
            TrItemBomRepository.update(session, existing)
    except IntegrityError as exc:
        session.rollback()
        raise HTTPException(status_code=409, detail="商品原料対照表の登録に失敗しました") from exc
    return TrItemBomUpsertResponse(ok=True)


@router.post("/tr_item_bom/delete", response_model=TrItemBomDeleteResponse)
def delete_tr_item_bom(
    payload: TrItemBomDeletePayload,
    session: Session = Depends(get_session),
) -> TrItemBomDeleteResponse:
    deleted = TrItemBomRepository.delete_by_pk(session, payload.parent_item_no)
    if not deleted:
        raise HTTPException(status_code=404, detail="未登録の商品原料対照表です")
    return TrItemBomDeleteResponse(ok=True)
