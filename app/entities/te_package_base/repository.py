"""te_package_base 永続化アクセス（CRUD 雛形・自動生成）。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.te_package_base.model import TePackageBase


class TePackageBaseRepository:
    @staticmethod
    def list_all(session: Session) -> list[TePackageBase]:
        return list(session.scalars(select(TePackageBase)).all())

    @staticmethod
    def get_by_pk(session: Session, product_no: object) -> TePackageBase | None:
        return session.get(TePackageBase, product_no)

    @staticmethod
    def create(session: Session, row: TePackageBase) -> TePackageBase:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: TePackageBase) -> TePackageBase:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def delete_by_pk(session: Session, product_no: object) -> bool:
        row = session.get(TePackageBase, product_no)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True

    @staticmethod
    def delete_entity(session: Session, row: TePackageBase) -> None:
        session.delete(row)
        session.commit()
