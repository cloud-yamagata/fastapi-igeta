"""vi_factory3_stoc 参照。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.vi_factory3_stoc.model import ViFactory3Stoc


class ViFactory3StocRepository:
    @staticmethod
    def list_all(session: Session) -> list[ViFactory3Stoc]:
        return list(session.scalars(select(ViFactory3Stoc)).all())
