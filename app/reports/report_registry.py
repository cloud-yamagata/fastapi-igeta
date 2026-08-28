from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path

from app.reports.excel_export import ExcelExportOptions


EXCEL_TEMPLATE_SUFFIX_JA = "_雛形.xlsx"
EXCEL_TEMPLATE_SUFFIX = ".template.xlsx"


@dataclass(frozen=True)
class ReportAsset:
    report_id: str
    title: str
    sql_filename: str
    # None の場合は report_id ベースの既定規約で探索する
    excel_template_filename: str | None = None
    excel_export_options: ExcelExportOptions = ExcelExportOptions()


def project_root() -> Path:
    # .../fastapi-igeta/app/xxx.py -> parents[1] == .../fastapi-igeta
    return Path(__file__).resolve().parents[2]


def sql_dir() -> Path:
    return project_root() / "各種レポートSQL"


def excel_template_dir() -> Path:
    # 運用で置き場を変えたい場合に備えて環境変数で上書き可能にする
    # 例: EXCEL_TEMPLATE_DIR=D:\shared\Excelレポート雛形
    env = os.getenv("EXCEL_TEMPLATE_DIR")
    if env:
        return Path(env)
    return project_root() / "Excelレポート雛形"


REPORTS: dict[str, ReportAsset] = {
    # Menu screenKey: LotBulkTeaStockList
    "LotBulkTeaStockList": ReportAsset(
        report_id="LotBulkTeaStockList",
        title="ロット別仕上茶在庫一覧",
        sql_filename="ロット別仕上茶在庫一覧.sql",
        # 雛形は既定の命名規約（report_id + ".template.xlsx"）で探索する
        excel_template_filename=None,
        # タイトル等の固定領域を壊さないため、テンプレ側で開始セルをマークしてもらう運用にする
        excel_export_options=ExcelExportOptions(
            start_cell_marker="__DATA__",
            write_header=False,
            autosize_columns=False,
        ),
    ),
    # Menu screenKey: Factory2LotStockList
    "Factory2LotStockList": ReportAsset(
        report_id="Factory2LotStockList",
        title="第2工場ロット在庫一覧",
        sql_filename="第2工場ロット在庫一覧_v2.sql",
        excel_template_filename=None,
        excel_export_options=ExcelExportOptions(
            start_cell_marker="__DATA__",
            write_header=False,
            autosize_columns=False,
        ),
    ),
    # Menu screenKey: Factory2LotStockTransition
    "Factory2LotStockTransition": ReportAsset(
        report_id="Factory2LotStockTransition",
        title="第2工場ロット在庫推移表",
        sql_filename="第2工場ロット在庫推移表.sql",
        excel_template_filename=None,
        excel_export_options=ExcelExportOptions(
            start_cell_marker="__DATA__",
            write_header=False,
            autosize_columns=False,
        ),
    ),
    # Menu screenKey: Factory3BulkTeaTransition
    "Factory3BulkTeaTransition": ReportAsset(
        report_id="Factory3BulkTeaTransition",
        title="第3工場仕上茶移動推移表",
        sql_filename="第3工場仕上茶移動推移.sql",
        excel_template_filename=None,
        excel_export_options=ExcelExportOptions(
            start_cell_marker="__DATA__",
            write_header=False,
            autosize_columns=False,
        ),
    ),
    # Menu screenKey: UsuallLotUusedAadoptedList
    "UsuallLotUusedAadoptedList": ReportAsset(
        report_id="UsuallLotUusedAadoptedList",
        title="通常品ロット使用実績",
        sql_filename="通常品ロット使用実績.sql",
        excel_template_filename=None,
        excel_export_options=ExcelExportOptions(
            # 雛形に __DATA__ マーカーが無く、2行目に結合セルがあるため3行目から出力する
            start_row=3,
            write_header=False,
            autosize_columns=False,
        ),
    ),
    # Menu screenKey: BulkTeaYearOnYearUsage
    "BulkTeaYearOnYearUsage": ReportAsset(
        report_id="BulkTeaYearOnYearUsage",
        title="月別仕上茶前年対比使用量",
        sql_filename="月別仕上茶前年対比使用量.sql",
        excel_template_filename=None,
        excel_export_options=ExcelExportOptions(
            start_cell_marker="__DATA__",
            write_header=False,
            autosize_columns=False,
        ),
    ),
    # Menu screenKey: BulkTeaYearOnYearProduction
    "BulkTeaYearOnYearProduction": ReportAsset(
        report_id="BulkTeaYearOnYearProduction",
        title="月別仕上茶前年対比生産量",
        sql_filename="月別仕上茶前年対比生産量.sql",
        excel_template_filename=None,
        excel_export_options=ExcelExportOptions(
            start_cell_marker="__DATA__",
            write_header=False,
            autosize_columns=False,
        ),
    ),
    # Menu screenKey: MonthlySalesPlan
    "MonthlySalesPlan": ReportAsset(
        report_id="MonthlySalesPlan",
        title="月次販売計画実績一覧表",
        sql_filename="月次販売計画実績一覧表.sql",
        excel_template_filename=None,
        excel_export_options=ExcelExportOptions(
            start_row=2,
            write_header=False,
            autosize_columns=False,
        ),
    ),
}


def get_report(report_id: str) -> ReportAsset | None:
    return REPORTS.get(report_id)


def resolve_excel_template_path(asset: ReportAsset) -> Path | None:
    """
    雛形Excelの探索ルール（推奨: report_id.template.xlsx）
    - 明示指定があればそれを最優先
    - 次に report_id ベースの推奨規約
    - 最後に title + "_雛形.xlsx"（既存運用互換）
    """
    base = excel_template_dir()
    candidates: list[str] = []
    if asset.excel_template_filename:
        candidates.append(asset.excel_template_filename)
    candidates.append(f"{asset.report_id}{EXCEL_TEMPLATE_SUFFIX}")
    # 既存資産互換（日本語タイトル + ".template.xlsx"）
    candidates.append(f"{asset.title}{EXCEL_TEMPLATE_SUFFIX}")
    candidates.append(f"{asset.title}{EXCEL_TEMPLATE_SUFFIX_JA}")
    for name in candidates:
        p = (base / name).resolve()
        if p.exists():
            return p
    return None


def list_excel_template_candidates(asset: ReportAsset) -> list[str]:
    base = excel_template_dir()
    candidates: list[str] = []
    if asset.excel_template_filename:
        candidates.append(str((base / asset.excel_template_filename).resolve()))
    candidates.append(str((base / f"{asset.report_id}{EXCEL_TEMPLATE_SUFFIX}").resolve()))
    candidates.append(str((base / f"{asset.title}{EXCEL_TEMPLATE_SUFFIX}").resolve()))
    candidates.append(str((base / f"{asset.title}{EXCEL_TEMPLATE_SUFFIX_JA}").resolve()))
    return candidates

