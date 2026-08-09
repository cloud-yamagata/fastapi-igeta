"""tr_item_group 永続化アクセス（CRUD 雛形・自動生成）。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.tr_item_group.model import TrItemGroup


class TrItemGroupRepository:
    @staticmethod
    def list_all(session: Session) -> list[TrItemGroup]:
        return list(session.scalars(select(TrItemGroup)).all())

    @staticmethod
    def get_by_pk(session: Session, item_group_no: object) -> TrItemGroup | None:
        return session.get(TrItemGroup, item_group_no)

    @staticmethod
    def create(session: Session, row: TrItemGroup) -> TrItemGroup:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: TrItemGroup) -> TrItemGroup:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def delete_by_pk(session: Session, item_group_no: object) -> bool:
        row = session.get(TrItemGroup, item_group_no)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True

    @staticmethod
    def delete_entity(session: Session, row: TrItemGroup) -> None:
        session.delete(row)
        session.commit()
