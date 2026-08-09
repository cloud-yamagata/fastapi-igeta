"""パッケージ製造報告書登録：登録・変更・削除 API。"""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_session
from app.schemas.package_lot_manufacture import (
    PackageLotConfirmStockRequest,
    PackageLotConfirmStockResponse,
    PackageLotCreateRequest,
    PackageLotDeleteRequest,
    PackageLotMutationResponse,
    PackageLotUpdateRequest,
)
from app.services.package_lot_manufacture_service import (
    confirm_package_lot_stock,
    create_package_lot,
    delete_package_lot,
    update_package_lot,
)

router = APIRouter(tags=["package_lot_manufacture"])


@router.post(
    "/package_lot_manufacture/create",
    response_model=PackageLotMutationResponse,
)
def post_package_lot_create(
    payload: PackageLotCreateRequest,
    session: Session = Depends(get_session),
) -> PackageLotMutationResponse:
    product_no = create_package_lot(session, payload)
    return PackageLotMutationResponse(ok=True, product_no=product_no)


@router.post(
    "/package_lot_manufacture/update",
    response_model=PackageLotMutationResponse,
)
def post_package_lot_update(
    payload: PackageLotUpdateRequest,
    session: Session = Depends(get_session),
) -> PackageLotMutationResponse:
    product_no = update_package_lot(session, payload)
    return PackageLotMutationResponse(ok=True, product_no=product_no)


@router.post(
    "/package_lot_manufacture/delete",
    response_model=PackageLotMutationResponse,
)
def post_package_lot_delete(
    payload: PackageLotDeleteRequest,
    session: Session = Depends(get_session),
) -> PackageLotMutationResponse:
    product_no = delete_package_lot(session, payload)
    return PackageLotMutationResponse(ok=True, product_no=product_no)


@router.post(
    "/package_lot_manufacture/confirm_stock",
    response_model=PackageLotConfirmStockResponse,
)
def post_package_lot_confirm_stock(
    payload: PackageLotConfirmStockRequest,
    session: Session = Depends(get_session),
) -> PackageLotConfirmStockResponse:
    product_no, transfer_nos = confirm_package_lot_stock(session, payload)
    return PackageLotConfirmStockResponse(
        ok=True,
        product_no=product_no,
        transfer_nos=transfer_nos,
        lot_status="3",
    )
