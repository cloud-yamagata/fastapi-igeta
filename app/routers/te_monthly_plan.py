"""te_monthly_plan API"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_session
from app.entities.te_monthly_plan.model import TeMonthlyPlan
from app.entities.te_monthly_plan.repository import TeMonthlyPlanRepository
from app.schemas.te_monthly_plan import (
    MonthlyPlanDeleteRequest,
    MonthlyPlanDeleteResponse,
    MonthlyPlanUpsertPayload,
    TeMonthlyPlanRead,
)

router = APIRouter(tags=["te_monthly_plan"])


def apply_monthly_plan_payload(row: TeMonthlyPlan, payload: MonthlyPlanUpsertPayload) -> TeMonthlyPlan:
    row.year = payload.year
    row.month = payload.month
    row.process_type = payload.process_type
    row.lot_name = payload.lot_name
    row.work_date = payload.work_date
    row.work_time = payload.work_time
    row.unit_weight = payload.unit_weight if payload.unit_weight is not None else 0
    row.item_no = payload.item_no
    row.remarks = payload.remarks
    row.lot_part_info = payload.lot_part_info if payload.lot_part_info is not None else []
    return row


@router.get("/te_monthly_plan", response_model=list[TeMonthlyPlanRead])
@router.get("/te_monthly_plan/", response_model=list[TeMonthlyPlanRead])
def read_te_monthly_plan(session: Session = Depends(get_session)) -> list[TeMonthlyPlanRead]:
    rows = TeMonthlyPlanRepository.list_all(session)
    return [TeMonthlyPlanRead.model_validate(r) for r in rows]


@router.post("/te_monthly_plan/delete", response_model=MonthlyPlanDeleteResponse)
def delete_te_monthly_plan(
    payload: MonthlyPlanDeleteRequest,
    session: Session = Depends(get_session),
) -> MonthlyPlanDeleteResponse:
    plan_no_list: list[int] = []
    for target in payload.plans:
        if target.plan_no is not None and isinstance(target.plan_no, int):
            plan_no_list.append(target.plan_no)

    deleted_count = TeMonthlyPlanRepository.delete_by_plan_nos(session, plan_no_list)
    return MonthlyPlanDeleteResponse(deleted_count=deleted_count)


@router.post("/te_monthly_plan/create", response_model=TeMonthlyPlanRead)
def create_te_monthly_plan(
    payload: MonthlyPlanUpsertPayload,
    session: Session = Depends(get_session),
) -> TeMonthlyPlanRead:
    row = TeMonthlyPlan(
        plan_no=payload.plan_no,
        year=payload.year,
        month=payload.month,
        process_type=payload.process_type,
        lot_name=payload.lot_name,
        work_date=payload.work_date,
        work_time=payload.work_time,
        unit_weight=0,
        item_no=payload.item_no,
        remarks=payload.remarks,
        lot_part_info=[],
    )
    row = apply_monthly_plan_payload(row, payload)
    saved = TeMonthlyPlanRepository.persist(session, row)
    return TeMonthlyPlanRead.model_validate(saved)


@router.post("/te_monthly_plan/update", response_model=TeMonthlyPlanRead)
def update_te_monthly_plan(
    payload: MonthlyPlanUpsertPayload,
    session: Session = Depends(get_session),
) -> TeMonthlyPlanRead:
    if payload.plan_no is None:
        raise HTTPException(status_code=400, detail="planNo is required")

    row = TeMonthlyPlanRepository.get_by_plan_no(session, payload.plan_no)
    if row is None:
        raise HTTPException(status_code=404, detail="Monthly plan not found")

    row = apply_monthly_plan_payload(row, payload)
    saved = TeMonthlyPlanRepository.persist(session, row)
    return TeMonthlyPlanRead.model_validate(saved)
