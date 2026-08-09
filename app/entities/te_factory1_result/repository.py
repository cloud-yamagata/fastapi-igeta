"""te_factory1_result 永続化アクセス（CRUD 雛形・自動生成）。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.te_factory1_result.model import TeFactory1Result


class TeFactory1ResultRepository:
    @staticmethod
    def list_all(session: Session) -> list[TeFactory1Result]:
        return list(session.scalars(select(TeFactory1Result)).all())

    @staticmethod
    def get_by_pk(session: Session, lot_no: object) -> TeFactory1Result | None:
        return session.get(TeFactory1Result, lot_no)

    @staticmethod
    def create(session: Session, row: TeFactory1Result) -> TeFactory1Result:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: TeFactory1Result) -> TeFactory1Result:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def delete_by_pk(session: Session, lot_no: object) -> bool:
        row = session.get(TeFactory1Result, lot_no)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True

    @staticmethod
    def delete_entity(session: Session, row: TeFactory1Result) -> None:
        session.delete(row)
        session.commit()
