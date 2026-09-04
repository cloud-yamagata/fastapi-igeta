"""vi_factory3_stoc 参照。"""
from __future__ import annotations

from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.entities.vi_factory3_stoc.model import ViFactory3Stoc

# ビュー本体に organic_class / item_group_no が無いため tr_item を JOIN して返す
_LIST_WITH_ITEM_SQL = text(
    """
    SELECT
      v.item_no,
      v.item_name,
      v.product_no,
      v.stoc_quantity,
      i.organic_class,
      i.item_group_no
    FROM vi_factory3_stoc v
    INNER JOIN tr_item i ON v.item_no = i.item_no
    ORDER BY v.item_no, v.product_no
    """
)


class ViFactory3StocRepository:
    @staticmethod
    def list_all(session: Session) -> list[ViFactory3Stoc]:
        return list(session.scalars(select(ViFactory3Stoc)).all())

    @staticmethod
    def list_all_with_item_attrs(session: Session) -> list[dict[str, object]]:
        return [dict(row) for row in session.execute(_LIST_WITH_ITEM_SQL).mappings().all()]
