"""仕上品仕入登録 API（WPF MaterialPurchase Regist/Update 相当）。"""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_session
from app.schemas.material_purchase import (
    MaterialPurchaseCreateRequest,
    MaterialPurchaseCreateResponse,
    MaterialPurchaseUpdateRequest,
    MaterialPurchaseUpdateResponse,
)
from app.services.material_purchase_service import (
    create_material_purchase,
    update_material_purchase,
)

router = APIRouter(tags=["material_purchase"])


@router.post(
    "/material_purchase/create",
    response_model=MaterialPurchaseCreateResponse,
)
def post_material_purchase_create(
    payload: MaterialPurchaseCreateRequest,
    session: Session = Depends(get_session),
) -> MaterialPurchaseCreateResponse:
    purchase_no, transfer_no, lot_no = create_material_purchase(session, payload)
    return MaterialPurchaseCreateResponse(
        ok=True,
        purchase_no=purchase_no,
        transfer_no=transfer_no,
        lot_no=lot_no,
    )


@router.post(
    "/material_purchase/update",
    response_model=MaterialPurchaseUpdateResponse,
)
def post_material_purchase_update(
    payload: MaterialPurchaseUpdateRequest,
    session: Session = Depends(get_session),
) -> MaterialPurchaseUpdateResponse:
    purchase_no = update_material_purchase(session, payload)
    return MaterialPurchaseUpdateResponse(ok=True, purchase_no=purchase_no)
