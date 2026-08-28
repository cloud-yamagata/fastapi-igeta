"""te_monthly_sales_plan 永続化アクセス。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.te_monthly_sales_plan.model import TeMonthlySalesPlan


class TeMonthlySalesPlanRepository:
    @staticmethod
    def list_by_year_month(session: Session, year: int, month: int) -> list[TeMonthlySalesPlan]:
        stmt = (
            select(TeMonthlySalesPlan)
            .where(TeMonthlySalesPlan.year == year, TeMonthlySalesPlan.month == month)
            .order_by(TeMonthlySalesPlan.item_no)
        )
        return list(session.scalars(stmt).all())

    @staticmethod
    def get_by_pk(
        session: Session, year: int, month: int, item_no: int
    ) -> TeMonthlySalesPlan | None:
        return session.get(TeMonthlySalesPlan, (year, month, item_no))

    @staticmethod
    def upsert_month(
        session: Session,
        *,
        year: int,
        month: int,
        items: list[TeMonthlySalesPlan],
    ) -> None:
        incoming_nos = {row.item_no for row in items}
        for existing in TeMonthlySalesPlanRepository.list_by_year_month(session, year, month):
            if existing.item_no not in incoming_nos:
                session.delete(existing)
        for row in items:
            current = session.get(TeMonthlySalesPlan, (year, month, row.item_no))
            if current is None:
                session.add(row)
            else:
                current.item_name = row.item_name
                current.sales_size = row.sales_size
                current.remarks = row.remarks
        session.commit()

    @staticmethod
    def delete_by_year_month(session: Session, year: int, month: int) -> int:
        rows = TeMonthlySalesPlanRepository.list_by_year_month(session, year, month)
        if not rows:
            return 0
        for row in rows:
            session.delete(row)
        session.commit()
        return len(rows)
