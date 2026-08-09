"""
テーブル ``tr_item`` の SQLAlchemy モデル。

論理名・列コメントは DB辞書.tsv を参照。
"""
from __future__ import annotations

from sqlalchemy import Boolean, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TrItem(Base):
    """商品。

    DB辞書: table_comment = 商品
    """

    # table: tr_item | 商品
    __tablename__ = "tr_item"

    item_no: Mapped[int | None] = mapped_column(Integer, primary_key=True)  # item_no | 商品NO | PK | NOT NULL
    system_class: Mapped[str] = mapped_column(Text)  # system_class | システム区分 |  | NOT NULL
    organic_class: Mapped[str] = mapped_column(Text)  # organic_class | 有機区分 |  | NOT NULL
    item_group_no: Mapped[int] = mapped_column(Integer)  # item_group_no | 商品分類NO |  | NULL可（辞書上 nullable）
    item_name: Mapped[str] = mapped_column(Text)  # item_name | 商品名 |  | NOT NULL
    jan_code: Mapped[str] = mapped_column(Text)  # jan_code | JANコード |  | NULL可（辞書上 nullable）
    package_size: Mapped[int] = mapped_column(Integer)  # package_size | 梱包サイズ |  | NULL可（辞書上 nullable）
    display_order: Mapped[int] = mapped_column(Integer)  # display_order | 表示順 |  | NULL可（辞書上 nullable）
    display: Mapped[bool | None] = mapped_column(Boolean, nullable=True)  # display | 表示 |  | NULL可（実装: Boolean）
    remarks: Mapped[str | None] = mapped_column(Text, nullable=True)  # remarks | 備考 |  | NULL可
