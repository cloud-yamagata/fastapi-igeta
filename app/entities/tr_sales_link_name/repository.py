"""tr_sales_link_name 永続化アクセス。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.tr_sales_link_name.model import TrSalesLinkName


class TrSalesLinkNameRepository:
    @staticmethod
    def list_all(session: Session) -> list[TrSalesLinkName]:
        stmt = select(TrSalesLinkName).order_by(TrSalesLinkName.sales_item_name)
        return list(session.scalars(stmt).all())

    @staticmethod
    def build_exact_lookup(session: Session) -> dict[str, int]:
        exact: dict[str, int] = {}
        for row in TrSalesLinkNameRepository.list_all(session):
            name = (row.sales_item_name or "").strip()
            if name:
                exact[name] = row.item_no
        return exact
