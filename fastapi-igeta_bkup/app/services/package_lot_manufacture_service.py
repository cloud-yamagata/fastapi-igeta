"""パッケージ製造報告書登録：登録・変更・削除の DB 更新（1 トランザクション）。

登録時:
  ① package_no INSERT → serial_no 採番（製造No）
  ② te_package_base_new INSERT（product_no = ① の serial_no）
  ③ te_package_categorys_new INSERT（product_no = ① の serial_no）
変更時:
  ① te_package_base_new UPDATE
  ② te_package_categorys_new UPDATE（無ければ INSERT）
削除時:
  ① te_package_categorys_new DELETE
  ② te_package_base_new DELETE
在庫確定時:
  ① te_package_base_new UPDATE（lot_status = 3）
  ② te_store_transfer INSERT
"""
from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Any

from fastapi import HTTPException
from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.entities.package_no.model import PackageNo
from app.entities.te_package_base_new.model import TePackageBaseNew
from app.entities.te_package_categorys_new.model import TePackageCategorysNew
from app.entities.te_store_transfer.model import TeStoreTransfer
from app.schemas.package_lot_manufacture import (
    PackageLotBaseFieldsPayload,
    PackageLotCategoryFieldsPayload,
    PackageLotConfirmStockRequest,
    PackageLotCreateRequest,
    PackageLotDeleteRequest,
    PackageLotUpdateRequest,
)

PACKAGE_LOT_STATUS_COMPLETE = "2"
PACKAGE_LOT_STATUS_CONFIRMED = "3"


def _parse_work_date(text: str) -> date:
    t = text.strip()
    if not t:
        raise HTTPException(status_code=400, detail="work_date is required")
    if len(t) >= 10 and t[4] == "-":
        y, m, d = t[:10].split("-")
        return date(int(y), int(m), int(d))
    if len(t) >= 10 and t[4] == "/":
        y, m, d = t[:10].split("/")
        return date(int(y), int(m), int(d))
    raise HTTPException(status_code=400, detail="Invalid work_date format")


def _normalize_organic_class(code: str) -> str:
    organic = (code or "C").strip().upper()[:1] or "C"
    return organic


def _lot_part_info_to_json(
    parts: list[Any] | None,
) -> list[dict[str, Any]] | None:
    if not parts:
        return None
    rows: list[dict[str, Any]] = []
    for part in parts:
        row: dict[str, Any] = {"part_lot_no": int(part.part_lot_no)}
        if part.out_quantity is not None:
            row["out_quantity"] = part.out_quantity
        if part.rem_quantity is not None:
            row["rem_quantity"] = part.rem_quantity
        if part.use_quantity is not None:
            row["use_quantity"] = part.use_quantity
        rows.append(row)
    return rows or None


def _apply_base_fields(base: TePackageBaseNew, bf: PackageLotBaseFieldsPayload) -> None:
    base.lot_status = (bf.lot_status or "1").strip()[:1] or "1"
    base.organic_class = _normalize_organic_class(bf.organic_class)
    base.item_no = int(bf.item_no)
    base.product_name = bf.product_name
    base.work_date = _parse_work_date(bf.work_date)
    base.complete_quantity = int(bf.complete_quantity)
    base.sample_quantity = int(bf.sample_quantity)
    base.fail_quantity = int(bf.fail_quantity)
    base.use_tea_no = int(bf.use_tea_no) if bf.use_tea_no is not None else None
    base.part_name = bf.part_name
    base.remarks = bf.remarks
    base.lot_part_info = _lot_part_info_to_json(bf.lot_part_info)


