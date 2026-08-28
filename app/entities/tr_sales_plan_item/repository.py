"""tr_sales_plan_item 永続化アクセス。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.tr_sales_plan_item.model import TrSalesPlanItem


class TrSalesPlanItemRepository:
    @staticmethod
    def list_all(session: Session) -> list[TrSalesPlanItem]:
        return list(session.scalars(select(TrSalesPlanItem)).all())

    @staticmethod
    def get_by_pk(session: Session, item_no: object) -> TrSalesPlanItem | None:
        return session.get(TrSalesPlanItem, item_no)

    @staticmethod
    def create(session: Session, row: TrSalesPlanItem) -> TrSalesPlanItem:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: TrSalesPlanItem) -> TrSalesPlanItem:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def delete_by_pk(session: Session, item_no: object) -> bool:
        row = session.get(TrSalesPlanItem, item_no)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True
