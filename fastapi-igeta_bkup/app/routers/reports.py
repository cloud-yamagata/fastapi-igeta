from __future__ import annotations

from pathlib import Path
from typing import Any
from urllib.parse import quote

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.deps import get_session
from app.reports.excel_export import export_to_excel_using_template
from app.reports.report_registry import get_report, list_excel_template_candidates, resolve_excel_template_path, sql_dir
from app.reports.sql_runner import load_sql, run_sql_report


router = APIRouter(tags=["reports"])

def content_disposition_with_utf8_filename(filename_utf8: str, *, fallback_ascii: str) -> str:
    """
    Starlette/ASGI のヘッダは latin-1 制約があるため、
    RFC 5987 の filename* を併用して日本語ファイル名を安全に返す。
    """
    encoded = quote(filename_utf8, safe="")
    return f'attachment; filename="{fallback_ascii}"; filename*=UTF-8\'\'{encoded}'


class ReportRunRequest(BaseModel):
    params: dict[str, Any] = {}


@router.post("/reports/{report_id}/run")
def run_report(report_id: str, body: ReportRunRequest, session: Session = Depends(get_session)) -> dict[str, Any]:
    asset = get_report(report_id)
    if asset is None:
        raise HTTPException(status_code=404, detail="report not found")

    sql_path = (sql_dir() / asset.sql_filename).resolve()
    if not sql_path.exists():
        raise HTTPException(status_code=500, detail=f"sql not found: {asset.sql_filename}")

    sql = load_sql(sql_path)
    rows = run_sql_report(session, sql=sql, params=body.params)
    return {"reportId": asset.report_id, "title": asset.title, "rows": rows}


@router.post("/reports/{report_id}/excel")
def export_report_excel(report_id: str, body: ReportRunRequest, session: Session = Depends(get_session)) -> Response:
    asset = get_report(report_id)
    if asset is None:
        raise HTTPException(status_code=404, detail="report not found")

    sql_path = (sql_dir() / asset.sql_filename).resolve()
    if not sql_path.exists():
        raise HTTPException(status_code=500, detail=f"sql not found: {asset.sql_filename}")

    template_path = resolve_excel_template_path(asset)
    if template_path is None:
        raise HTTPException(
            status_code=500,
            detail={"message": "excel template not found", "candidates": list_excel_template_candidates(asset)},
        )

    sql = load_sql(sql_path)
    rows = run_sql_report(session, sql=sql, params=body.params)
    xlsx = export_to_excel_using_template(
        template_bytes=template_path.read_bytes(),
        rows=rows,
        options=asset.excel_export_options,
    )

    filename = f"{asset.title}.xlsx"
    fallback = f"{asset.report_id}.xlsx"
    return Response(
        content=xlsx,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": content_disposition_with_utf8_filename(filename, fallback_ascii=fallback)},
    )

