"""tr_item 永続化アクセス（CRUD 雛形を含む）。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.tr_item.model import TrItem


class TrItemRepository:
    """商品 ``tr_item`` の Repository。"""

    # --- Read ---

    @staticmethod
    def list_all(session: Session) -> list[TrItem]:
        return list(session.scalars(select(TrItem)).all())

    @staticmethod
    def get_by_item_no(session: Session, item_no: int) -> TrItem | None:
        return session.get(TrItem, item_no)

    # --- Create / Update ---

    @staticmethod
    def create(session: Session, row: TrItem) -> TrItem:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: TrItem) -> TrItem:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    # --- Delete ---

    @staticmethod
    def delete_by_item_no(session: Session, item_no: int) -> bool:
        row = session.get(TrItem, item_no)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True

    @staticmethod
    def delete_entity(session: Session, row: TrItem) -> None:
        session.delete(row)
        session.commit()
