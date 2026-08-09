"""te_material 永続化アクセス（CRUD 雛形を含む）。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.te_material.model import TeMaterial


class TeMaterialRepository:
    """原料情報 ``te_material`` の Repository。

    ルーターが直接使わないメソッドも、雛形として定義する。
    """

    # --- Read ---

    @staticmethod
    def list_all(session: Session) -> list[TeMaterial]:
        return list(session.scalars(select(TeMaterial)).all())

    @staticmethod
    def get_by_material_no(session: Session, material_no: int) -> TeMaterial | None:
        return session.get(TeMaterial, material_no)

    # --- Create / Update ---

    @staticmethod
    def create(session: Session, row: TeMaterial) -> TeMaterial:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: TeMaterial) -> TeMaterial:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    # --- Delete ---

    @staticmethod
    def delete_by_material_no(session: Session, material_no: int) -> bool:
        row = session.get(TeMaterial, material_no)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True

    @staticmethod
    def delete_entity(session: Session, row: TeMaterial) -> None:
        session.delete(row)
        session.commit()
