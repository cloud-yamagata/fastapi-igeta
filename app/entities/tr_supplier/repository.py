"""tr_supplier 永続化アクセス（CRUD 雛形・自動生成）。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.tr_supplier.model import TrSupplier


class TrSupplierRepository:
    @staticmethod
    def list_all(session: Session) -> list[TrSupplier]:
        return list(session.scalars(select(TrSupplier)).all())

    @staticmethod
    def get_by_pk(session: Session, supplier_no: object) -> TrSupplier | None:
        return session.get(TrSupplier, supplier_no)

    @staticmethod
    def create(session: Session, row: TrSupplier) -> TrSupplier:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: TrSupplier) -> TrSupplier:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def delete_by_pk(session: Session, supplier_no: object) -> bool:
        row = session.get(TrSupplier, supplier_no)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True

    @staticmethod
    def delete_entity(session: Session, row: TrSupplier) -> None:
        session.delete(row)
        session.commit()
