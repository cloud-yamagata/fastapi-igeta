"""第二工場ロット製造登録：登録・変更・削除の DB 更新（1 トランザクション）。

登録時:
  製造No … 工程別番号表（bulk_no 等）を PK 省略 INSERT → DB シーケンス
  ロットNo … te_lot_base を lot_no 省略 INSERT → DB シーケンス
  te_lot_categorys_common … 同一 lot_no で INSERT
"""
from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.entities.blend_no.model import BlendNo
from app.entities.bulk_no.model import BulkNo
from app.entities.finish_no.model import FinishNo
from app.entities.firepan_no.model import FirepanNo
from app.entities.te_lot_base.model import TeLotBase
from app.entities.te_lot_categorys_common.model import TeLotCategorysCommon
from app.entities.te_lot_part.model import TeLotPart
from app.entities.te_lot_use_item.model import TeLotUseItem
from app.schemas.factory2_lot_manufacture import (
    Factory2LotCategoryFieldsPayload,
    Factory2LotCreateRequest,
    Factory2LotDeleteRequest,
    Factory2LotUpdateRequest,
)

PROCESS_TYPE_PRODUCT_NO_TABLE: dict[str, type] = {
    "02": BulkNo,
    "03": FinishNo,
    "04": FirepanNo,
    "05": BlendNo,
}

DEFAULT_LOT_STATUS_ACTIVE = "1"


def _parse_work_date(text: str) -> date:
    t = text.strip()
    if not t:
        raise HTTPException(status_code=400, detail="work_date is required")
    if len(t) >= 10 and t[4] == "-":
        y, m, d = t[:10].split("-")
        return date(int(y), int(m), int(d))
    raise HTTPException(status_code=400, detail="Invalid work_date format")


def _resolve_use_no(session: Session, lot_no: int) -> int:
    use_row = session.get(TeLotUseItem, lot_no)
    if use_row is not None:
        return int(use_row.use_no)
    base = session.get(TeLotBase, lot_no)
    if base is not None:
        return int(base.product_no)
    return lot_no


def _child_lot_nos_from_parts(session: Session, parent_lot_no: int) -> set[int]:
    rows = session.scalars(select(TeLotPart).where(TeLotPart.lot_no == parent_lot_no)).all()
    return {int(p.part_no) for p in rows}


def _delete_use_items_for_lot_nos(session: Session, lot_nos: set[int]) -> None:
    if not lot_nos:
        return
    session.execute(delete(TeLotUseItem).where(TeLotUseItem.lot_no.in_(lot_nos)))


def _normalize_process_type(code: str) -> str:
    c = code.strip()
    if c.isdigit():
        return c.zfill(2)
    return c


def _insert_product_no(session: Session, process_type: str) -> int:
    """工程別番号表へ INSERT し、DB シーケンスで採番した serial_no（製造No）を返す。"""
    normalized = _normalize_process_type(process_type)
    model_cls = PROCESS_TYPE_PRODUCT_NO_TABLE.get(normalized)
    if model_cls is None:
        raise HTTPException(status_code=400, detail=f"Unsupported process_type: {process_type}")

    row = model_cls(create_date=datetime.now())
    session.add(row)
    session.flush()
    if row.serial_no is None:
        session.refresh(row)
    if row.serial_no is None:
        raise HTTPException(status_code=500, detail="Failed to allocate product_no from DB sequence")
    return int(row.serial_no)


