"""仕上品受入 API スキーマ（WPF PartsReceive 相当）。"""
from __future__ import annotations

from pydantic import BaseModel, Field


class PartsReceiveStockRow(BaseModel):
    product_date: str | None = None
    item_no: int
    product_no: int
    product_name: str | None = None
    make_year: str | None = None
    count: str | None = None
    product_quantity: float = 0
    factory2_stock: float = 0
    factory3_stock: float = 0


class PartsReceiveReceiveRequest(BaseModel):
    item_no: int
    product_no: int
    transfer_quantity: float = Field(..., gt=0)
    transfer_date: str = Field(..., description="移動日 yyyy-MM-dd")
    store_no: int = Field(..., description="受入先工場: 2=第2工場（返品）, 3=第3工場（受入）")


class PartsReceiveReceiveResponse(BaseModel):
    ok: bool = True
