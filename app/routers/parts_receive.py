"""仕上品受入 API（WPF PartsReceive 相当）。"""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_session
from app.schemas.parts_receive import (
    PartsReceiveReceiveRequest,
    PartsReceiveReceiveResponse,
    PartsReceiveStockRow,
)
from app.services.parts_receive_service import list_parts_receive_stocks, receive_parts

router = APIRouter(tags=["parts_receive"])


@router.get("/parts_receive/stocks", response_model=list[PartsReceiveStockRow])
@router.get("/parts_receive/stocks/", response_model=list[PartsReceiveStockRow])
def get_parts_receive_stocks(session: Session = Depends(get_session)) -> list[PartsReceiveStockRow]:
    rows = list_parts_receive_stocks(session)
    return [PartsReceiveStockRow.model_validate(r) for r in rows]


@router.post("/parts_receive/receive", response_model=PartsReceiveReceiveResponse)
def post_parts_receive_receive(
    payload: PartsReceiveReceiveRequest,
    session: Session = Depends(get_session),
) -> PartsReceiveReceiveResponse:
    receive_parts(
        session,
        item_no=payload.item_no,
        product_no=payload.product_no,
        transfer_quantity=payload.transfer_quantity,
        transfer_date=payload.transfer_date,
        store_no=payload.store_no,
    )
    return PartsReceiveReceiveResponse(ok=True)
