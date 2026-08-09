"""te_material_purchase 永続化アクセス（CRUD 雛形・自動生成）。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.te_material_purchase.model import TeMaterialPurchase


class TeMaterialPurchaseRepository:
    @staticmethod
    def list_all(session: Session) -> list[TeMaterialPurchase]:
        return list(session.scalars(select(TeMaterialPurchase)).all())

    @staticmethod
    def get_by_pk(session: Session, purchase_no: object) -> TeMaterialPurchase | None:
        return session.get(TeMaterialPurchase, purchase_no)

    @staticmethod
    def create(session: Session, row: TeMaterialPurchase) -> TeMaterialPurchase:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: TeMaterialPurchase) -> TeMaterialPurchase:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def delete_by_pk(session: Session, purchase_no: object) -> bool:
        row = session.get(TeMaterialPurchase, purchase_no)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True

    @staticmethod
    def delete_entity(session: Session, row: TeMaterialPurchase) -> None:
        session.delete(row)
        session.commit()
