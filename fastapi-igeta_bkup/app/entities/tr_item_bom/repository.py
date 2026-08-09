"""tr_item_bom 永続化アクセス（CRUD 雛形・自動生成）。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.tr_item_bom.model import TrItemBom


class TrItemBomRepository:
    @staticmethod
    def list_all(session: Session) -> list[TrItemBom]:
        return list(session.scalars(select(TrItemBom)).all())

    @staticmethod
    def get_by_pk(session: Session, parent_item_no: object) -> TrItemBom | None:
        return session.get(TrItemBom, parent_item_no)

    @staticmethod
    def create(session: Session, row: TrItemBom) -> TrItemBom:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: TrItemBom) -> TrItemBom:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def delete_by_pk(session: Session, parent_item_no: object) -> bool:
        row = session.get(TrItemBom, parent_item_no)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True

    @staticmethod
    def delete_entity(session: Session, row: TrItemBom) -> None:
        session.delete(row)
        session.commit()
