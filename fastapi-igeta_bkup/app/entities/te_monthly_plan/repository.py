"""te_monthly_plan 永続化アクセス（CRUD 雛形を含む）。"""
from __future__ import annotations

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.entities.te_monthly_plan.model import TeMonthlyPlan


class TeMonthlyPlanRepository:
    """月別製造計画 ``te_monthly_plan`` の Repository。"""

    # --- Read ---

    @staticmethod
    def list_all(session: Session) -> list[TeMonthlyPlan]:
        return list(session.scalars(select(TeMonthlyPlan)).all())

    @staticmethod
    def get_by_plan_no(session: Session, plan_no: int) -> TeMonthlyPlan | None:
        return session.get(TeMonthlyPlan, plan_no)

    # --- Create / Update（persist はルーターからの汎用保存用）---

    @staticmethod
    def create(session: Session, row: TeMonthlyPlan) -> TeMonthlyPlan:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def persist(session: Session, row: TeMonthlyPlan) -> TeMonthlyPlan:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: TeMonthlyPlan) -> TeMonthlyPlan:
        return TeMonthlyPlanRepository.persist(session, row)

    # --- Delete ---

    @staticmethod
    def delete_by_plan_no(session: Session, plan_no: int) -> bool:
        row = session.get(TeMonthlyPlan, plan_no)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True

    @staticmethod
    def delete_by_plan_nos(session: Session, plan_nos: list[int]) -> int:
        if not plan_nos:
            return 0
        uniq = list(dict.fromkeys(plan_nos))
        res = session.execute(delete(TeMonthlyPlan).where(TeMonthlyPlan.plan_no.in_(uniq)))
        session.commit()
        return int(res.rowcount or 0)
