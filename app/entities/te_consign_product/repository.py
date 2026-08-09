"""te_consign_product 永続化アクセス（CRUD 雛形・自動生成）。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.te_consign_product.model import TeConsignProduct


class TeConsignProductRepository:
    @staticmethod
    def list_all(session: Session) -> list[TeConsignProduct]:
        return list(session.scalars(select(TeConsignProduct)).all())

    @staticmethod
    def get_by_pk(session: Session, consign_no: object) -> TeConsignProduct | None:
        return session.get(TeConsignProduct, consign_no)

    @staticmethod
    def create(session: Session, row: TeConsignProduct) -> TeConsignProduct:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: TeConsignProduct) -> TeConsignProduct:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def delete_by_pk(session: Session, consign_no: object) -> bool:
        row = session.get(TeConsignProduct, consign_no)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True

    @staticmethod
    def delete_entity(session: Session, row: TeConsignProduct) -> None:
        session.delete(row)
        session.commit()
