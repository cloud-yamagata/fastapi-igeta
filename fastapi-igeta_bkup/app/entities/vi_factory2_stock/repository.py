"""vi_factory2_stock 参照（在庫ありのみ）。"""
from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.te_lot_base.model import TeLotBase
from app.entities.te_lot_use_item.model import TeLotUseItem
from app.entities.vi_factory2_stock.model import ViFactory2Stock

# 第二工場ロット一覧と同じ工程表示名（process_type コード → 名称）
_PROCESS_TYPE_NAMES: dict[str, str] = {
    "01": "荒茶原料",
    "02": "荒茶ブ",
    "03": "仕上",
    "04": "火入",
    "05": "仕上ブ",
}


def _normalize_process_type(code: str) -> str:
    c = (code or "").strip()
    if c.isdigit():
        return c.zfill(2)
    return c


def _process_type_name(code: str) -> str | None:
    key = _normalize_process_type(code)
    if key in _PROCESS_TYPE_NAMES:
        return _PROCESS_TYPE_NAMES[key]
    if ":" in code:
        return code.split(":", 1)[1]
    if code and not code.isdigit():
        return code
    return None


class ViFactory2StockRepository:
    @staticmethod
    def list_in_stock(session: Session) -> list[dict[str, Any]]:
        """
        在庫ビューに te_lot_base / te_lot_use_item を結合し、
        行ごとに工程・通称名などがロットNO単位で正しくなるよう補完する。
        """
        v = ViFactory2Stock
        b = TeLotBase
        u = TeLotUseItem

        stmt = (
            select(
                v.lot_no,
                b.process_type.label("_base_process_type"),
                v.process_type.label("_view_process_type"),
                v.product_no,
                v.process_type_name,
                v.product_date,
                b.work_date.label("_base_work_date"),
                u.use_name.label("_use_name"),
                v.item_name.label("_view_item_name"),
                b.lot_name.label("_base_lot_name"),
                v.lot_name.label("_view_lot_name"),
                b.organic_class.label("_base_organic_class"),
                v.organic_class.label("_view_organic_class"),
                u.make_year.label("_use_make_year"),
                v.make_year.label("_view_make_year"),
                u.count.label("_use_count"),
                v.count.label("_view_count"),
                v.product_quantity,
                v.factory2_stock,
            )
            .select_from(v)
            .outerjoin(b, v.lot_no == b.lot_no)
            .outerjoin(u, v.lot_no == u.lot_no)
            .where(v.factory2_stock > 0)
        )

        out: list[dict[str, Any]] = []
        for row in session.execute(stmt).mappings().all():
            base_pt = row.get("_base_process_type")
            view_pt = row.get("_view_process_type")
            process_type = _normalize_process_type(
                str(base_pt).strip() if base_pt is not None and str(base_pt).strip() else str(view_pt or "")
            )
            pt_name = row.get("process_type_name")
            process_type_name = (
                str(pt_name).strip()
                if pt_name is not None and str(pt_name).strip()
                else _process_type_name(process_type)
            )

            use_name = row.get("_use_name")
            view_item = row.get("_view_item_name")
            item_name = (
                str(use_name).strip()
                if use_name is not None and str(use_name).strip()
                else (str(view_item).strip() if view_item is not None else None)
            ) or None

            base_lot = row.get("_base_lot_name")
            view_lot = row.get("_view_lot_name")
            lot_name = (
                str(base_lot).strip()
                if base_lot is not None and str(base_lot).strip()
                else (str(view_lot).strip() if view_lot is not None else None)
            ) or None

            base_oc = row.get("_base_organic_class")
            view_oc = row.get("_view_organic_class")
            organic_class = (
                str(base_oc).strip()
                if base_oc is not None and str(base_oc).strip()
                else (str(view_oc).strip() if view_oc is not None else None)
            ) or None

            use_my = row.get("_use_make_year")
            view_my = row.get("_view_make_year")
            make_year = (
                str(use_my).strip()
                if use_my is not None and str(use_my).strip()
                else (str(view_my).strip() if view_my is not None else None)
            ) or None

            use_cnt = row.get("_use_count")
            view_cnt = row.get("_view_count")
            count = (
                str(use_cnt).strip()
                if use_cnt is not None and str(use_cnt).strip()
                else (str(view_cnt).strip() if view_cnt is not None else None)
            ) or None

            product_date = row.get("product_date") or row.get("_base_work_date")

            out.append(
                {
                    "lot_no": row["lot_no"],
                    "process_type": process_type,
                    "process_type_name": process_type_name,
                    "product_no": row["product_no"],
                    "product_date": product_date,
                    "item_name": item_name,
                    "lot_name": lot_name,
                    "organic_class": organic_class,
                    "make_year": make_year,
                    "count": count,
                    "product_quantity": row.get("product_quantity"),
                    "factory2_stock": row.get("factory2_stock"),
                }
            )
        return out
