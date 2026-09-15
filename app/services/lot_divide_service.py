"""ロット分割 MaterialRegist（WPF LotDivide StoreRepository.MaterialRegist 相当）。

同一トランザクションで:
  1. te_material INSERT
  2. te_material_material_no_seq の currval → serial_no
  3. te_store_transfer_fa2 INSERT（新ロット入庫）
  4. te_lot_use_item INSERT
  5. te_store_transfer_fa2 INSERT（元ロット出庫）
  6. te_lot_divide UPSERT
"""
from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

_INSERT_MATERIAL_SQL = """
insert into te_material
(
 year
,purchase
,purchase_no
,purchase_date
,variety
,tea_life
,organic_class
,tea_type
,tea_rank
,field_no
,producer
,cost
,material_name
,unit_weight
,unit_number
,fraction_weight
,fraction_number
,remarks
,update_time
)
values
(
 :year
,:purchase
,:purchase_no
,:purchase_date
,:variety
,:tea_life
,:organic_class
,:tea_type
,:tea_rank
,:field_no
,:producer
,:cost
,:material_name
,:unit_weight
,:unit_number
,:fraction_weight
,:fraction_number
,:remarks
,current_timestamp
)
"""

_CURRVAL_MATERIAL_SQL = "select currval('te_material_material_no_seq')"

_INSERT_TRANSFER_FA2_SQL = """
insert into te_store_transfer_fa2
(
 transfer_date
,lot_no
,process_type
,product_no
,lot_name
,transfer_type
,result_type
,lot_type
,reason
,unit_weight
,unit_number
,fraction_weight
,fraction_number
,transfer_quantity
,unit_type
,remarks
,update_time
)
values
(
 :transfer_date
,:lot_no
,:process_type
,:product_no
,:lot_name
,:transfer_type
,:result_type
,:lot_type
,:reason
,:unit_weight
,:unit_number
,:fraction_weight
,:fraction_number
,:transfer_quantity
,:unit_type
,:remarks
,current_timestamp
)
"""

_INSERT_LOT_USE_ITEM_SQL = """
insert into te_lot_use_item
(
 lot_no
,use_no
,use_name
,make_year
,count
)
values
(
 :lot_no
,:item_no
,:item_name
,:make_year
,:count
)
"""

_UPSERT_LOT_DIVIDE_SQL = """
insert into te_lot_divide
(
 lot_no
,divide_no
,divide_date
,divide_type
,reason
,divide_quantity
,remarks
,update_time
)
values
(
 :lot_no
,:divide_no
,:divide_date
,:divide_type
,:reason
,:divide_quantity
,:remarks
,current_timestamp
)
on conflict on constraint pk_te_lot_divide
do update set
lot_no = excluded.lot_no,
divide_no = excluded.divide_no,
divide_date = excluded.divide_date,
divide_type = excluded.divide_type,
reason = excluded.reason,
divide_quantity = excluded.divide_quantity,
remarks = excluded.remarks,
update_time = excluded.update_time
"""


def _parse_date(text_value: str) -> date:
    t = (text_value or "").strip()
    if not t:
        raise HTTPException(status_code=400, detail="divide_date is required")
    if len(t) >= 10 and t[4] in "-/":
        sep = t[4]
        y, m, d = t[:10].split(sep)
        return date(int(y), int(m), int(d))
    raise HTTPException(status_code=400, detail="Invalid divide_date format")


def _fiscal_year_yy() -> int:
    """WPF: DateTime.Now.AddMonths(-3).ToString(\"yy\")"""
    d = datetime.now()
    # AddMonths(-3)
    month = d.month - 3
    year = d.year
    while month <= 0:
        month += 12
        year -= 1
    return year % 100


