"""仕上品仕入登録（WPF StockRepository.Regist 相当）1 トランザクション。

  ① te_material_purchase INSERT → purchase_no 採番
  ② te_store_transfer INSERT（product_no = purchase_no）
  ③ te_lot INSERT（product_no = purchase_no）
"""
from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.entities.te_lot.model import TeLot
from app.entities.te_material_purchase.model import TeMaterialPurchase
from app.entities.te_store_transfer.model import TeStoreTransfer
from app.schemas.material_purchase import MaterialPurchaseCreateRequest, MaterialPurchaseUpdateRequest

# WPF Regist 固定値
TRANSFER_TYPE = "1"
RESULT_TYPE = "4"
LOT_TYPE = "2"
REASON = "仕上品仕入"
STORE_NO = 3
UNIT_TYPE = "Kg"
PROCESS_TYPE = "08"
PROCESS_NAME = "仕上品仕入"


def _parse_purchase_date(text: str) -> datetime:
    t = (text or "").strip()
    if not t:
        raise HTTPException(status_code=400, detail="purchase_date is required")
    if len(t) >= 10 and t[4] in "-/":
        sep = t[4]
        y, m, d = t[:10].split(sep)
        day = date(int(y), int(m), int(d))
        return datetime.combine(day, datetime.min.time())
    raise HTTPException(status_code=400, detail="Invalid purchase_date format")


def create_material_purchase(
    session: Session, payload: MaterialPurchaseCreateRequest
) -> tuple[int, int, int]:
    if payload.item_no <= 0:
        raise HTTPException(status_code=400, detail="item_no is required")
    item_name = (payload.item_name or "").strip()
    if not item_name:
        raise HTTPException(status_code=400, detail="item_name is required")
    purchase_lot_no = (payload.purchase_lot_no or "").strip()
    if not purchase_lot_no:
        raise HTTPException(status_code=400, detail="purchase_lot_no is required")
    supplier = (payload.supplier or "").strip()
    if not supplier:
        raise HTTPException(status_code=400, detail="supplier is required")
    qty = Decimal(str(payload.purchase_quantity))
    if qty <= 0:
        raise HTTPException(status_code=400, detail="仕入れ量の指定が正しくありません")

    purchase_dt = _parse_purchase_date(payload.purchase_date)

    try:
        purchase = TeMaterialPurchase(
            purchase_date=purchase_dt,
            item_no=int(payload.item_no),
            item_name=item_name,
            purchase_lot_no=purchase_lot_no,
            purchase_quantity=qty,
            supplier=supplier,
        )
        session.add(purchase)
        session.flush()
        if purchase.purchase_no is None:
            session.refresh(purchase)
        if purchase.purchase_no is None:
            raise HTTPException(
                status_code=500,
                detail="Failed to allocate purchase_no from DB sequence",
            )
        purchase_no = int(purchase.purchase_no)

        transfer = TeStoreTransfer(
            transfer_date=purchase_dt,
            item_no=int(payload.item_no),
            product_no=purchase_no,
            transfer_type=(payload.transfer_type or TRANSFER_TYPE).strip() or TRANSFER_TYPE,
            result_type=(payload.result_type or RESULT_TYPE).strip() or RESULT_TYPE,
            lot_no=purchase_lot_no,
            lot_type=(payload.lot_type or LOT_TYPE).strip() or LOT_TYPE,
            reason=(payload.reason or REASON).strip() or REASON,
            store_no=int(payload.store_no) if payload.store_no is not None else STORE_NO,
            store_party_name=supplier,
            unit_weight=Decimal("0"),
            unit_number=0,
            fraction_weight=Decimal("0"),
            fraction_number=0,
            transfer_quantity=qty,
            unit_type=(payload.unit_type or UNIT_TYPE).strip() or UNIT_TYPE,
            remarks="",
        )
        session.add(transfer)
        session.flush()
        if transfer.transfer_no is None:
            session.refresh(transfer)
        if transfer.transfer_no is None:
            raise HTTPException(
                status_code=500,
                detail="Failed to allocate transfer_no from DB sequence",
            )
        transfer_no = int(transfer.transfer_no)

        lot = TeLot(
            product_no=purchase_no,
            work_date=purchase_dt,
            process_type=(payload.process_type or PROCESS_TYPE).strip() or PROCESS_TYPE,
            process_name=(payload.process_name or PROCESS_NAME).strip() or PROCESS_NAME,
            lot_name=purchase_lot_no,
            lot_description=item_name,
        )
        session.add(lot)
        session.flush()
        if lot.lot_no is None:
            session.refresh(lot)
        if lot.lot_no is None:
            raise HTTPException(
                status_code=500,
                detail="Failed to allocate lot_no from DB sequence",
            )
        lot_no = int(lot.lot_no)

        session.commit()
        return purchase_no, transfer_no, lot_no
    except HTTPException:
        session.rollback()
        raise
    except Exception as exc:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(exc)) from exc


def update_material_purchase(session: Session, payload: MaterialPurchaseUpdateRequest) -> int:
    """te_material_purchase のみ更新（te_store_transfer / te_lot は更新しない）。"""
    purchase_no = int(payload.purchase_no)
    if purchase_no <= 0:
        raise HTTPException(status_code=400, detail="purchase_no is required")
    if payload.item_no <= 0:
        raise HTTPException(status_code=400, detail="item_no is required")
    item_name = (payload.item_name or "").strip()
    if not item_name:
        raise HTTPException(status_code=400, detail="item_name is required")
    purchase_lot_no = (payload.purchase_lot_no or "").strip()
    if not purchase_lot_no:
        raise HTTPException(status_code=400, detail="purchase_lot_no is required")
    supplier = (payload.supplier or "").strip()
    if not supplier:
        raise HTTPException(status_code=400, detail="supplier is required")
    qty = Decimal(str(payload.purchase_quantity))
    if qty <= 0:
        raise HTTPException(status_code=400, detail="仕入れ量の指定が正しくありません")

    purchase_dt = _parse_purchase_date(payload.purchase_date)

    try:
        row = session.get(TeMaterialPurchase, purchase_no)
        if row is None:
            raise HTTPException(status_code=404, detail="仕入実績が見つかりません")

        row.purchase_date = purchase_dt
        row.item_no = int(payload.item_no)
        row.item_name = item_name
        row.purchase_lot_no = purchase_lot_no
        row.purchase_quantity = qty
        row.supplier = supplier

        session.add(row)
        session.commit()
        return purchase_no
    except HTTPException:
        session.rollback()
        raise
    except Exception as exc:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(exc)) from exc
