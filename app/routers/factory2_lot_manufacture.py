"""第二工場ロット製造登録：変更・削除 API。"""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_session
from app.schemas.factory2_lot_manufacture import (
    Factory2LotCreateRequest,
    Factory2LotDeleteRequest,
    Factory2LotMutationResponse,
    Factory2LotUpdateRequest,
)
from app.services.factory2_lot_manufacture_service import (
    create_factory2_lot,
    delete_factory2_lot,
    update_factory2_lot,
)

router = APIRouter(tags=["factory2_lot_manufacture"])


@router.post(
    "/factory2_lot_manufacture/create",
    response_model=Factory2LotMutationResponse,
)
def post_factory2_lot_create(
    payload: Factory2LotCreateRequest,
    session: Session = Depends(get_session),
) -> Factory2LotMutationResponse:
    lot_no, product_no = create_factory2_lot(session, payload)
    return Factory2LotMutationResponse(ok=True, lot_no=lot_no, product_no=product_no)


@router.post(
    "/factory2_lot_manufacture/update",
    response_model=Factory2LotMutationResponse,
)
def post_factory2_lot_update(
    payload: Factory2LotUpdateRequest,
    session: Session = Depends(get_session),
) -> Factory2LotMutationResponse:
    lot_no = update_factory2_lot(session, payload)
    return Factory2LotMutationResponse(ok=True, lot_no=lot_no, product_no=None)


@router.post(
    "/factory2_lot_manufacture/delete",
    response_model=Factory2LotMutationResponse,
)
def post_factory2_lot_delete(
    payload: Factory2LotDeleteRequest,
    session: Session = Depends(get_session),
) -> Factory2LotMutationResponse:
    lot_no = delete_factory2_lot(session, payload)
    return Factory2LotMutationResponse(ok=True, lot_no=lot_no, product_no=None)
