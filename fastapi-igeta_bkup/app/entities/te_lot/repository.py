"""te_lot 永続化アクセス（CRUD 雛形・自動生成）。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.te_lot.model import TeLot


class TeLotRepository:
    @staticmethod
    def list_all(session: Session) -> list[TeLot]:
        return list(session.scalars(select(TeLot)).all())

    @staticmethod
    def get_by_pk(session: Session, lot_no: object) -> TeLot | None:
        return session.get(TeLot, lot_no)

    @staticmethod
    def create(session: Session, row: TeLot) -> TeLot:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: TeLot) -> TeLot:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def delete_by_pk(session: Session, lot_no: object) -> bool:
        row = session.get(TeLot, lot_no)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True

    @staticmethod
    def delete_entity(session: Session, row: TeLot) -> None:
        session.delete(row)
        session.commit()
