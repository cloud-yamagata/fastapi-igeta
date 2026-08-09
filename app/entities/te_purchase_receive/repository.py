"""te_purchase_receive 永続化アクセス（CRUD 雛形・自動生成）。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.te_purchase_receive.model import TePurchaseReceive


class TePurchaseReceiveRepository:
    @staticmethod
    def list_all(session: Session) -> list[TePurchaseReceive]:
        return list(session.scalars(select(TePurchaseReceive)).all())

    @staticmethod
    def get_by_pk(session: Session, year: object, purchase: object, bid_no: object, receive_date: object) -> TePurchaseReceive | None:
        stmt = select(TePurchaseReceive).where((TePurchaseReceive.year == year) & (TePurchaseReceive.purchase == purchase) & (TePurchaseReceive.bid_no == bid_no) & (TePurchaseReceive.receive_date == receive_date))
        return session.scalars(stmt).first()

    @staticmethod
    def create(session: Session, row: TePurchaseReceive) -> TePurchaseReceive:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: TePurchaseReceive) -> TePurchaseReceive:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def delete_by_pk(session: Session, year: object, purchase: object, bid_no: object, receive_date: object) -> bool:
        row = TePurchaseReceiveRepository.get_by_pk(session, year, purchase, bid_no, receive_date)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True

    @staticmethod
    def delete_entity(session: Session, row: TePurchaseReceive) -> None:
        session.delete(row)
        session.commit()
