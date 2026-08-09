"""bulk_no 永続化アクセス（CRUD 雛形・自動生成）。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.bulk_no.model import BulkNo


class BulkNoRepository:
    @staticmethod
    def list_all(session: Session) -> list[BulkNo]:
        return list(session.scalars(select(BulkNo)).all())

    @staticmethod
    def get_by_pk(session: Session, serial_no: object) -> BulkNo | None:
        return session.get(BulkNo, serial_no)

    @staticmethod
    def create(session: Session, row: BulkNo) -> BulkNo:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: BulkNo) -> BulkNo:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def delete_by_pk(session: Session, serial_no: object) -> bool:
        row = session.get(BulkNo, serial_no)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True

    @staticmethod
    def delete_entity(session: Session, row: BulkNo) -> None:
        session.delete(row)
        session.commit()