def _apply_category_fields(
    category: TePackageCategorysNew,
    cf: PackageLotCategoryFieldsPayload,
) -> None:
    category.temperature = cf.temperature
    category.humidity = cf.humidity
    category.packing_start_hh = cf.packing_start_hh
    category.packing_start_mm = cf.packing_start_mm
    category.packing_end_hh = cf.packing_end_hh
    category.packing_end_mm = cf.packing_end_mm
    category.work_before_cleaning_start_hh = cf.work_before_cleaning_start_hh
    category.work_before_cleaning_start_mm = cf.work_before_cleaning_start_mm
    category.work_before_cleaning_end_hh = cf.work_before_cleaning_end_hh
    category.work_before_cleaning_end_mm = cf.work_before_cleaning_end_mm
    category.work_end_cleaning_start_hh = cf.work_end_cleaning_start_hh
    category.work_end_cleaning_start_mm = cf.work_end_cleaning_start_mm
    category.work_end_cleaning_end_hh = cf.work_end_cleaning_end_hh
    category.work_end_cleaning_end_mm = cf.work_end_cleaning_end_mm
    category.hp500_no1_chk = cf.hp500_no1_chk
    category.hp500_no2_chk = cf.hp500_no2_chk
    category.fr2_chk = cf.fr2_chk
    category.fpg_chk = cf.fpg_chk
    category.uba_chk = cf.uba_chk
    category.lift_cleaning_before_chk = cf.lift_cleaning_before_chk
    category.lift_cleaning_after_chk = cf.lift_cleaning_after_chk
    category.lift_operation_before_chk = cf.lift_operation_before_chk
    category.lift_operation_after_chk = cf.lift_operation_after_chk
    category.lift_rem_before_chk = cf.lift_rem_before_chk
    category.lift_rem_after_chk = cf.lift_rem_after_chk
    category.packing_filter_before_chk = cf.packing_filter_before_chk
    category.packing_filter_after_chk = cf.packing_filter_after_chk
    category.packing_seal_before_chk = cf.packing_seal_before_chk
    category.packing_seal_after_chk = cf.packing_seal_after_chk
    category.packing_conveyor_before_chk = cf.packing_conveyor_before_chk
    category.packing_conveyor_after_chk = cf.packing_conveyor_after_chk
    category.packing_magnet_before_chk = cf.packing_magnet_before_chk
    category.packing_magnet_after_chk = cf.packing_magnet_after_chk
    category.packing_operation_before_chk = cf.packing_operation_before_chk
    category.packing_operation_after_chk = cf.packing_operation_after_chk
    category.packing_rem_before_chk = cf.packing_rem_before_chk
    category.packing_rem_after_chk = cf.packing_rem_after_chk
    category.tool_cleaning_before_chk = cf.tool_cleaning_before_chk
    category.tool_cleaning_after_chk = cf.tool_cleaning_after_chk
    category.uba3_cleaning_before_chk = cf.uba3_cleaning_before_chk
    category.uba3_cleaning_after_chk = cf.uba3_cleaning_after_chk
    category.weight_test_before_chk = cf.weight_test_before_chk
    category.weight_test_after_chk = cf.weight_test_after_chk
    category.residual_oxygen_am = cf.residual_oxygen_am
    category.residual_oxygen_pm = cf.residual_oxygen_pm
    category.weight_no_1 = cf.weight_no_1
    category.weight_no_2 = cf.weight_no_2
    category.weight_no_3 = cf.weight_no_3
    category.weight_no_4 = cf.weight_no_4
    category.weight_no_5 = cf.weight_no_5
    category.weight_chk_1 = cf.weight_chk_1
    category.weight_chk_2 = cf.weight_chk_2
    category.weight_chk_3 = cf.weight_chk_3
    category.weight_chk_4 = cf.weight_chk_4
    category.weight_chk_5 = cf.weight_chk_5
    category.remarks = cf.remarks


def _insert_package_no(session: Session) -> int:
    """package_no へ INSERT し、DB シーケンスで採番した serial_no（製造No）を返す。"""
    row = PackageNo(create_date=datetime.now())
    session.add(row)
    session.flush()
    if row.serial_no is None:
        session.refresh(row)
    if row.serial_no is None:
        raise HTTPException(
            status_code=500,
            detail="Failed to allocate product_no from package_no sequence",
        )
    return int(row.serial_no)


