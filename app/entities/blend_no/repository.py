"""blend_no 永続化アクセス（CRUD 雛形・自動生成）。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.blend_no.model import BlendNo


class BlendNoRepository:
    @staticmethod
    def list_all(session: Session) -> list[BlendNo]:
        return list(session.scalars(select(BlendNo)).all())

    @staticmethod
    def get_by_pk(session: Session, serial_no: object) -> BlendNo | None:
        return session.get(BlendNo, serial_no)

    @staticmethod
    def create(session: Session, row: BlendNo) -> BlendNo:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: BlendNo) -> BlendNo:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def delete_by_pk(session: Session, serial_no: object) -> bool:
        row = session.get(BlendNo, serial_no)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True

    @staticmethod
    def delete_entity(session: Session, row: BlendNo) -> None:
        session.delete(row)
        session.commit()
