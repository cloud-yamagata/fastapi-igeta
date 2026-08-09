"""te_lot_bom 永続化アクセス（CRUD 雛形・自動生成）。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.te_lot_bom.model import TeLotBom


class TeLotBomRepository:
    @staticmethod
    def list_all(session: Session) -> list[TeLotBom]:
        return list(session.scalars(select(TeLotBom)).all())

    @staticmethod
    def get_by_pk(session: Session, lot_no: object, part_no: object) -> TeLotBom | None:
        stmt = select(TeLotBom).where((TeLotBom.lot_no == lot_no) & (TeLotBom.part_no == part_no))
        return session.scalars(stmt).first()

    @staticmethod
    def create(session: Session, row: TeLotBom) -> TeLotBom:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: TeLotBom) -> TeLotBom:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def delete_by_pk(session: Session, lot_no: object, part_no: object) -> bool:
        row = TeLotBomRepository.get_by_pk(session, lot_no, part_no)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True

    @staticmethod
    def delete_entity(session: Session, row: TeLotBom) -> None:
        session.delete(row)
        session.commit()
