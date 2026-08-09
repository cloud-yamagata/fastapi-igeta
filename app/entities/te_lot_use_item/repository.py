"""te_lot_use_item 永続化アクセス（CRUD 雛形・自動生成）。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.te_lot_use_item.model import TeLotUseItem


class TeLotUseItemRepository:
    @staticmethod
    def list_all(session: Session) -> list[TeLotUseItem]:
        return list(session.scalars(select(TeLotUseItem)).all())

    @staticmethod
    def get_by_pk(session: Session, lot_no: object) -> TeLotUseItem | None:
        return session.get(TeLotUseItem, lot_no)

    @staticmethod
    def create(session: Session, row: TeLotUseItem) -> TeLotUseItem:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: TeLotUseItem) -> TeLotUseItem:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def delete_by_pk(session: Session, lot_no: object) -> bool:
        row = session.get(TeLotUseItem, lot_no)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True

    @staticmethod
    def delete_entity(session: Session, row: TeLotUseItem) -> None:
        session.delete(row)
        session.commit()
