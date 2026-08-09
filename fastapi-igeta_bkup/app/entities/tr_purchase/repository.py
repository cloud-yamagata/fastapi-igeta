"""tr_purchase 永続化アクセス（CRUD 雛形・自動生成）。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.tr_purchase.model import TrPurchase


class TrPurchaseRepository:
    @staticmethod
    def list_all(session: Session) -> list[TrPurchase]:
        return list(session.scalars(select(TrPurchase)).all())

    @staticmethod
    def get_by_pk(session: Session, purchase_no: object) -> TrPurchase | None:
        return session.get(TrPurchase, purchase_no)

    @staticmethod
    def create(session: Session, row: TrPurchase) -> TrPurchase:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: TrPurchase) -> TrPurchase:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def delete_by_pk(session: Session, purchase_no: object) -> bool:
        row = session.get(TrPurchase, purchase_no)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True

    @staticmethod
    def delete_entity(session: Session, row: TrPurchase) -> None:
        session.delete(row)
        session.commit()
