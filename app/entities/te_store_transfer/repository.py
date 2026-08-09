"""te_store_transfer 永続化アクセス（CRUD 雛形・自動生成）。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.te_store_transfer.model import TeStoreTransfer


class TeStoreTransferRepository:
    @staticmethod
    def list_all(session: Session) -> list[TeStoreTransfer]:
        return list(session.scalars(select(TeStoreTransfer)).all())

    @staticmethod
    def get_by_pk(session: Session, transfer_no: object) -> TeStoreTransfer | None:
        return session.get(TeStoreTransfer, transfer_no)

    @staticmethod
    def create(session: Session, row: TeStoreTransfer) -> TeStoreTransfer:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: TeStoreTransfer) -> TeStoreTransfer:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def delete_by_pk(session: Session, transfer_no: object) -> bool:
        row = session.get(TeStoreTransfer, transfer_no)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True

    @staticmethod
    def delete_entity(session: Session, row: TeStoreTransfer) -> None:
        session.delete(row)
        session.commit()
