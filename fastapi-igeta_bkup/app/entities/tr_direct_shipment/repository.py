"""tr_direct_shipment 永続化アクセス（CRUD 雛形・自動生成）。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.tr_direct_shipment.model import TrDirectShipment


class TrDirectShipmentRepository:
    @staticmethod
    def list_all(session: Session) -> list[TrDirectShipment]:
        return list(session.scalars(select(TrDirectShipment)).all())

    @staticmethod
    def get_by_pk(session: Session, direct_shipment_no: object) -> TrDirectShipment | None:
        return session.get(TrDirectShipment, direct_shipment_no)

    @staticmethod
    def create(session: Session, row: TrDirectShipment) -> TrDirectShipment:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: TrDirectShipment) -> TrDirectShipment:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def delete_by_pk(session: Session, direct_shipment_no: object) -> bool:
        row = session.get(TrDirectShipment, direct_shipment_no)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True

    @staticmethod
    def delete_entity(session: Session, row: TrDirectShipment) -> None:
        session.delete(row)
        session.commit()
