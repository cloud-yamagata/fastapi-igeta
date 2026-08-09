"""
テーブル ``te_lot_categorys_finish`` の SQLAlchemy モデル（DB辞書.tsv 自動生成）。
"""
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import Boolean, DateTime, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TeLotCategorysFinish(Base):
    """仕上個別情報"""

    # table: te_lot_categorys_finish | 仕上個別情報
    __tablename__ = "te_lot_categorys_finish"

    lot_no: Mapped[int] = mapped_column(Integer(), primary_key=True)  # lot_no | ロットNO | PK | NOT NULL
    sp1_use_chk: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)  # sp1_use_chk | SP-1使用チェック |  | NULL可
    sp1_value_1: Mapped[str | None] = mapped_column(Text(), nullable=True)  # sp1_value_1 | SP-1投入量 |  | NULL可
    sp1_value_2a: Mapped[str | None] = mapped_column(Text(), nullable=True)  # sp1_value_2a | SP-1回転篩網_元 |  | NULL可
    sp1_value_2b: Mapped[str | None] = mapped_column(Text(), nullable=True)  # sp1_value_2b | SP-1回転篩網_中 |  | NULL可
    sp1_value_2c: Mapped[str | None] = mapped_column(Text(), nullable=True)  # sp1_value_2c | SP-1回転篩網_先 |  | NULL可
    sp1_value_3a: Mapped[str | None] = mapped_column(Text(), nullable=True)  # sp1_value_3a | SP-1廻し篩網目_上 |  | NULL可
    sp1_value_3b: Mapped[str | None] = mapped_column(Text(), nullable=True)  # sp1_value_3b | SP-1廻し篩網目_下 |  | NULL可
    sp1_value_4: Mapped[str | None] = mapped_column(Text(), nullable=True)  # sp1_value_4 | SP-1唐箕 |  | NULL可
    sp1_value_5: Mapped[str | None] = mapped_column(Text(), nullable=True)  # sp1_value_5 | SP-1電棒電圧 |  | NULL可
    sp1_value_6a: Mapped[str | None] = mapped_column(Text(), nullable=True)  # sp1_value_6a | SP-1角葉抜き_振動 |  | NULL可
    sp1_value_6b: Mapped[str | None] = mapped_column(Text(), nullable=True)  # sp1_value_6b | SP-1角葉抜き_網 |  | NULL可
    sp2_use_chk: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)  # sp2_use_chk | SP-2使用チェック |  | NULL可
    sp2_value_1: Mapped[str | None] = mapped_column(Text(), nullable=True)  # sp2_value_1 | SP-2投入量 |  | NULL可
    sp2_value_2a: Mapped[str | None] = mapped_column(Text(), nullable=True)  # sp2_value_2a | SP-2抜き網_抜き振動 |  | NULL可
    sp2_value_2b: Mapped[str | None] = mapped_column(Text(), nullable=True)  # sp2_value_2b | SP-2抜き網_先網目 |  | NULL可
    sp2_value_2c: Mapped[str | None] = mapped_column(Text(), nullable=True)  # sp2_value_2c | SP-2抜き網_中網目 |  | NULL可
    sp2_value_2d: Mapped[str | None] = mapped_column(Text(), nullable=True)  # sp2_value_2d | SP-2抜き網_元網目 |  | NULL可
    sp2_value_3a: Mapped[str | None] = mapped_column(Text(), nullable=True)  # sp2_value_3a | SP-2廻し篩網目_上 |  | NULL可
    sp2_value_3b: Mapped[str | None] = mapped_column(Text(), nullable=True)  # sp2_value_3b | SP-2廻し篩網目_下 |  | NULL可
    sp2_value_4a: Mapped[str | None] = mapped_column(Text(), nullable=True)  # sp2_value_4a | SP-2唐箕_本茶 |  | NULL可
    sp2_value_4b: Mapped[str | None] = mapped_column(Text(), nullable=True)  # sp2_value_4b | SP-2唐箕_芽 |  | NULL可
    sp2_value_5: Mapped[str | None] = mapped_column(Text(), nullable=True)  # sp2_value_5 | SP-2電棒電圧 |  | NULL可
    etc_value_1a: Mapped[str | None] = mapped_column(Text(), nullable=True)  # etc_value_1a | 乾燥機_温度 |  | NULL可
    etc_value_1b: Mapped[str | None] = mapped_column(Text(), nullable=True)  # etc_value_1b | 乾燥機_投入厚 |  | NULL可
    etc_value_1c: Mapped[str | None] = mapped_column(Text(), nullable=True)  # etc_value_1c | 乾燥機_速度 |  | NULL可
    etc_value_2a: Mapped[str | None] = mapped_column(Text(), nullable=True)  # etc_value_2a | 色彩選別機調整_上 |  | NULL可
    etc_value_2b: Mapped[str | None] = mapped_column(Text(), nullable=True)  # etc_value_2b | 色彩選別機調整_下 |  | NULL可
    etc_value_2c: Mapped[str | None] = mapped_column(Text(), nullable=True)  # etc_value_2c | 色彩選別機調整_投入量1 |  | NULL可
    etc_value_2d: Mapped[str | None] = mapped_column(Text(), nullable=True)  # etc_value_2d | 色彩選別機調整_投入量2 |  | NULL可
    etc_use_chk3a: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)  # etc_use_chk3a | HA300使用チェック |  | NULL可
    etc_use_chk3b: Mapped[bool | None] = mapped_column(Boolean(), nullable=True)  # etc_use_chk3b | 横山式使用チェック |  | NULL可
    etc_value_3: Mapped[str | None] = mapped_column(Text(), nullable=True)  # etc_value_3 | 切断網目 |  | NULL可
    pickup1_name: Mapped[str | None] = mapped_column(Text(), nullable=True)  # pickup1_name | 出物棒 |  | NULL可
    pickup1_weight: Mapped[str | None] = mapped_column(Text(), nullable=True)  # pickup1_weight | 出物棒Kg |  | NULL可
    pickup1_number: Mapped[str | None] = mapped_column(Text(), nullable=True)  # pickup1_number | 出物棒個数 |  | NULL可
    pickup1_fraction: Mapped[str | None] = mapped_column(Text(), nullable=True)  # pickup1_fraction | 出物棒端数 |  | NULL可
    pickup2_name: Mapped[str | None] = mapped_column(Text(), nullable=True)  # pickup2_name | 出物唐箕先 |  | NULL可
    pickup2_weight: Mapped[str | None] = mapped_column(Text(), nullable=True)  # pickup2_weight | 出物唐箕先Kg |  | NULL可
    pickup2_number: Mapped[str | None] = mapped_column(Text(), nullable=True)  # pickup2_number | 出物唐箕先個数 |  | NULL可
    pickup2_fraction: Mapped[str | None] = mapped_column(Text(), nullable=True)  # pickup2_fraction | 出物唐箕先端数 |  | NULL可
    pickup3_name: Mapped[str | None] = mapped_column(Text(), nullable=True)  # pickup3_name | 出物頭 |  | NULL可
    pickup3_weight: Mapped[str | None] = mapped_column(Text(), nullable=True)  # pickup3_weight | 出物頭Kg |  | NULL可
    pickup3_number: Mapped[str | None] = mapped_column(Text(), nullable=True)  # pickup3_number | 出物頭個数 |  | NULL可
    pickup3_fraction: Mapped[str | None] = mapped_column(Text(), nullable=True)  # pickup3_fraction | 出物頭端数 |  | NULL可
    pickup4_name: Mapped[str | None] = mapped_column(Text(), nullable=True)  # pickup4_name | 出物粉 |  | NULL可
    pickup4_weight: Mapped[str | None] = mapped_column(Text(), nullable=True)  # pickup4_weight | 出物粉Kg |  | NULL可
    pickup4_number: Mapped[str | None] = mapped_column(Text(), nullable=True)  # pickup4_number | 出物粉個数数 |  | NULL可
    pickup4_fraction: Mapped[str | None] = mapped_column(Text(), nullable=True)  # pickup4_fraction | 出物粉端数 |  | NULL可
    remarks: Mapped[str | None] = mapped_column(Text(), nullable=True)  # remarks | 摘要 |  | NULL可
    update_time: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=False), nullable=True)  # update_time | #(論理名なし・DB辞書列コメント空) |  | NULL可

