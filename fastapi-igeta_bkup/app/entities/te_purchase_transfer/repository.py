"""te_purchase_transfer 永続化アクセス（CRUD 雛形・自動生成）。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.te_purchase_transfer.model import TePurchaseTransfer


class TePurchaseTransferRepository:
    @staticmethod
    def list_all(session: Session) -> list[TePurchaseTransfer]:
        return list(session.scalars(select(TePurchaseTransfer)).all())

    @staticmethod
    def get_by_pk(session: Session, year: object, purchase: object, bid_no: object, result_type: object, transfer: object) -> TePurchaseTransfer | None:
        stmt = select(TePurchaseTransfer).where((TePurchaseTransfer.year == year) & (TePurchaseTransfer.purchase == purchase) & (TePurchaseTransfer.bid_no == bid_no) & (TePurchaseTransfer.result_type == result_type) & (TePurchaseTransfer.transfer == transfer))
        return session.scalars(stmt).first()

    @staticmethod
    def create(session: Session, row: TePurchaseTransfer) -> TePurchaseTransfer:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: TePurchaseTransfer) -> TePurchaseTransfer:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def delete_by_pk(session: Session, year: object, purchase: object, bid_no: object, result_type: object, transfer: object) -> bool:
        row = TePurchaseTransferRepository.get_by_pk(session, year, purchase, bid_no, result_type, transfer)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True

    @staticmethod
    def delete_entity(session: Session, row: TePurchaseTransfer) -> None:
        session.delete(row)
        session.commit()
