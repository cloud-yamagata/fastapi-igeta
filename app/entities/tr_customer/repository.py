"""tr_customer 永続化アクセス（CRUD 雛形・自動生成）。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.tr_customer.model import TrCustomer


class TrCustomerRepository:
    @staticmethod
    def list_all(session: Session) -> list[TrCustomer]:
        return list(session.scalars(select(TrCustomer)).all())

    @staticmethod
    def get_by_pk(session: Session, customer_no: object) -> TrCustomer | None:
        return session.get(TrCustomer, customer_no)

    @staticmethod
    def create(session: Session, row: TrCustomer) -> TrCustomer:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: TrCustomer) -> TrCustomer:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def delete_by_pk(session: Session, customer_no: object) -> bool:
        row = session.get(TrCustomer, customer_no)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True

    @staticmethod
    def delete_entity(session: Session, row: TrCustomer) -> None:
        session.delete(row)
        session.commit()
