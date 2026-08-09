"""te_material_result 永続化アクセス（CRUD 雛形・自動生成）。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.te_material_result.model import TeMaterialResult


class TeMaterialResultRepository:
    @staticmethod
    def list_all(session: Session) -> list[TeMaterialResult]:
        return list(session.scalars(select(TeMaterialResult)).all())

    @staticmethod
    def get_by_pk(session: Session, year: object, purchase: object, product_no: object, purchase_date: object, tea_rank: object, rank: object) -> TeMaterialResult | None:
        stmt = select(TeMaterialResult).where((TeMaterialResult.year == year) & (TeMaterialResult.purchase == purchase) & (TeMaterialResult.product_no == product_no) & (TeMaterialResult.purchase_date == purchase_date) & (TeMaterialResult.tea_rank == tea_rank) & (TeMaterialResult.rank == rank))
        return session.scalars(stmt).first()

    @staticmethod
    def create(session: Session, row: TeMaterialResult) -> TeMaterialResult:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: TeMaterialResult) -> TeMaterialResult:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def delete_by_pk(session: Session, year: object, purchase: object, product_no: object, purchase_date: object, tea_rank: object, rank: object) -> bool:
        row = TeMaterialResultRepository.get_by_pk(session, year, purchase, product_no, purchase_date, tea_rank, rank)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True

    @staticmethod
    def delete_entity(session: Session, row: TeMaterialResult) -> None:
        session.delete(row)
        session.commit()
