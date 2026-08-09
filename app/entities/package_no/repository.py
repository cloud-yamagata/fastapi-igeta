"""package_no 永続化アクセス（CRUD 雛形）。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.package_no.model import PackageNo


class PackageNoRepository:
    @staticmethod
    def list_all(session: Session) -> list[PackageNo]:
        return list(session.scalars(select(PackageNo)).all())

    @staticmethod
    def get_by_pk(session: Session, serial_no: object) -> PackageNo | None:
        return session.get(PackageNo, serial_no)

    @staticmethod
    def create(session: Session, row: PackageNo) -> PackageNo:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row
