"""te_factory3_stock 永続化アクセス（CRUD 雛形・自動生成）。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.te_factory3_stock.model import TeFactory3Stock


class TeFactory3StockRepository:
    @staticmethod
    def list_all(session: Session) -> list[TeFactory3Stock]:
        return list(session.scalars(select(TeFactory3Stock)).all())

    @staticmethod
    def get_by_pk(session: Session, stock_date: object, use_tea_no: object, make_year: object, count: object) -> TeFactory3Stock | None:
        stmt = select(TeFactory3Stock).where((TeFactory3Stock.stock_date == stock_date) & (TeFactory3Stock.use_tea_no == use_tea_no) & (TeFactory3Stock.make_year == make_year) & (TeFactory3Stock.count == count))
        return session.scalars(stmt).first()

    @staticmethod
    def create(session: Session, row: TeFactory3Stock) -> TeFactory3Stock:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: TeFactory3Stock) -> TeFactory3Stock:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def delete_by_pk(session: Session, stock_date: object, use_tea_no: object, make_year: object, count: object) -> bool:
        row = TeFactory3StockRepository.get_by_pk(session, stock_date, use_tea_no, make_year, count)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True

    @staticmethod
    def delete_entity(session: Session, row: TeFactory3Stock) -> None:
        session.delete(row)
        session.commit()
