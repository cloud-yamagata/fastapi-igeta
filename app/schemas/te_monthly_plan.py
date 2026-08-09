"""te_monthly_plan API スキーマ"""
from __future__ import annotations

import datetime
from typing import Any

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class TeMonthlyPlanRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    plan_no: int | None
    year: int
    month: int
    process_type: str
    lot_name: str
    work_date: datetime.date
    work_time: datetime.time | None
    unit_weight: int
    item_no: int | None
    remarks: str | None
    lot_part_info: object | None


class MonthlyPlanUpsertPayload(BaseModel):
    """フロントからの JSON は camelCase（planNo, processType 等）を許容"""

    model_config = ConfigDict(populate_by_name=True)

    plan_no: int | None = Field(None, validation_alias=AliasChoices("planNo", "plan_no"))
    year: int
    month: int
    process_type: str = Field(validation_alias=AliasChoices("processType", "process_type"))
    lot_name: str = Field(validation_alias=AliasChoices("lotName", "lot_name"))
    work_date: datetime.date = Field(validation_alias=AliasChoices("workDate", "work_date"))
    work_time: datetime.time | None = Field(None, validation_alias=AliasChoices("workTime", "work_time"))
    unit_weight: int | None = Field(None, validation_alias=AliasChoices("unitWeight", "unit_weight"))
    item_no: int | None = Field(None, validation_alias=AliasChoices("itemNo", "item_no"))
    remarks: str | None = None
    lot_part_info: Any | None = Field(None, validation_alias=AliasChoices("lotPartInfo", "lot_part_info"))


class MonthlyPlanDeleteRow(BaseModel):
    """削除リクエストはフロントから TeMonthlyPlan 行オブジェクトごと渡る想定で planNo のみ参照"""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    plan_no: int | None = Field(None, validation_alias=AliasChoices("planNo", "plan_no"))


class MonthlyPlanDeleteRequest(BaseModel):
    plans: list[MonthlyPlanDeleteRow] = Field(default_factory=list)


class MonthlyPlanDeleteResponse(BaseModel):
    deleted_count: int
