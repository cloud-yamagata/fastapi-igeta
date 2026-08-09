"""tr_constant 永続化アクセス（CRUD 雛形を含む）。"""
from __future__ import annotations

from sqlalchemy import asc, select
from sqlalchemy.orm import Session

from app.entities.tr_constant.model import TrConstant


class TrConstantRepository:
    """システム定数 ``tr_constant`` の Repository（複合 PK）。"""

    # --- Read ---

    @staticmethod
    def list_all(session: Session) -> list[TrConstant]:
        stmt = select(TrConstant).order_by(asc(TrConstant.const_field), asc(TrConstant.const_value))
        return list(session.scalars(stmt).all())

    @staticmethod
    def list_filtered(session: Session, const_field: str | None) -> list[TrConstant]:
        stmt = select(TrConstant)
        if const_field is not None and str(const_field).strip() != "":
            stmt = stmt.where(TrConstant.const_field == str(const_field).strip())
        stmt = stmt.order_by(asc(TrConstant.const_value), asc(TrConstant.display_order))
        return list(session.scalars(stmt).all())

    @staticmethod
    def get_by_natural_key(session: Session, const_field: str, const_value: str) -> TrConstant | None:
        stmt = select(TrConstant).where(
            TrConstant.const_field == const_field,
            TrConstant.const_value == const_value,
        )
        return session.scalars(stmt).first()

    # --- Create / Update ---

    @staticmethod
    def create(session: Session, row: TrConstant) -> TrConstant:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: TrConstant) -> TrConstant:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    # --- Delete ---

    @staticmethod
    def delete_by_natural_key(session: Session, const_field: str, const_value: str) -> bool:
        row = TrConstantRepository.get_by_natural_key(session, const_field, const_value)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True

    @staticmethod
    def delete_entity(session: Session, row: TrConstant) -> None:
        session.delete(row)
        session.commit()
