"""te_purchase_transfer upsert リクエスト"""
from __future__ import annotations

import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class TePurchaseTransferUpsertPayload(BaseModel):
    year: int
    purchase: str
    bid_no: str = Field(alias="bid_no")
    result_type: str = Field(alias="result_type")
    transfer: str
    transfer_date: datetime.date = Field(alias="transfer_date")
    unit_weight: Decimal = Field(alias="unit_weight")
    unit_number: int = Field(alias="unit_number")
    fraction_weight: Decimal = Field(alias="fraction_weight")
    fraction_number: int = Field(alias="fraction_number")
    unit_price: Decimal | None = Field(default=None, alias="unit_price")
    remarks: str | None = None

    model_config = {"populate_by_name": True}


class TePurchaseTransferUpsertResponse(BaseModel):
    ok: bool = True
