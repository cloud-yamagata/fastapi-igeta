"""te_package_categorys_new 永続化アクセス。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.te_package_categorys_new.model import TePackageCategorysNew


class TePackageCategorysNewRepository:
    @staticmethod
    def list_all(session: Session) -> list[TePackageCategorysNew]:
        return list(session.scalars(select(TePackageCategorysNew)).all())
