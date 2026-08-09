"""finish_no 永続化アクセス（CRUD 雛形・自動生成）。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.finish_no.model import FinishNo


class FinishNoRepository:
    @staticmethod
    def list_all(session: Session) -> list[FinishNo]:
        return list(session.scalars(select(FinishNo)).all())

    @staticmethod
    def get_by_pk(session: Session, serial_no: object) -> FinishNo | None:
        return session.get(FinishNo, serial_no)

    @staticmethod
    def create(session: Session, row: FinishNo) -> FinishNo:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: FinishNo) -> FinishNo:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def delete_by_pk(session: Session, serial_no: object) -> bool:
        row = session.get(FinishNo, serial_no)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True

    @staticmethod
    def delete_entity(session: Session, row: FinishNo) -> None:
        session.delete(row)
        session.commit()
