"""te_monthly_product_plan 永続化アクセス。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.te_monthly_product_plan.model import TeMonthlyProductPlan


class TeMonthlyProductPlanRepository:
    @staticmethod
    def list_by_year_month(session: Session, year: int, month: int) -> list[TeMonthlyProductPlan]:
        stmt = (
            select(TeMonthlyProductPlan)
            .where(TeMonthlyProductPlan.year == year, TeMonthlyProductPlan.month == month)
            .order_by(TeMonthlyProductPlan.item_no, TeMonthlyProductPlan.bulk_no)
        )
        return list(session.scalars(stmt).all())

    @staticmethod
    def delete_by_year_month(session: Session, year: int, month: int) -> int:
        rows = TeMonthlyProductPlanRepository.list_by_year_month(session, year, month)
        for row in rows:
            session.delete(row)
        return len(rows)
