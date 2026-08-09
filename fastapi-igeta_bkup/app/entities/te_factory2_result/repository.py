"""te_factory2_result 永続化アクセス（CRUD 雛形・自動生成）。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.te_factory2_result.model import TeFactory2Result


class TeFactory2ResultRepository:
    @staticmethod
    def list_all(session: Session) -> list[TeFactory2Result]:
        return list(session.scalars(select(TeFactory2Result)).all())

    @staticmethod
    def get_by_pk(session: Session, work_date: object, use_tea_no: object, make_year: object, count: object) -> TeFactory2Result | None:
        stmt = select(TeFactory2Result).where((TeFactory2Result.work_date == work_date) & (TeFactory2Result.use_tea_no == use_tea_no) & (TeFactory2Result.make_year == make_year) & (TeFactory2Result.count == count))
        return session.scalars(stmt).first()

    @staticmethod
    def create(session: Session, row: TeFactory2Result) -> TeFactory2Result:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: TeFactory2Result) -> TeFactory2Result:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def delete_by_pk(session: Session, work_date: object, use_tea_no: object, make_year: object, count: object) -> bool:
        row = TeFactory2ResultRepository.get_by_pk(session, work_date, use_tea_no, make_year, count)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True

    @staticmethod
    def delete_entity(session: Session, row: TeFactory2Result) -> None:
        session.delete(row)
        session.commit()
