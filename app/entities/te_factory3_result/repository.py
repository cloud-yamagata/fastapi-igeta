"""te_factory3_result 永続化アクセス（CRUD 雛形・自動生成）。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.te_factory3_result.model import TeFactory3Result


class TeFactory3ResultRepository:
    @staticmethod
    def list_all(session: Session) -> list[TeFactory3Result]:
        return list(session.scalars(select(TeFactory3Result)).all())

    @staticmethod
    def get_by_pk(session: Session, work_date: object, item_no: object) -> TeFactory3Result | None:
        stmt = select(TeFactory3Result).where((TeFactory3Result.work_date == work_date) & (TeFactory3Result.item_no == item_no))
        return session.scalars(stmt).first()

    @staticmethod
    def create(session: Session, row: TeFactory3Result) -> TeFactory3Result:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: TeFactory3Result) -> TeFactory3Result:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def delete_by_pk(session: Session, work_date: object, item_no: object) -> bool:
        row = TeFactory3ResultRepository.get_by_pk(session, work_date, item_no)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True

    @staticmethod
    def delete_entity(session: Session, row: TeFactory3Result) -> None:
        session.delete(row)
        session.commit()
