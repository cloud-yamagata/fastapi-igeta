"""te_blend_lot_part 永続化アクセス（CRUD 雛形・自動生成）。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.te_blend_lot_part.model import TeBlendLotPart


class TeBlendLotPartRepository:
    @staticmethod
    def list_all(session: Session) -> list[TeBlendLotPart]:
        return list(session.scalars(select(TeBlendLotPart)).all())

    @staticmethod
    def get_by_pk(session: Session, product_no: object, part_lot_no: object) -> TeBlendLotPart | None:
        stmt = select(TeBlendLotPart).where((TeBlendLotPart.product_no == product_no) & (TeBlendLotPart.part_lot_no == part_lot_no))
        return session.scalars(stmt).first()

    @staticmethod
    def create(session: Session, row: TeBlendLotPart) -> TeBlendLotPart:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: TeBlendLotPart) -> TeBlendLotPart:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def delete_by_pk(session: Session, product_no: object, part_lot_no: object) -> bool:
        row = TeBlendLotPartRepository.get_by_pk(session, product_no, part_lot_no)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True

    @staticmethod
    def delete_entity(session: Session, row: TeBlendLotPart) -> None:
        session.delete(row)
        session.commit()
