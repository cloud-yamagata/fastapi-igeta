"""te_store_transfer_fa2 永続化アクセス（CRUD 雛形・自動生成）。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.te_store_transfer_fa2.model import TeStoreTransferFa2


class TeStoreTransferFa2Repository:
    @staticmethod
    def list_all(session: Session) -> list[TeStoreTransferFa2]:
        return list(session.scalars(select(TeStoreTransferFa2)).all())

    @staticmethod
    def get_by_pk(session: Session, transfer_no: object) -> TeStoreTransferFa2 | None:
        return session.get(TeStoreTransferFa2, transfer_no)

    @staticmethod
    def create(session: Session, row: TeStoreTransferFa2) -> TeStoreTransferFa2:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: TeStoreTransferFa2) -> TeStoreTransferFa2:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def delete_by_pk(session: Session, transfer_no: object) -> bool:
        row = session.get(TeStoreTransferFa2, transfer_no)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True

    @staticmethod
    def delete_entity(session: Session, row: TeStoreTransferFa2) -> None:
        session.delete(row)
        session.commit()