def _apply_category_fields(
    category: TeLotCategorysCommon,
    cf: Factory2LotCategoryFieldsPayload,
    *,
    now: datetime,
) -> None:
    category.temperature = cf.temperature
    category.humidity = cf.humidity
    category.work_start_hh = cf.work_start_hh
    category.work_start_mm = cf.work_start_mm
    category.work_end_hh = cf.work_end_hh
    category.work_end_mm = cf.work_end_mm
    category.work_before_cleaning_start_hh = cf.work_before_cleaning_start_hh
    category.work_before_cleaning_start_mm = cf.work_before_cleaning_start_mm
    category.work_before_cleaning_end_hh = cf.work_before_cleaning_end_hh
    category.work_before_cleaning_end_mm = cf.work_before_cleaning_end_mm
    category.work_end_cleaning_start_hh = cf.work_end_cleaning_start_hh
    category.work_end_cleaning_start_mm = cf.work_end_cleaning_start_mm
    category.work_end_cleaning_end_hh = cf.work_end_cleaning_end_hh
    category.work_end_cleaning_end_mm = cf.work_end_cleaning_end_mm
    category.work_before_cleaning_chk = cf.work_before_cleaning_chk
    category.work_after_cleaning_chk = cf.work_after_cleaning_chk
    category.device_chk = cf.device_chk
    category.operation_chk = cf.operation_chk
    category.rest_chk = cf.rest_chk
    category.magnet_cleaning_chk = cf.magnet_cleaning_chk
    category.use_device_unit1_chk = cf.use_device_unit1_chk
    category.use_device_unit2_chk = cf.use_device_unit2_chk
    category.use_device_unit3_chk = cf.use_device_unit3_chk
    category.packing_case1_chk = cf.packing_case1_chk
    category.packing_case2_chk = cf.packing_case2_chk
    category.update_time = now


def _insert_category(
    session: Session,
    lot_no: int,
    cf: Factory2LotCategoryFieldsPayload,
    *,
    now: datetime,
) -> None:
    category = TeLotCategorysCommon(lot_no=lot_no)
    _apply_category_fields(category, cf, now=now)
    session.add(category)


def _delete_category_for_lot(session: Session, lot_no: int) -> None:
    session.execute(delete(TeLotCategorysCommon).where(TeLotCategorysCommon.lot_no == lot_no))


def _upsert_child_use_item(
    session: Session,
    child_lot_no: int,
    *,
    part_name: str | None,
    make_year: str | None,
    count: str | None,
) -> None:
    """使用部品の子ロット：既存行は更新、未登録のみ INSERT（PK 衝突回避）。"""
    existing = session.get(TeLotUseItem, child_lot_no)
    if existing is not None:
        existing.use_name = part_name
        existing.make_year = make_year
        existing.count = count
        return
    session.add(
        TeLotUseItem(
            lot_no=child_lot_no,
            use_no=_resolve_use_no(session, child_lot_no),
            use_name=part_name,
            make_year=make_year,
            count=count,
        )
    )


def create_factory2_lot(session: Session, payload: Factory2LotCreateRequest) -> tuple[int, int]:
    process_type = _normalize_process_type(payload.process_type)
    if process_type not in PROCESS_TYPE_PRODUCT_NO_TABLE:
        raise HTTPException(status_code=400, detail=f"Unsupported process_type: {payload.process_type}")

    bf = payload.base_fields
    organic = (payload.organic_class or "C").strip().upper()[:1] or "C"
    now = datetime.now()

    try:
        product_no = _insert_product_no(session, process_type)

        base = TeLotBase(
            process_type=process_type,
            product_no=product_no,
            lot_status=DEFAULT_LOT_STATUS_ACTIVE,
            lot_name=bf.lot_name,
            work_date=_parse_work_date(bf.work_date),
            organic_class=organic,
            unit_weight=Decimal(str(bf.unit_weight)),
            unit_number=int(bf.unit_number),
            fraction_weight=Decimal(str(bf.fraction_weight)) if bf.fraction_weight is not None else None,
            fraction_number=int(bf.fraction_number) if bf.fraction_number is not None else None,
            remarks=bf.remarks,
            update_time=now,
        )
        session.add(base)
        session.flush()
        if base.lot_no is None:
            session.refresh(base)
        if base.lot_no is None:
            raise HTTPException(status_code=500, detail="Failed to allocate lot_no from DB sequence")
        lot_no = int(base.lot_no)

        session.add(
            TeLotUseItem(
                lot_no=lot_no,
                use_no=product_no,
                use_name=bf.use_name or None,
                make_year=bf.make_year or None,
                count=bf.count or None,
            )
        )

        for row in payload.part_rows:
            child_lot_no = int(row.lot_no)
            part_no = int(row.part_no)
            _upsert_child_use_item(
                session,
                child_lot_no,
                part_name=row.part_name,
                make_year=row.make_year,
                count=row.count,
            )
            qty = row.use_quantity
            session.add(
                TeLotPart(
                    lot_no=lot_no,
                    part_no=part_no,
                    use_quantity=Decimal(str(qty)) if qty is not None else None,
                    remarks=row.remarks,
                    update_time=now,
                )
            )

        _insert_category(session, lot_no, payload.category_fields, now=now)

        session.commit()
        return lot_no, product_no
    except HTTPException:
        session.rollback()
        raise
    except Exception as exc:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(exc)) from exc


