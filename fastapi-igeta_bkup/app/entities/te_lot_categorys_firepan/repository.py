"""te_lot_categorys_firepan 永続化アクセス（CRUD 雛形・自動生成）。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.te_lot_categorys_firepan.model import TeLotCategorysFirepan


class TeLotCategorysFirepanRepository:
    @staticmethod
    def list_all(session: Session) -> list[TeLotCategorysFirepan]:
        return list(session.scalars(select(TeLotCategorysFirepan)).all())

    @staticmethod
    def get_by_pk(session: Session, lot_no: object) -> TeLotCategorysFirepan | None:
        return session.get(TeLotCategorysFirepan, lot_no)

    @staticmethod
    def create(session: Session, row: TeLotCategorysFirepan) -> TeLotCategorysFirepan:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: TeLotCategorysFirepan) -> TeLotCategorysFirepan:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def delete_by_pk(session: Session, lot_no: object) -> bool:
        row = session.get(TeLotCategorysFirepan, lot_no)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True

    @staticmethod
    def delete_entity(session: Session, row: TeLotCategorysFirepan) -> None:
        session.delete(row)
        session.commit()
