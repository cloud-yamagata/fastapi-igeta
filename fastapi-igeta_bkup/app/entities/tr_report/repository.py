"""tr_report 永続化アクセス（CRUD 雛形・自動生成）。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.tr_report.model import TrReport


class TrReportRepository:
    @staticmethod
    def list_all(session: Session) -> list[TrReport]:
        return list(session.scalars(select(TrReport)).all())

    @staticmethod
    def get_by_pk(session: Session, report_no: object) -> TrReport | None:
        return session.get(TrReport, report_no)

    @staticmethod
    def create(session: Session, row: TrReport) -> TrReport:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: TrReport) -> TrReport:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def delete_by_pk(session: Session, report_no: object) -> bool:
        row = session.get(TrReport, report_no)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True

    @staticmethod
    def delete_entity(session: Session, row: TrReport) -> None:
        session.delete(row)
        session.commit()
