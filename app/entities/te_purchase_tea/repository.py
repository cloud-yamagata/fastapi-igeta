"""te_purchase_tea 永続化アクセス（CRUD 雛形・自動生成）。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.te_purchase_tea.model import TePurchaseTea


class TePurchaseTeaRepository:
    @staticmethod
    def list_all(session: Session) -> list[TePurchaseTea]:
        return list(session.scalars(select(TePurchaseTea)).all())

    @staticmethod
    def get_by_pk(session: Session, year: object, purchase: object, bid_no: object) -> TePurchaseTea | None:
        stmt = select(TePurchaseTea).where((TePurchaseTea.year == year) & (TePurchaseTea.purchase == purchase) & (TePurchaseTea.bid_no == bid_no))
        return session.scalars(stmt).first()

    @staticmethod
    def create(session: Session, row: TePurchaseTea) -> TePurchaseTea:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: TePurchaseTea) -> TePurchaseTea:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def delete_by_pk(session: Session, year: object, purchase: object, bid_no: object) -> bool:
        row = TePurchaseTeaRepository.get_by_pk(session, year, purchase, bid_no)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True

    @staticmethod
    def delete_entity(session: Session, row: TePurchaseTea) -> None:
        session.delete(row)
        session.commit()
