"""te_grade 永続化アクセス（CRUD 雛形・自動生成）。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.te_grade.model import TeGrade


class TeGradeRepository:
    @staticmethod
    def list_all(session: Session) -> list[TeGrade]:
        return list(session.scalars(select(TeGrade)).all())

    @staticmethod
    def get_by_pk(session: Session, grade_no: object) -> TeGrade | None:
        return session.get(TeGrade, grade_no)

    @staticmethod
    def create(session: Session, row: TeGrade) -> TeGrade:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: TeGrade) -> TeGrade:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def delete_by_pk(session: Session, grade_no: object) -> bool:
        row = session.get(TeGrade, grade_no)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True

    @staticmethod
    def delete_entity(session: Session, row: TeGrade) -> None:
        session.delete(row)
        session.commit()
