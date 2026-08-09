"""te_lot_categorys_finish 永続化アクセス（CRUD 雛形・自動生成）。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.te_lot_categorys_finish.model import TeLotCategorysFinish


class TeLotCategorysFinishRepository:
    @staticmethod
    def list_all(session: Session) -> list[TeLotCategorysFinish]:
        return list(session.scalars(select(TeLotCategorysFinish)).all())

    @staticmethod
    def get_by_pk(session: Session, lot_no: object) -> TeLotCategorysFinish | None:
        return session.get(TeLotCategorysFinish, lot_no)

    @staticmethod
    def create(session: Session, row: TeLotCategorysFinish) -> TeLotCategorysFinish:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: TeLotCategorysFinish) -> TeLotCategorysFinish:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def delete_by_pk(session: Session, lot_no: object) -> bool:
        row = session.get(TeLotCategorysFinish, lot_no)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True

    @staticmethod
    def delete_entity(session: Session, row: TeLotCategorysFinish) -> None:
        session.delete(row)
        session.commit()