def create_package_lot(session: Session, payload: PackageLotCreateRequest) -> int:
    bf = payload.base_fields
    cf = payload.category_fields

    try:
        product_no = _insert_package_no(session)

        base = TePackageBaseNew(product_no=product_no)
        _apply_base_fields(base, bf)
        session.add(base)

        category = TePackageCategorysNew(product_no=product_no)
        _apply_category_fields(category, cf)
        session.add(category)

        session.commit()
        return product_no
    except HTTPException:
        session.rollback()
        raise
    except Exception as exc:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(exc)) from exc


def update_package_lot(session: Session, payload: PackageLotUpdateRequest) -> int:
    product_no = int(payload.product_no)
    base = session.get(TePackageBaseNew, product_no)
    if base is None:
        raise HTTPException(status_code=404, detail="Package lot not found")

    bf = payload.base_fields
    cf = payload.category_fields

    try:
        _apply_base_fields(base, bf)

        category = session.get(TePackageCategorysNew, product_no)
        if category is None:
            category = TePackageCategorysNew(product_no=product_no)
            session.add(category)
        _apply_category_fields(category, cf)

        session.commit()
        return product_no
    except HTTPException:
        session.rollback()
        raise
    except Exception as exc:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(exc)) from exc


def delete_package_lot(session: Session, payload: PackageLotDeleteRequest) -> int:
    product_no = int(payload.product_no)
    base = session.get(TePackageBaseNew, product_no)
    if base is None:
        raise HTTPException(status_code=404, detail="Package lot not found")

    try:
        session.execute(
            delete(TePackageCategorysNew).where(TePackageCategorysNew.product_no == product_no)
        )
        session.delete(base)
        session.commit()
        return product_no
    except HTTPException:
        session.rollback()
        raise
    except Exception as exc:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(exc)) from exc


def _insert_store_transfer_row(
    session: Session,
    *,
    transfer_dt: datetime,
    item_no: int,
    lot_no: int,
    transfer_quantity: float,
) -> int:
    transfer = TeStoreTransfer(
        transfer_date=transfer_dt,
        item_no=int(item_no),
        product_no=int(lot_no),
        transfer_type="2",
        result_type="2",
        lot_no="",
        lot_type="2",
        reason="通常品使用",
        store_no=3,
        store_party_name="",
        unit_weight=Decimal("0"),
        unit_number=0,
        fraction_weight=Decimal("0"),
        fraction_number=0,
        transfer_quantity=Decimal(str(transfer_quantity)),
        unit_type="Kg",
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
    return int(transfer.transfer_no)


def confirm_package_lot_stock(
    session: Session, payload: PackageLotConfirmStockRequest
) -> tuple[int, list[int]]:
    product_no = int(payload.product_no)
    base = session.get(TePackageBaseNew, product_no)
    if base is None:
        raise HTTPException(status_code=404, detail="Package lot not found")

    current_status = (base.lot_status or "").strip()
    if current_status == PACKAGE_LOT_STATUS_CONFIRMED:
        raise HTTPException(status_code=400, detail="Package lot is already confirmed")
    if current_status != PACKAGE_LOT_STATUS_COMPLETE:
        raise HTTPException(status_code=400, detail="Package lot status must be complete (2)")

    if not payload.transfer_rows:
        raise HTTPException(status_code=400, detail="transfer_rows is required")

    try:
        base.lot_status = PACKAGE_LOT_STATUS_CONFIRMED

        # 移動日はシステム日付（時刻は 00:00:00）
        transfer_dt = datetime.combine(datetime.now().date(), datetime.min.time())

        transfer_nos: list[int] = []
        for row in payload.transfer_rows:
            transfer_no = _insert_store_transfer_row(
                session,
                transfer_dt=transfer_dt,
                item_no=int(row.item_no),
                lot_no=int(row.lot_no),
                transfer_quantity=float(row.transfer_quantity),
            )
            transfer_nos.append(transfer_no)

        session.commit()
        return product_no, transfer_nos
    except HTTPException:
        session.rollback()
        raise
    except Exception as exc:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(exc)) from exc
