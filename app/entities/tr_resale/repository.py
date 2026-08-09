"""tr_resale 永続化アクセス（CRUD 雛形・自動生成）。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.tr_resale.model import TrResale


class TrResaleRepository:
    @staticmethod
    def list_all(session: Session) -> list[TrResale]:
        return list(session.scalars(select(TrResale)).all())

    @staticmethod
    def get_by_pk(session: Session, resale: object) -> TrResale | None:
        return session.get(TrResale, resale)

    @staticmethod
    def create(session: Session, row: TrResale) -> TrResale:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: TrResale) -> TrResale:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def delete_by_pk(session: Session, resale: object) -> bool:
        row = session.get(TrResale, resale)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True

    @staticmethod
    def delete_entity(session: Session, row: TrResale) -> None:
        session.delete(row)
        session.commit()
