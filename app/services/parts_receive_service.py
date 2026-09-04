"""仕上品受入（WPF PartsReceive StockRepository 相当）。

一覧: 仕上茶在庫 SQL（process_type=05）
受入: te_store_transfer + te_store_transfer_fa2 を同一トランザクションで INSERT
"""
from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

STOCK_LIST_SQL = (Path(__file__).resolve().parents[2] / "各種レポートSQL" / "parts_receive_stock_list.sql")

# WPF Resources から抽出した SQL（ファイルが無い場合のフォールバック）
_STOCK_LIST_FALLBACK = r"""
with
v_factory2_product as
(
select
 a.lot_no
,a.process_type
,a.product_no
,max(a.transfer_date) as product_date
,sum(a.transfer_quantity) as quantity
from te_store_transfer_fa2 a
where a.transfer_type = '1'
  and a.result_type = '1'
  and a.process_type = '05'
group by a.lot_no, a.process_type, a.product_no
)
,
v_factory3_receive as
(
select
 a.lot_no
,a.process_type
,a.product_no
,sum(a.transfer_quantity) as quantity
from te_store_transfer_fa2 a
where a.transfer_type = '3'
  and a.result_type in ('3')
group by a.lot_no, a.process_type, a.product_no
)
,
v_factory3_input as
(
select
 a.product_no
,'05' as process_type
,sum(a.transfer_quantity) as quantity
from te_store_transfer a
where a.transfer_type = '2'
  and a.result_type in ('2')
  and a.store_no = 3
  and a.lot_type = '2'
group by a.product_no
)
,
v_factory3_return as
(
select
 a.lot_no
,a.process_type
,a.product_no
,sum(a.transfer_quantity) as quantity
from te_store_transfer_fa2 a
where a.transfer_type = '3'
  and a.result_type in ('7')
group by a.lot_no, a.process_type, a.product_no
)
,
v_factory3_adjust as
(
select
 a.item_no
,a.product_no
,sum(case a.transfer_type when '2' then -(a.transfer_quantity) else a.transfer_quantity end) as quantity
from te_store_transfer a
where a.lot_type = '2'
  and a.result_type = '9'
  and a.store_no = 3
group by a.item_no, a.product_no
)
select
 a.product_date
,b.use_no as item_no
,a.product_no
,b.use_name as product_name
,b.make_year
,b.count
,coalesce(a.quantity, 0) as product_quantity
,coalesce(c.factory2_stock, 0)  as factory2_stock
,coalesce(d.quantity, 0) - coalesce(e.quantity, 0) - coalesce(f.quantity, 0) + coalesce(g.quantity, 0) as factory3_stock
from v_factory2_product a
inner join te_lot_use_item b on a.lot_no = b.lot_no
left join vi_factory2_stock c on a.product_no = c.product_no and c.process_type = '05'
left join v_factory3_receive d on a.lot_no = d.lot_no
left join v_factory3_return e on a.lot_no = e.lot_no
left join v_factory3_input f on a.product_no = f.product_no
left join v_factory3_adjust g on a.product_no = g.product_no
where 0=0
order by b.use_no, a.product_no
"""

_INSERT_TRANSFER_SQL = """
insert into te_store_transfer
(
 transfer_date
,item_no
,product_no
,lot_no
,transfer_type
,result_type
,reason
,lot_type
,store_no
,store_party_name
,unit_weight
,unit_number
,fraction_weight
,fraction_number
,transfer_quantity
,unit_type
,remarks
)
select
 :transfer_date as transfer_date
,b.use_no as item_no
,a.product_no
,cast(a.lot_no as text) as lot_no
,'3' as transfer_type
,:result_type as result_type
,:reason as reason
,'2' as lot_type
,:store_no as store_no
,'井ケ田第二工場' as store_party_name
,0 as unit_weight
,0 as unit_number
,0 as fraction_weight
,0 as fraction_number
,:transfer_quantity as transfer_quantity
,'Kg' as unit_type
,'' as remarks
from te_store_transfer_fa2 a
inner join te_lot_use_item b on a.lot_no = b.lot_no
where 0=0
  and b.use_no = :item_no
  and a.product_no = :product_no
  and a.process_type = '05'
  and a.transfer_type = '1'
  and a.result_type = '1'
  and a.lot_type = '2'
"""

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
)
select
 :transfer_date as transfer_date
,a.lot_no
,a.process_type
,a.product_no
,a.lot_name
,'3' as transfer_type
,:result_type as result_type
,'2' as lot_type
,:reason as reason
,0 as unit_weight
,0 as unit_number
,0 as fraction_weight
,0 as fraction_number
,:transfer_quantity as transfer_quantity
,'Kg'
,'' as remarks
from te_store_transfer_fa2 a
where 0=0
  and a.product_no = :product_no
  and a.process_type = '05'
  and a.transfer_type = '1'
  and a.result_type = '1'
  and a.lot_type = '2'
