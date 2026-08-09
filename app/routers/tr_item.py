"""tr_item API（一覧・登録/更新・削除。WPF ItemCorrect 相当）。"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.deps import get_session
from app.entities.tr_item.model import TrItem
from app.entities.tr_item.repository import TrItemRepository
from app.schemas.tr_item import (
    TrItemDeletePayload,
    TrItemDeleteResponse,
    TrItemRead,
    TrItemUpsertPayload,
    TrItemUpsertResponse,
)

router = APIRouter(tags=["tr_item"])


@router.get("/tr_item", response_model=list[TrItemRead])
@router.get("/tr_item/", response_model=list[TrItemRead])
def read_tr_item(session: Session = Depends(get_session)) -> list[TrItemRead]:
    rows = TrItemRepository.list_all(session)
    return [TrItemRead.model_validate(r) for r in rows]


def _apply_payload(row: TrItem, payload: TrItemUpsertPayload) -> TrItem:
    row.system_class = payload.system_class
    row.organic_class = payload.organic_class
    row.item_group_no = payload.item_group_no
    row.item_name = payload.item_name
    row.jan_code = payload.jan_code
    row.package_size = payload.package_size
    row.display_order = payload.display_order
    row.display = payload.display
    row.remarks = payload.remarks
    return row


@router.post("/tr_item/upsert", response_model=TrItemUpsertResponse)
def upsert_tr_item(
    payload: TrItemUpsertPayload,
    session: Session = Depends(get_session),
) -> TrItemUpsertResponse:
    existing = TrItemRepository.get_by_item_no(session, payload.item_no)
    try:
        if existing is None:
            row = TrItem(item_no=payload.item_no, system_class=payload.system_class, organic_class=payload.organic_class, item_group_no=payload.item_group_no, item_name=payload.item_name, jan_code=payload.jan_code, package_size=payload.package_size, display_order=payload.display_order)
            _apply_payload(row, payload)
            TrItemRepository.create(session, row)
        else:
            _apply_payload(existing, payload)
            TrItemRepository.update(session, existing)
    except IntegrityError as exc:
        session.rollback()
        raise HTTPException(status_code=409, detail="入力した商品名は既に使用されております。") from exc
    return TrItemUpsertResponse(ok=True)


@router.post("/tr_item/delete", response_model=TrItemDeleteResponse)
def delete_tr_item(
    payload: TrItemDeletePayload,
    session: Session = Depends(get_session),
) -> TrItemDeleteResponse:
    deleted = TrItemRepository.delete_by_item_no(session, payload.item_no)
    if not deleted:
        raise HTTPException(status_code=404, detail="未登録の商品マスタです")
    return TrItemDeleteResponse(ok=True)
