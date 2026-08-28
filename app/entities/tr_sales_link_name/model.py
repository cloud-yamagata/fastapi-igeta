"""
テーブル ``tr_sales_link_name`` の SQLAlchemy モデル。
"""
from __future__ import annotations

from sqlalchemy import SmallInteger, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TrSalesLinkName(Base):
    """販売商品名対照表"""

    __tablename__ = "tr_sales_link_name"

    sales_item_name: Mapped[str] = mapped_column(Text(), primary_key=True)
    item_no: Mapped[int] = mapped_column(SmallInteger())
