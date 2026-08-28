"""te_monthly_product_plan API（月別製造計画・Excel 取込）。"""
from __future__ import annotations

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.deps import get_session
from app.schemas.sales_plan_excel_import import (
    SalesPlanImportPreviewResponse,
    SalesPlanImportRegisterResponse,
)
from app.services.sales_plan_excel_import_service import (
    SalesPlanExcelImportError,
    build_preview,
    register_from_excel,
)

router = APIRouter(tags=["te_monthly_product_plan"])

_ALLOWED_SUFFIXES = (".xlsx", ".xlsm")


async def _read_upload(file: UploadFile) -> tuple[str, bytes]:
    name = (file.filename or "").strip()
    if not name:
        raise HTTPException(status_code=400, detail="ファイル名がありません")
    lower = name.lower()
    if not any(lower.endswith(suffix) for suffix in _ALLOWED_SUFFIXES):
        raise HTTPException(status_code=400, detail="Excel ファイル（.xlsx）を指定してください")
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="ファイルが空です")
    return name, content


@router.post(
    "/te_monthly_product_plan/import-excel/preview",
    response_model=SalesPlanImportPreviewResponse,
)
async def preview_sales_plan_excel_import(
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
) -> SalesPlanImportPreviewResponse:
    file_name, content = await _read_upload(file)
    try:
        return build_preview(session, file_name=file_name, content=content)
    except SalesPlanExcelImportError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post(
    "/te_monthly_product_plan/import-excel/register",
    response_model=SalesPlanImportRegisterResponse,
)
async def register_sales_plan_excel_import(
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
) -> SalesPlanImportRegisterResponse:
    file_name, content = await _read_upload(file)
    try:
        return register_from_excel(session, file_name=file_name, content=content)
    except SalesPlanExcelImportError as exc:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception:
        session.rollback()
        raise
