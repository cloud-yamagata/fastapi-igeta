"""ブレンドロット在庫確定 … te_store_transfer 登録 + lot_status 更新。"""
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.entities.te_blend_lot.repository import TeBlendLotRepository
from app.entities.te_store_transfer.model import TeStoreTransfer

BLEND_LOT_STATUS_COMPLETE = "2"
BLEND_LOT_STATUS_CONFIRMED = "3"
STORE_NO = 3


def _format_finished_lot_no(organic_class: str, product_no: int) -> str:
    return f"{organic_class.strip()}{product_no:05d}"


def _format_part_lot_no(item_group_no: str, product_no: int) -> str:
    return f"{item_group_no.strip()}-{product_no:05d}"


def _work_date_to_transfer_dt(work_date: datetime.date) -> datetime.datetime:
    return datetime.datetime.combine(work_date, datetime.time.min)


def _parse_part_rows(lot_part_info: Any) -> list[dict[str, Any]]:
    if not isinstance(lot_part_info, list):
        return []
    rows: list[dict[str, Any]] = []
    for item in lot_part_info:
        if isinstance(item, dict):
            rows.append(item)
    return rows


def _insert_transfer(
    session: Session,
    *,
    transfer_dt: datetime.datetime,
    item_no: int,
    product_no: int,
    transfer_type: str,
    result_type: str,
    lot_no: str,
    reason: str,
    unit_weight: Decimal,
    transfer_quantity: Decimal,
    remarks: str | None,
) -> int:
    transfer = TeStoreTransfer(
        transfer_date=transfer_dt,
        item_no=int(item_no),
        product_no=int(product_no),
        transfer_type=transfer_type,
        result_type=result_type,
        lot_no=lot_no,
        lot_type="2",
        reason=reason,
        store_no=STORE_NO,
        store_party_name="",
        unit_weight=unit_weight,
        unit_number=1,
        fraction_weight=Decimal("0"),
        fraction_number=0,
        transfer_quantity=transfer_quantity,
        unit_type="Kg",
        remarks=remarks or "",
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
    return int(transfer.transfer_no)


def confirm_blend_lot_stock(session: Session, product_no: int) -> tuple[int, list[int]]:
    row = TeBlendLotRepository.get_by_product_no(session, product_no)
    if row is None:
        raise HTTPException(status_code=404, detail="Blend lot not found")

    current_status = (row.lot_status or "").strip()
    if current_status == BLEND_LOT_STATUS_CONFIRMED:
        raise HTTPException(status_code=400, detail="Blend lot is already confirmed")
    if current_status != BLEND_LOT_STATUS_COMPLETE:
        raise HTTPException(status_code=400, detail="Blend lot status must be complete (2)")

    if row.item_no is None:
        raise HTTPException(status_code=400, detail="item_no is required")

    part_rows = _parse_part_rows(row.lot_part_info)
    if not part_rows:
        raise HTTPException(status_code=400, detail="lot_part_info is required")

    transfer_dt = _work_date_to_transfer_dt(row.work_date)
    unit_weight = Decimal(str(row.unit_weight))
    transfer_nos: list[int] = []

    try:
        finished_no = _insert_transfer(
            session,
            transfer_dt=transfer_dt,
            item_no=int(row.item_no),
            product_no=int(row.product_no),
            transfer_type="1",
            result_type="1",
            lot_no=_format_finished_lot_no(row.organic_class, int(row.product_no)),
            reason="通常品生産",
            unit_weight=unit_weight,
            transfer_quantity=unit_weight,
            remarks=row.remarks,
        )
        transfer_nos.append(finished_no)

        for part in part_rows:
            part_item_no = part.get("item_no")
            part_product_no = part.get("product_no")
            item_group_no = part.get("item_group_no")
            use_quantity = part.get("use_quantity")
            if part_item_no is None or part_product_no is None or item_group_no is None:
                raise HTTPException(status_code=400, detail="Invalid lot_part_info row")
            if use_quantity is None:
                raise HTTPException(status_code=400, detail="use_quantity is required in lot_part_info")

            part_no = _insert_transfer(
                session,
                transfer_dt=transfer_dt,
                item_no=int(part_item_no),
                product_no=int(part_product_no),
                transfer_type="2",
                result_type="2",
                lot_no=_format_part_lot_no(str(item_group_no), int(part_product_no)),
                reason="通常品使用",
                unit_weight=Decimal("0"),
                transfer_quantity=Decimal(str(use_quantity)),
                remarks=None,
            )
            transfer_nos.append(part_no)

        row.lot_status = BLEND_LOT_STATUS_CONFIRMED
        session.commit()
        return int(row.product_no), transfer_nos
    except HTTPException:
        session.rollback()
        raise
    except Exception as exc:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(exc)) from exc
