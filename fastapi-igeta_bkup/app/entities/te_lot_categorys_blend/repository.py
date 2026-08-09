"""te_lot_categorys_blend 永続化アクセス（CRUD 雛形・自動生成）。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.te_lot_categorys_blend.model import TeLotCategorysBlend


class TeLotCategorysBlendRepository:
    @staticmethod
    def list_all(session: Session) -> list[TeLotCategorysBlend]:
        return list(session.scalars(select(TeLotCategorysBlend)).all())

    @staticmethod
    def get_by_pk(session: Session, lot_no: object) -> TeLotCategorysBlend | None:
        return session.get(TeLotCategorysBlend, lot_no)

    @staticmethod
    def create(session: Session, row: TeLotCategorysBlend) -> TeLotCategorysBlend:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: TeLotCategorysBlend) -> TeLotCategorysBlend:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def delete_by_pk(session: Session, lot_no: object) -> bool:
        row = session.get(TeLotCategorysBlend, lot_no)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True

    @staticmethod
    def delete_entity(session: Session, row: TeLotCategorysBlend) -> None:
        session.delete(row)
        session.commit()
