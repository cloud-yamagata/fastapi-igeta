"""te_lot_divide 永続化アクセス（CRUD 雛形・自動生成）。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.te_lot_divide.model import TeLotDivide


class TeLotDivideRepository:
    @staticmethod
    def list_all(session: Session) -> list[TeLotDivide]:
        return list(session.scalars(select(TeLotDivide)).all())

    @staticmethod
    def get_by_pk(session: Session, lot_no: object, divide_no: object) -> TeLotDivide | None:
        stmt = select(TeLotDivide).where((TeLotDivide.lot_no == lot_no) & (TeLotDivide.divide_no == divide_no))
        return session.scalars(stmt).first()

    @staticmethod
    def create(session: Session, row: TeLotDivide) -> TeLotDivide:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: TeLotDivide) -> TeLotDivide:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def delete_by_pk(session: Session, lot_no: object, divide_no: object) -> bool:
        row = TeLotDivideRepository.get_by_pk(session, lot_no, divide_no)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True

    @staticmethod
    def delete_entity(session: Session, row: TeLotDivide) -> None:
        session.delete(row)
        session.commit()