def update_factory2_lot(session: Session, payload: Factory2LotUpdateRequest) -> int:
    lot_no = payload.parent_lot_no
    base = session.get(TeLotBase, lot_no)
    if base is None:
        raise HTTPException(status_code=404, detail="Lot not found")

    bf = payload.base_fields
    cf = payload.category_fields
    organic = (payload.organic_class or "C").strip().upper()[:1] or "C"
    now = datetime.now()

    try:
        base.organic_class = organic
        base.lot_name = bf.lot_name
        base.work_date = _parse_work_date(bf.work_date)
        base.unit_weight = Decimal(str(bf.unit_weight))
        base.unit_number = int(bf.unit_number)
        base.fraction_weight = Decimal(str(bf.fraction_weight)) if bf.fraction_weight is not None else None
        base.fraction_number = int(bf.fraction_number) if bf.fraction_number is not None else None
        base.remarks = bf.remarks
        base.update_time = now

        category = session.get(TeLotCategorysCommon, lot_no)
        if category is None:
            category = TeLotCategorysCommon(lot_no=lot_no)
            session.add(category)
        _apply_category_fields(category, cf, now=now)

        child_lot_nos = _child_lot_nos_from_parts(session, lot_no)
        use_delete_lot_nos = {lot_no, *child_lot_nos}

        session.execute(delete(TeLotPart).where(TeLotPart.lot_no == lot_no))
        _delete_use_items_for_lot_nos(session, use_delete_lot_nos)

        parent_use_no = _resolve_use_no(session, lot_no)
        session.add(
            TeLotUseItem(
                lot_no=lot_no,
                use_no=parent_use_no,
                use_name=bf.use_name or None,
                make_year=bf.make_year or None,
                count=bf.count or None,
            )
        )

        for row in payload.part_rows:
            child_lot_no = int(row.lot_no)
            part_no = int(row.part_no)
            session.add(
                TeLotUseItem(
                    lot_no=child_lot_no,
                    use_no=_resolve_use_no(session, child_lot_no),
                    use_name=row.part_name,
                    make_year=row.make_year,
                    count=row.count,
                )
            )
            qty = row.use_quantity
            session.add(
                TeLotPart(
                    lot_no=lot_no,
                    part_no=part_no,
                    use_quantity=Decimal(str(qty)) if qty is not None else None,
                    remarks=row.remarks,
                    update_time=now,
                )
            )

        session.commit()
        return lot_no
    except HTTPException:
        session.rollback()
        raise
    except Exception as exc:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(exc)) from exc


def delete_factory2_lot(session: Session, payload: Factory2LotDeleteRequest) -> int:
    lot_no = payload.lot_no
    base = session.get(TeLotBase, lot_no)
    if base is None:
        raise HTTPException(status_code=404, detail="Lot not found")

    try:
        child_lot_nos = _child_lot_nos_from_parts(session, lot_no)
        use_delete_lot_nos = {lot_no, *child_lot_nos}

        session.execute(delete(TeLotPart).where(TeLotPart.lot_no == lot_no))
        _delete_use_items_for_lot_nos(session, use_delete_lot_nos)
        _delete_category_for_lot(session, lot_no)
        session.delete(base)
        session.commit()
        return lot_no
    except HTTPException:
        session.rollback()
        raise
    except Exception as exc:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(exc)) from exc
