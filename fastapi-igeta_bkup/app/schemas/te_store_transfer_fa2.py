"""te_store_transfer_fa2 API スキーマ（StoreTransferFa2 登録・変更相当）"""
from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, field_validator


def _parse_optional_datetime(v: object) -> object:
    if v is None or v == "":
        return None
    if isinstance(v, datetime):
        return v
    if isinstance(v, str):
        s = v.strip()
        if not s:
            return None
        if len(s) >= 10 and s[4] == "-" and s[7] == "-":
            try:
                return datetime.fromisoformat(s[:19].replace("Z", ""))
            except ValueError:
                return datetime.strptime(s[:10], "%Y-%m-%d")
    return v


class TeStoreTransferFa2CreatePayload(BaseModel):
    """登録時（WPF 入出庫情報登録）。transfer_no は DB 採番。"""

    transfer_date: datetime
    lot_no: int
    process_type: str
    product_no: int
    lot_name: str | None = None
    transfer_type: str
    result_type: str
    lot_type: str
    reason: str | None = None
    unit_weight: Decimal | None = None
    unit_number: int | None = None
    fraction_weight: Decimal | None = None
    fraction_number: int | None = None
    transfer_quantity: Decimal
    unit_type: str | None = None
    remarks: str | None = None

    @field_validator("transfer_date", mode="before")
    @classmethod
    def _parse_transfer_date(cls, v: object) -> object:
        parsed = _parse_optional_datetime(v)
        if parsed is None:
            raise ValueError("transfer_date is required")
        return parsed


class TeStoreTransferFa2CreateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    ok: bool = True
    transfer_no: int | None = None


class TeStoreTransferFa2UpdatePayload(BaseModel):
    """変更時更新カラム（WPF 入出庫情報更新 + 編集画面の編集項目）"""

    transfer_no: int
    transfer_date: datetime | None = None
    reason: str | None = None
    unit_weight: Decimal | None = None
    unit_number: int | None = None
    fraction_weight: Decimal | None = None
    fraction_number: int | None = None
    transfer_quantity: Decimal
    remarks: str | None = None

    @field_validator("transfer_date", mode="before")
    @classmethod
    def _parse_transfer_date(cls, v: object) -> object:
        return _parse_optional_datetime(v)


class TeStoreTransferFa2UpdateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    ok: bool = True
