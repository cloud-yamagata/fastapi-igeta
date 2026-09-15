"""ロット分割 API（WPF LotDivide MaterialRegist 相当）。"""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_session
from app.schemas.lot_divide import LotDivideMaterialRegistRequest, LotDivideMaterialRegistResponse
from app.services.lot_divide_service import material_regist

router = APIRouter(tags=["lot_divide"])


@router.post("/lot_divide/material_regist", response_model=LotDivideMaterialRegistResponse)
def post_lot_divide_material_regist(
    payload: LotDivideMaterialRegistRequest,
    session: Session = Depends(get_session),
) -> LotDivideMaterialRegistResponse:
    serial_no = material_regist(
        session,
        lot_no=payload.lot_no,
        process_type=payload.process_type,
        product_no=payload.product_no,
        lot_name=payload.lot_name,
        item_no=payload.item_no,
        item_name=payload.item_name,
        organic_class=payload.organic_class,
        make_year=payload.make_year,
        count=payload.count,
        factory2_stock=payload.factory2_stock,
        divide_type=payload.divide_type,
        divide_date=payload.divide_date,
        divide_quantity=payload.divide_quantity,
        divide_lot_name=payload.divide_lot_name,
        reason=payload.reason,
        remarks=payload.remarks,
    )
    return LotDivideMaterialRegistResponse(
        ok=True,
        serial_no=serial_no,
        message=f"製造No:{serial_no}として分割されました",
    )
