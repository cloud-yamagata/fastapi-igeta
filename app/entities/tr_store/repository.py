"""tr_store 永続化アクセス（CRUD 雛形・自動生成）。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.tr_store.model import TrStore


class TrStoreRepository:
    @staticmethod
    def list_all(session: Session) -> list[TrStore]:
        return list(session.scalars(select(TrStore)).all())

    @staticmethod
    def get_by_pk(session: Session, store_no: object) -> TrStore | None:
        return session.get(TrStore, store_no)

    @staticmethod
    def create(session: Session, row: TrStore) -> TrStore:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: TrStore) -> TrStore:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def delete_by_pk(session: Session, store_no: object) -> bool:
        row = session.get(TrStore, store_no)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True

    @staticmethod
    def delete_entity(session: Session, row: TrStore) -> None:
        session.delete(row)
        session.commit()