def material_regist(
    session: Session,
    *,
    lot_no: int,
    process_type: str,
    product_no: int,
    lot_name: str | None,
    item_no: int,
    item_name: str | None,
    organic_class: str,
    make_year: str | None,
    count: str | None,
    factory2_stock: float,
    divide_type: str,
    divide_date: str,
    divide_quantity: float,
    divide_lot_name: str,
    reason: str | None,
    remarks: str | None,
) -> int:
    if divide_type not in ("1", "2"):
        raise HTTPException(status_code=400, detail="divide_type must be 1 or 2")
    if lot_no <= 0 or product_no <= 0:
        raise HTTPException(status_code=400, detail="lot_no / product_no is required")

    qty = Decimal(str(divide_quantity))
    stock = Decimal(str(factory2_stock))
    if qty <= 0 or qty > stock:
        raise HTTPException(status_code=400, detail="入力された分割数量が不正です")

    if divide_type == "2" and not (reason or "").strip():
        raise HTTPException(status_code=400, detail="転売先を入力してください")

    divide_dt = _parse_date(divide_date)
    divide_lot_name = (divide_lot_name or "").strip()
    if not divide_lot_name:
        raise HTTPException(status_code=400, detail="分割ロット名を入力してください")

    is_reinput = divide_type == "1"
    process = (process_type or "").strip().zfill(2)[-2:]

    try:
        session.execute(
            text(_INSERT_MATERIAL_SQL),
            {
                "year": _fiscal_year_yy(),
                "purchase": "第2工場",
                "purchase_no": "00000",
                "purchase_date": divide_dt,
                "variety": "",
                "tea_life": "",
                "organic_class": (organic_class or "").strip() or "C",
                "tea_type": "",
                "tea_rank": "",
                "field_no": "",
                "producer": "",
                "cost": 0,
                "material_name": divide_lot_name,
                "unit_weight": qty,
                "unit_number": 1,
                "fraction_weight": Decimal("0"),
                "fraction_number": 0,
                "remarks": remarks,
            },
        )

        serial_no = session.execute(text(_CURRVAL_MATERIAL_SQL)).scalar()
        if serial_no is None or int(serial_no) <= 0:
            raise HTTPException(status_code=500, detail="原料NOの採番に失敗しました")
        serial_no = int(serial_no)

        # 新ロット入庫
        session.execute(
            text(_INSERT_TRANSFER_FA2_SQL),
            {
                "transfer_date": datetime.combine(divide_dt, datetime.min.time()),
                "lot_no": serial_no,
                "process_type": "01",
                "product_no": serial_no,
                "lot_name": divide_lot_name,
                "transfer_type": "1",
                "result_type": "1",
                "lot_type": "1",
                "reason": "ロット再投入" if is_reinput else "転売",
                "unit_weight": qty if is_reinput else Decimal("0"),
                "unit_number": 1 if is_reinput else 0,
                "fraction_weight": Decimal("0"),
                "fraction_number": 0,
                "transfer_quantity": qty if is_reinput else Decimal("0"),
                "unit_type": "Kg",
                "remarks": "",
            },
        )

        session.execute(
            text(_INSERT_LOT_USE_ITEM_SQL),
            {
                "lot_no": serial_no,
                "item_no": item_no if item_no > 0 else 0,
                "item_name": item_name,
                "make_year": make_year,
                "count": count,
            },
        )

        # 元ロット出庫
        session.execute(
            text(_INSERT_TRANSFER_FA2_SQL),
            {
                "transfer_date": datetime.combine(divide_dt, datetime.min.time()),
                "lot_no": lot_no,
                "process_type": process,
                "product_no": product_no,
                "lot_name": lot_name,
                "transfer_type": "2",
                "result_type": "2" if is_reinput else "5",
                "lot_type": "2",
                "reason": "ロット分割" if is_reinput else "転売",
                "unit_weight": qty,
                "unit_number": 1,
                "fraction_weight": Decimal("0"),
                "fraction_number": 0,
                "transfer_quantity": qty,
                "unit_type": "Kg",
                "remarks": "",
            },
        )

        session.execute(
            text(_UPSERT_LOT_DIVIDE_SQL),
            {
                "lot_no": lot_no,
                "divide_no": serial_no,
                "divide_date": divide_dt,
                "divide_type": divide_type,
                "reason": reason,
                "divide_quantity": qty,
                "remarks": remarks,
            },
        )

        session.commit()
        return serial_no
    except HTTPException:
        session.rollback()
        raise
    except Exception as exc:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(exc)) from exc
