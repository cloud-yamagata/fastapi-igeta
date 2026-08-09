"""te_lot_base 永続化アクセス（CRUD 雛形・自動生成）。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.te_lot_base.model import TeLotBase


class TeLotBaseRepository:
    @staticmethod
    def list_all(session: Session) -> list[TeLotBase]:
        return list(session.scalars(select(TeLotBase)).all())

    @staticmethod
    def get_by_pk(session: Session, lot_no: object) -> TeLotBase | None:
        return session.get(TeLotBase, lot_no)

    @staticmethod
    def create(session: Session, row: TeLotBase) -> TeLotBase:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: TeLotBase) -> TeLotBase:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def delete_by_pk(session: Session, lot_no: object) -> bool:
        row = session.get(TeLotBase, lot_no)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True

    @staticmethod
    def delete_entity(session: Session, row: TeLotBase) -> None:
        session.delete(row)
        session.commit()
