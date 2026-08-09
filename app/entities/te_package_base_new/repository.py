"""te_package_base_new 永続化アクセス。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.te_package_base_new.model import TePackageBaseNew


class TePackageBaseNewRepository:
    @staticmethod
    def list_all(session: Session) -> list[TePackageBaseNew]:
        return list(session.scalars(select(TePackageBaseNew)).all())
