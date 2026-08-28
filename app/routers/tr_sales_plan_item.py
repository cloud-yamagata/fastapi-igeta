"""tr_sales_plan_item API（一覧・登録/更新・削除。販売計画商品マスタメンテナンス）。"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.deps import get_session
from app.entities.tr_sales_plan_item.model import TrSalesPlanItem
from app.entities.tr_sales_plan_item.repository import TrSalesPlanItemRepository
from app.schemas.tr_sales_plan_item import (
    TrSalesPlanItemDeletePayload,
    TrSalesPlanItemDeleteResponse,
    TrSalesPlanItemRead,
    TrSalesPlanItemUpsertPayload,
    TrSalesPlanItemUpsertResponse,
)

router = APIRouter(tags=["tr_sales_plan_item"])


@router.get("/tr_sales_plan_item", response_model=list[TrSalesPlanItemRead])
@router.get("/tr_sales_plan_item/", response_model=list[TrSalesPlanItemRead])
def list_tr_sales_plan_item(session: Session = Depends(get_session)) -> list[TrSalesPlanItemRead]:
    rows = TrSalesPlanItemRepository.list_all(session)
    return [TrSalesPlanItemRead.model_validate(r) for r in rows]


def _apply_payload(row: TrSalesPlanItem, payload: TrSalesPlanItemUpsertPayload) -> TrSalesPlanItem:
    row.display_order = payload.display_order
    row.display = payload.display
    row.remarks = payload.remarks
    return row


@router.post("/tr_sales_plan_item/upsert", response_model=TrSalesPlanItemUpsertResponse)
def upsert_tr_sales_plan_item(
    payload: TrSalesPlanItemUpsertPayload,
    session: Session = Depends(get_session),
) -> TrSalesPlanItemUpsertResponse:
    existing = TrSalesPlanItemRepository.get_by_pk(session, payload.item_no)
    try:
        if existing is None:
            row = TrSalesPlanItem(item_no=payload.item_no)
            _apply_payload(row, payload)
            TrSalesPlanItemRepository.create(session, row)
        else:
            _apply_payload(existing, payload)
            TrSalesPlanItemRepository.update(session, existing)
    except IntegrityError as exc:
        session.rollback()
        raise HTTPException(status_code=409, detail="販売計画商品マスタの登録に失敗しました") from exc
    return TrSalesPlanItemUpsertResponse(ok=True)


@router.post("/tr_sales_plan_item/delete", response_model=TrSalesPlanItemDeleteResponse)
def delete_tr_sales_plan_item(
    payload: TrSalesPlanItemDeletePayload,
    session: Session = Depends(get_session),
) -> TrSalesPlanItemDeleteResponse:
    deleted = TrSalesPlanItemRepository.delete_by_pk(session, payload.item_no)
    if not deleted:
        raise HTTPException(status_code=404, detail="未登録の販売計画商品マスタです")
    return TrSalesPlanItemDeleteResponse(ok=True)
