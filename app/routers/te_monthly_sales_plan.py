"""te_monthly_sales_plan API（月次販売計画：年月単位の取得・登録・削除）。"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.deps import get_session
from app.entities.te_monthly_sales_plan.model import TeMonthlySalesPlan
from app.entities.te_monthly_sales_plan.repository import TeMonthlySalesPlanRepository
from app.schemas.te_monthly_sales_plan import (
    TeMonthlySalesPlanDeleteMonthPayload,
    TeMonthlySalesPlanDeleteMonthResponse,
    TeMonthlySalesPlanRead,
    TeMonthlySalesPlanUpsertMonthPayload,
    TeMonthlySalesPlanUpsertMonthResponse,
)

router = APIRouter(tags=["te_monthly_sales_plan"])


def _validate_year_month(year: int, month: int) -> None:
    if year < 2000 or year > 2100:
        raise HTTPException(status_code=400, detail="年が不正です")
    if month < 1 or month > 12:
        raise HTTPException(status_code=400, detail="月が不正です")


@router.get("/te_monthly_sales_plan/", response_model=list[TeMonthlySalesPlanRead])
@router.get("/te_monthly_sales_plan", response_model=list[TeMonthlySalesPlanRead])
def list_te_monthly_sales_plan(
    year: int = Query(...),
    month: int = Query(...),
    session: Session = Depends(get_session),
) -> list[TeMonthlySalesPlanRead]:
    _validate_year_month(year, month)
    rows = TeMonthlySalesPlanRepository.list_by_year_month(session, year, month)
    return [TeMonthlySalesPlanRead.model_validate(r) for r in rows]


@router.post("/te_monthly_sales_plan/upsert-month", response_model=TeMonthlySalesPlanUpsertMonthResponse)
def upsert_te_monthly_sales_plan_month(
    payload: TeMonthlySalesPlanUpsertMonthPayload,
    session: Session = Depends(get_session),
) -> TeMonthlySalesPlanUpsertMonthResponse:
    _validate_year_month(payload.year, payload.month)
    if not payload.items:
        raise HTTPException(status_code=400, detail="登録する明細がありません")
    rows = [
        TeMonthlySalesPlan(
            year=payload.year,
            month=payload.month,
            item_no=item.item_no,
            item_name=item.item_name,
            sales_size=item.sales_size,
            remarks=item.remarks,
        )
        for item in payload.items
    ]
    try:
        TeMonthlySalesPlanRepository.upsert_month(
            session, year=payload.year, month=payload.month, items=rows
        )
    except IntegrityError as exc:
        session.rollback()
        raise HTTPException(status_code=409, detail="月次販売計画の登録に失敗しました") from exc
    return TeMonthlySalesPlanUpsertMonthResponse(ok=True, count=len(rows))


@router.post("/te_monthly_sales_plan/delete-month", response_model=TeMonthlySalesPlanDeleteMonthResponse)
def delete_te_monthly_sales_plan_month(
    payload: TeMonthlySalesPlanDeleteMonthPayload,
    session: Session = Depends(get_session),
) -> TeMonthlySalesPlanDeleteMonthResponse:
    _validate_year_month(payload.year, payload.month)
    deleted = TeMonthlySalesPlanRepository.delete_by_year_month(session, payload.year, payload.month)
    if deleted == 0:
        raise HTTPException(status_code=404, detail="該当年月の月次販売計画はありません")
    return TeMonthlySalesPlanDeleteMonthResponse(ok=True, count=deleted)
