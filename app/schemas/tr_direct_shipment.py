"""tr_direct_shipment API スキーマ（ShipmentCorrect 相当）"""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class TrDirectShipmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    direct_shipment_no: int
    direct_shipment_name: str
    direct_shipment_kana: str | None = None
    zip: str | None = None
    address: str | None = None
    phone_no: str | None = None
    fax_no: str | None = None
    display_order: int | None = None
    remarks: str | None = None


class TrDirectShipmentUpsertPayload(BaseModel):
    direct_shipment_no: int
    direct_shipment_name: str
    direct_shipment_kana: str | None = None
    zip: str | None = None
    address: str | None = None
    phone_no: str | None = None
    fax_no: str | None = None
    display_order: int = 5
    remarks: str | None = None


class TrDirectShipmentUpsertResponse(BaseModel):
    ok: bool = True


class TrDirectShipmentDeletePayload(BaseModel):
    direct_shipment_no: int


class TrDirectShipmentDeleteResponse(BaseModel):
    ok: bool = True
