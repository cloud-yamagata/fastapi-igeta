"""firepan_no 永続化アクセス（CRUD 雛形・自動生成）。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.firepan_no.model import FirepanNo


class FirepanNoRepository:
    @staticmethod
    def list_all(session: Session) -> list[FirepanNo]:
        return list(session.scalars(select(FirepanNo)).all())

    @staticmethod
    def get_by_pk(session: Session, serial_no: object) -> FirepanNo | None:
        return session.get(FirepanNo, serial_no)

    @staticmethod
    def create(session: Session, row: FirepanNo) -> FirepanNo:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: FirepanNo) -> FirepanNo:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def delete_by_pk(session: Session, serial_no: object) -> bool:
        row = session.get(FirepanNo, serial_no)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True

    @staticmethod
    def delete_entity(session: Session, row: FirepanNo) -> None:
        session.delete(row)
        session.commit()
