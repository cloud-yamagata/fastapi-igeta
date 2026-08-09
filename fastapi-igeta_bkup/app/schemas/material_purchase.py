"""仕上品仕入登録 API スキーマ（WPF MaterialPurchase StockRepository.Regist 相当）。"""
from __future__ import annotations

from pydantic import BaseModel, Field


class MaterialPurchaseCreateRequest(BaseModel):
    purchase_date: str = Field(..., description="仕入日 yyyy-MM-dd")
    item_no: int
    item_name: str
    purchase_lot_no: str
    purchase_quantity: float
    supplier: str
    # 以下はフロントからも送られるが、サーバ側で固定値を優先してもよい
    transfer_type: str | None = None
    result_type: str | None = None
    lot_type: str | None = None
    reason: str | None = None
    store_no: int | None = None
    unit_type: str | None = None
    process_type: str | None = None
    process_name: str | None = None


class MaterialPurchaseCreateResponse(BaseModel):
    ok: bool = True
    purchase_no: int
    transfer_no: int | None = None
    lot_no: int | None = None


class MaterialPurchaseUpdateRequest(BaseModel):
    purchase_no: int
    purchase_date: str = Field(..., description="仕入日 yyyy-MM-dd")
    item_no: int
    item_name: str
    purchase_lot_no: str
    purchase_quantity: float
    supplier: str


class MaterialPurchaseUpdateResponse(BaseModel):
    ok: bool = True
    purchase_no: int
