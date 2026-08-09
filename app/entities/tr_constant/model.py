"""
テーブル ``tr_constant`` の SQLAlchemy モデル。

論理名・列コメントは DB辞書.tsv を参照。
物理列 ``const`` は Python 属性 ``const_value`` にマッピング。
"""
from __future__ import annotations

from sqlalchemy import Boolean, SmallInteger, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TrConstant(Base):
    """システム定数。

    DB辞書: table_comment = システム定数
    複合主キー: (const_field, const)
    """

    # table: tr_constant | システム定数
    __tablename__ = "tr_constant"

    const_field: Mapped[str] = mapped_column(Text, primary_key=True)  # const_field | 定数項目 | PK(1) | NOT NULL
    const_value: Mapped[str] = mapped_column("const", Text, primary_key=True)  # const | 定数値 | PK(2)物理名 const | NOT NULL
    const_name: Mapped[str] = mapped_column("const_name", Text, nullable=False)  # const_name | 定数名 |  | NOT NULL
    display_order: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)  # display_order | #(論理名なし・DB辞書列コメント空) |  | NULL可
    display: Mapped[bool | None] = mapped_column(Boolean, nullable=True)  # display | 表示 |  | NULL可
