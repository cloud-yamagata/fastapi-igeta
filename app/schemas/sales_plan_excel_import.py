"""販売計画 Excel 取込 API スキーマ。"""
from __future__ import annotations

from pydantic import BaseModel, Field


class SalesPlanImportSalesRow(BaseModel):
    sales_item_name: str
    item_no: int | None = None
    item_name: str = ""
    sales_size: int = 0
    status: str
    message: str = ""


class SalesPlanImportProductRow(BaseModel):
    sales_item_name: str
    column: str
    qty: int
    item_no: int | None = None
    bulk_no: int | None = None
    item_name: str = ""
    package_size: int = 0
    need_size: int = 0
    status: str
    message: str = ""


class SalesPlanImportErrorEntry(BaseModel):
    """取込プレビュー時のエラー1件（対象コード付き）。"""

    error_code: str
    sales_item_name: str
    item_no: int | None = None
    excel_column: str | None = None
    qty: int | None = None
    target_table: str = ""
    target_key: str = ""
    message: str


class SalesPlanImportSummary(BaseModel):
    total_sales_rows: int = 0
    ok_sales_rows: int = 0
    total_product_rows: int = 0
    ok_product_rows: int = 0
    link_not_found: int = 0
    bom_not_found: int = 0
    bom_missing_items: list[str] = Field(default_factory=list)
    merged_sales_rows: int = 0
    duplicate_item_nos: list[str] = Field(default_factory=list)
    can_register: bool = False


class SalesPlanImportPreviewResponse(BaseModel):
    year: int
    month: int
    file_name: str
    sales_rows: list[SalesPlanImportSalesRow] = Field(default_factory=list)
    product_rows: list[SalesPlanImportProductRow] = Field(default_factory=list)
    errors: list[SalesPlanImportErrorEntry] = Field(default_factory=list)
    summary: SalesPlanImportSummary


class SalesPlanImportRegisterResponse(BaseModel):
    ok: bool
    year: int
    month: int
    sales_count: int
    product_count: int
