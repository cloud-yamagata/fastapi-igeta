"""tr_report_item 永続化アクセス（CRUD 雛形・自動生成）。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.tr_report_item.model import TrReportItem


class TrReportItemRepository:
    @staticmethod
    def list_all(session: Session) -> list[TrReportItem]:
        return list(session.scalars(select(TrReportItem)).all())

    @staticmethod
    def get_by_pk(session: Session, report_no: object, field_no: object) -> TrReportItem | None:
        stmt = select(TrReportItem).where((TrReportItem.report_no == report_no) & (TrReportItem.field_no == field_no))
        return session.scalars(stmt).first()

    @staticmethod
    def create(session: Session, row: TrReportItem) -> TrReportItem:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: TrReportItem) -> TrReportItem:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def delete_by_pk(session: Session, report_no: object, field_no: object) -> bool:
        row = TrReportItemRepository.get_by_pk(session, report_no, field_no)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True

    @staticmethod
    def delete_entity(session: Session, row: TrReportItem) -> None:
        session.delete(row)
        session.commit()
