"""te_blend_lot 永続化アクセス。"""
from __future__ import annotations

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.entities.te_blend_lot.model import TeBlendLot


class TeBlendLotRepository:
    """ブレンドロット ``te_blend_lot`` の Repository。"""

    @staticmethod
    def list_all(session: Session) -> list[TeBlendLot]:
        stmt = select(TeBlendLot).order_by(TeBlendLot.product_no.desc())
        return list(session.scalars(stmt).all())

    @staticmethod
    def get_by_product_no(session: Session, product_no: int) -> TeBlendLot | None:
        return session.get(TeBlendLot, product_no)

    @staticmethod
    def persist(session: Session, row: TeBlendLot) -> TeBlendLot:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def delete_by_product_nos(session: Session, product_nos: list[int]) -> int:
        if not product_nos:
            return 0
        uniq = list(dict.fromkeys(product_nos))
        res = session.execute(delete(TeBlendLot).where(TeBlendLot.product_no.in_(uniq)))
        session.commit()
        return int(res.rowcount or 0)
