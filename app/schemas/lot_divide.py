"""ロット分割（WPF LotDivide MaterialRegist）API スキーマ。"""
from __future__ import annotations

from pydantic import BaseModel, Field


class LotDivideMaterialRegistRequest(BaseModel):
    lot_no: int
    process_type: str = Field(..., min_length=1, max_length=2)
    product_no: int
    lot_name: str | None = None
    item_no: int = 0
    item_name: str | None = None
    organic_class: str = ""
    make_year: str | None = None
    count: str | None = None
    factory2_stock: float = Field(..., gt=0)
    divide_type: str = Field(..., pattern="^[12]$", description="1=再投入, 2=転売")
    divide_date: str = Field(..., description="分割日 yyyy-MM-dd")
    divide_quantity: float = Field(..., gt=0)
    divide_lot_name: str = Field(..., min_length=1)
    reason: str | None = None
    remarks: str | None = None


class LotDivideMaterialRegistResponse(BaseModel):
    ok: bool = True
    serial_no: int
    message: str