"""


def _load_stock_sql() -> str:
    if STOCK_LIST_SQL.exists():
        return STOCK_LIST_SQL.read_text(encoding="utf-8")
    return _STOCK_LIST_FALLBACK


def _parse_date(text_value: str) -> datetime:
    t = (text_value or "").strip()
    if not t:
        raise HTTPException(status_code=400, detail="transfer_date is required")
    if len(t) >= 10 and t[4] in "-/":
        sep = t[4]
        y, m, d = t[:10].split(sep)
        day = date(int(y), int(m), int(d))
        return datetime.combine(day, datetime.min.time())
    raise HTTPException(status_code=400, detail="Invalid transfer_date format")


def _cell_date(v: object) -> str | None:
    if v is None:
        return None
    if hasattr(v, "isoformat"):
        s = v.isoformat()  # type: ignore[union-attr]
        return s[:10] if len(s) >= 10 else s
    s = str(v)
    return s[:10] if len(s) >= 10 else s


def list_parts_receive_stocks(session: Session) -> list[dict]:
    sql = _load_stock_sql()
    rows = session.execute(text(sql)).mappings().all()
    out: list[dict] = []
    for r in rows:
        f2 = float(r.get("factory2_stock") or 0)
        f3 = float(r.get("factory3_stock") or 0)
        if f2 <= 0 and f3 <= 0:
            continue
        out.append(
            {
                "product_date": _cell_date(r.get("product_date")),
                "item_no": int(r["item_no"]),
                "product_no": int(r["product_no"]),
                "product_name": r.get("product_name"),
                "make_year": None if r.get("make_year") is None else str(r.get("make_year")),
                "count": None if r.get("count") is None else str(r.get("count")),
                "product_quantity": float(r.get("product_quantity") or 0),
                "factory2_stock": f2,
                "factory3_stock": f3,
            }
        )
    return out


def receive_parts(session: Session, *, item_no: int, product_no: int, transfer_quantity: float, transfer_date: str, store_no: int) -> None:
    if store_no not in (2, 3):
        raise HTTPException(status_code=400, detail="受入先の工場が指定されておりません")
    if item_no <= 0 or product_no <= 0:
        raise HTTPException(status_code=400, detail="item_no / product_no is required")
    qty = Decimal(str(transfer_quantity))
    if qty <= 0:
        raise HTTPException(status_code=400, detail="移動量の指定が正しくありません")

    stocks = list_parts_receive_stocks(session)
    target = next((s for s in stocks if s["item_no"] == item_no and s["product_no"] == product_no), None)
    if target is None:
        raise HTTPException(status_code=404, detail="対象の仕上茶在庫が見つかりません")

    if store_no == 3 and qty > Decimal(str(target["factory2_stock"])):
        raise HTTPException(status_code=400, detail="第二工場の在庫量に対し受入れ量の指定が正しくありません")
    if store_no == 2 and qty > Decimal(str(target["factory3_stock"])):
        raise HTTPException(status_code=400, detail="第三工場の在庫量に対し受入れ量の指定が正しくありません")

    transfer_dt = _parse_date(transfer_date)
    # te_store_transfer: 第2工場は返品（result_type=7 / reason=仕上茶返品）
    #                    第3工場は通常品受入
    if store_no == 2:
        transfer_result_type = "7"
        transfer_reason = "仕上茶返品"
    else:
        transfer_result_type = "3"
        transfer_reason = "通常品受入"
    # te_store_transfer_fa2: WPF どおり（第2工場=返品 / 第3工場=受入）
    fa2_result_type = "7" if store_no == 2 else "3"
    fa2_reason = "仕上茶返品" if store_no == 2 else "仕上茶受入"

    try:
        r1 = session.execute(
            text(_INSERT_TRANSFER_SQL),
            {
                "transfer_date": transfer_dt,
                "store_no": store_no,
                "result_type": transfer_result_type,
                "reason": transfer_reason,
                "transfer_quantity": qty,
                "item_no": item_no,
                "product_no": product_no,
            },
        )
        if r1.rowcount == 0:
            raise HTTPException(status_code=404, detail="受入元の第2工場生産実績が見つかりません")

        r2 = session.execute(
            text(_INSERT_TRANSFER_FA2_SQL),
            {
                "transfer_date": transfer_dt,
                "result_type": fa2_result_type,
                "reason": fa2_reason,
                "transfer_quantity": qty,
                "product_no": product_no,
            },
        )
        if r2.rowcount == 0:
            raise HTTPException(status_code=404, detail="受入元の第2工場生産実績が見つかりません")

        session.commit()
    except HTTPException:
        session.rollback()
        raise
    except Exception as exc:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(exc)) from exc
