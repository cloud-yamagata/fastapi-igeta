"""te_lot_part 永続化アクセス（CRUD 雛形・自動生成）。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.te_lot_part.model import TeLotPart


class TeLotPartRepository:
    @staticmethod
    def list_all(session: Session) -> list[TeLotPart]:
        return list(session.scalars(select(TeLotPart)).all())

    @staticmethod
    def get_by_pk(session: Session, lot_no: object, part_no: object) -> TeLotPart | None:
        stmt = select(TeLotPart).where((TeLotPart.lot_no == lot_no) & (TeLotPart.part_no == part_no))
        return session.scalars(stmt).first()

    @staticmethod
    def create(session: Session, row: TeLotPart) -> TeLotPart:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: TeLotPart) -> TeLotPart:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def delete_by_pk(session: Session, lot_no: object, part_no: object) -> bool:
        row = TeLotPartRepository.get_by_pk(session, lot_no, part_no)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True

    @staticmethod
    def delete_entity(session: Session, row: TeLotPart) -> None:
        session.delete(row)
        session.commit()
