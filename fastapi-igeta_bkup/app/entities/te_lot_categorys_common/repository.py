"""te_lot_categorys_common 永続化アクセス（CRUD 雛形・自動生成）。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.te_lot_categorys_common.model import TeLotCategorysCommon


class TeLotCategorysCommonRepository:
    @staticmethod
    def list_all(session: Session) -> list[TeLotCategorysCommon]:
        return list(session.scalars(select(TeLotCategorysCommon)).all())

    @staticmethod
    def get_by_pk(session: Session, lot_no: object) -> TeLotCategorysCommon | None:
        return session.get(TeLotCategorysCommon, lot_no)

    @staticmethod
    def create(session: Session, row: TeLotCategorysCommon) -> TeLotCategorysCommon:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: TeLotCategorysCommon) -> TeLotCategorysCommon:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def delete_by_pk(session: Session, lot_no: object) -> bool:
        row = session.get(TeLotCategorysCommon, lot_no)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True

    @staticmethod
    def delete_entity(session: Session, row: TeLotCategorysCommon) -> None:
        session.delete(row)
        session.commit()
