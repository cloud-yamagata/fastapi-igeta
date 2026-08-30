"""FastAPI エントリ。ルーターは機能別モジュールに分割。"""
from __future__ import annotations

from contextlib import asynccontextmanager

import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.logging_config import configure_logging
from app.middleware.request_logging import RequestLoggingMiddleware

# ルーター登録: import 行または app.include_router(...) の1行をコメントアウトすると、その API だけ無効化できます。
# 先頭に # が無い import が有効。フロントの起動時一括マスタ取得対象はこれら（users / items のサンプルは除く）に合わせること。
from app.routers import blend_no  # 仕上茶番号
from app.routers import bulk_no  # 荒茶番号
from app.routers import finish_no  # 仕上番号
from app.routers import factory2_lot_manufacture  # 第二工場ロット製造登録（変更・削除）
from app.routers import package_lot_manufacture  # パッケージ製造報告書登録（登録・変更・削除）
from app.routers import firepan_no  # 火入番号
from app.routers import te_blend_lot  # ブレンドロット情報
# from app.routers import te_blend_lot_base  # ブレンドロット基本情報
# from app.routers import te_blend_lot_part  # ブレンドロット部品情報
# from app.routers import te_consign_product  # 外部委託実績情報
from app.routers import te_factory1_result  # 第1工場生産実績
from app.routers import te_factory1_transfer  # 第1工場移動実績
from app.routers import te_factory2_result  # 第2工場作業実績
from app.routers import vi_factory2_stock  # 第二工場ロット在庫（ビュー）
from app.routers import vi_factory3_stoc  # 第3工場仕上茶在庫（ビュー）
from app.routers import te_factory3_result  # 第3工場作業実績
from app.routers import te_factory3_stock  # 第3工場受入実績
from app.routers import te_grade  # ロット格付NO対象表
from app.routers import te_lot  # ロット情報
from app.routers import te_lot_base  # ロット基本情報
# from app.routers import te_lot_bom  # 使用部品
from app.routers import te_lot_categorys_blend  # 配合個別情報
from app.routers import te_lot_categorys_common  # 共通情報
from app.routers import te_lot_categorys_finish  # 仕上個別情報
from app.routers import te_lot_categorys_firepan  # 火入個別情報
from app.routers import te_lot_divide  # ロット分割
from app.routers import te_lot_part  # 使用部品
from app.routers import te_lot_use_item  # 仕上げ茶ロット対象表
from app.routers import te_material  # 原料情報
from app.routers import te_material_purchase  # 仕上品仕入情報
from app.routers import material_purchase  # 仕上品仕入登録（複合登録）
from app.routers import te_material_result  # 原料実績情報
from app.routers import te_monthly_plan  # 月別製造計画情報
from app.routers import te_monthly_product_plan  # 月別製造計画（Excel取込）
from app.routers import te_monthly_sales_plan  # 月別販売計画
from app.routers import te_package_base  # パッケージ基本情報
from app.routers import te_package_base_new  # パッケージ基本情報（新）
from app.routers import te_package_categorys_new  # パッケージ個別情報（新）
from app.routers import te_purchase_receive  # 仕入受入実績
from app.routers import te_purchase_tea  # 仕入実績
from app.routers import te_purchase_transfer  # 仕入移動実績
from app.routers import te_store_transfer  # 入出庫実績
from app.routers import te_store_transfer_fa2  # 入出庫実績
from app.routers import tr_constant  # システム定数
from app.routers import tr_customer  # 得意先
from app.routers import tr_direct_shipment  # 直送先
from app.routers import tr_item  # 商品
from app.routers import tr_item_bom  # 商品原料対照表
from app.routers import tr_item_group  # 商品分類
from app.routers import tr_purchase  # 仕入先
# from app.routers import tr_report  # レポート管理マスタ
# from app.routers import tr_report_item  # レポート項目マスタ
from app.routers import tr_resale  # 転売先
from app.routers import tr_sales_plan_item  # 販売計画商品マスタ
from app.routers import tr_store  # 倉庫
from app.routers import tr_supplier  # 委託先
from app.routers import users  # サンプルCRUD
from app.routers import items  # サンプルCRUD
from app.routers import reports  # 各種レポート（SQL実行/Excel）
from app.reports.report_registry import excel_template_dir


load_dotenv()
configure_logging()
logger = logging.getLogger(__name__)


def _cors_allow_origins() -> list[str]:
    """ブラウザ実効オリジン（localhost / 127.0.0.1 / ::1、Vite 既定・preview 用）＋ CORS_ORIGINS 追記。"""
    base = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://[::1]:5173",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
        "http://[::1]:4173",
    ]
    extra = os.getenv("CORS_ORIGINS", "").strip()
    if not extra:
        return base
    for part in extra.split(","):
        p = part.strip()
        if p and p not in base:
            base.append(p)
    return base


# 上記リストに無いポートの Vite 等は正規表現で許可（例: http://localhost:5174）
_CORS_ORIGIN_REGEX = os.getenv(
    "CORS_ORIGIN_REGEX",
    r"^https?://(localhost|127\.0\.0\.1|\[::1\])(:\d+)?$",
).strip()

# CORS_MODE=strict … 明示オリジン＋ credentials（本番向け）
# それ以外（既定）… allow_origins=["*"]（フロントは fetch 既定でクッキーを送らない想定。開発で CORS 不一致を避ける）
_CORS_MODE = os.getenv("CORS_MODE", "").strip().lower()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("startup")
    yield
    logger.info("shutdown")


app = FastAPI(lifespan=lifespan)

app.add_middleware(RequestLoggingMiddleware)
if _CORS_MODE == "strict":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=_cors_allow_origins(),
        allow_origin_regex=_CORS_ORIGIN_REGEX or None,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

logger.info(
    "CORS: mode=%s (set CORS_MODE=strict for explicit origins + credentials)",
    "strict" if _CORS_MODE == "strict" else "wildcard",
)

# import と同じ有効／無効（コメントアウト）に揃えること。
app.include_router(blend_no.router)  # 仕上茶番号
app.include_router(bulk_no.router)  # 荒茶番号
app.include_router(finish_no.router)  # 仕上番号
app.include_router(firepan_no.router)  # 火入番号
app.include_router(te_blend_lot.router)  # ブレンドロット情報
# app.include_router(te_blend_lot_base.router)  # ブレンドロット基本情報
# app.include_router(te_blend_lot_part.router)  # ブレンドロット部品情報
# app.include_router(te_consign_product.router)  # 外部委託実績情報
app.include_router(te_factory1_result.router)  # 第1工場生産実績
app.include_router(te_factory1_transfer.router)  # 第1工場移動実績
app.include_router(te_factory2_result.router)  # 第2工場作業実績
app.include_router(factory2_lot_manufacture.router)  # 第二工場ロット製造登録（変更・削除）
app.include_router(package_lot_manufacture.router)  # パッケージ製造報告書登録（登録・変更・削除）
app.include_router(vi_factory2_stock.router)  # 第二工場ロット在庫（ビュー・在庫>0）
app.include_router(vi_factory3_stoc.router)  # 第3工場仕上茶在庫（ビュー）
app.include_router(te_factory3_result.router)  # 第3工場作業実績
app.include_router(te_factory3_stock.router)  # 第3工場受入実績
app.include_router(te_grade.router)  # ロット格付NO対象表
app.include_router(te_lot.router)  # ロット情報
app.include_router(te_lot_base.router)  # ロット基本情報
# app.include_router(te_lot_bom.router)  # 使用部品
app.include_router(te_lot_categorys_blend.router)  # 配合個別情報
app.include_router(te_lot_categorys_common.router)  # 共通情報
app.include_router(te_lot_categorys_finish.router)  # 仕上個別情報
app.include_router(te_lot_categorys_firepan.router)  # 火入個別情報
app.include_router(te_lot_divide.router)  # ロット分割
app.include_router(te_lot_part.router)  # 使用部品
app.include_router(te_lot_use_item.router)  # 仕上げ茶ロット対象表
app.include_router(te_material.router)  # 原料情報
app.include_router(te_material_purchase.router)  # 仕上品仕入情報
app.include_router(material_purchase.router)  # 仕上品仕入登録（複合登録）
app.include_router(te_material_result.router)  # 原料実績情報
app.include_router(te_monthly_plan.router)  # 月別製造計画情報
app.include_router(te_monthly_product_plan.router)  # 月別製造計画（Excel取込）
app.include_router(te_monthly_sales_plan.router)  # 月別販売計画
app.include_router(te_package_base.router)  # パッケージ基本情報
app.include_router(te_package_base_new.router)  # パッケージ基本情報（新）
app.include_router(te_package_categorys_new.router)  # パッケージ個別情報（新）
app.include_router(te_purchase_receive.router)  # 仕入受入実績
app.include_router(te_purchase_tea.router)  # 仕入実績
app.include_router(te_purchase_transfer.router)  # 仕入移動実績
app.include_router(te_store_transfer.router)  # 入出庫実績
app.include_router(te_store_transfer_fa2.router)  # 入出庫実績
app.include_router(tr_constant.router)  # システム定数
app.include_router(tr_customer.router)  # 得意先
app.include_router(tr_direct_shipment.router)  # 直送先
app.include_router(tr_item.router)  # 商品
app.include_router(tr_item_bom.router)  # 商品原料対照表
app.include_router(tr_item_group.router)  # 商品分類
app.include_router(tr_purchase.router)  # 仕入先
# app.include_router(tr_report.router)  # レポート管理マスタ
# app.include_router(tr_report_item.router)  # レポート項目マスタ
app.include_router(tr_resale.router)  # 転売先
app.include_router(tr_sales_plan_item.router)  # 販売計画商品マスタ
app.include_router(tr_store.router)  # 倉庫
app.include_router(tr_supplier.router)  # 委託先
app.include_router(users.router)  # サンプルCRUD
app.include_router(items.router)  # サンプルCRUD
app.include_router(reports.router)  # 各種レポート（SQL実行/Excel）

# Excel 雛形（フロントの振分一覧 Excel 出力などが GET で取得）
_excel_template_dir = excel_template_dir()
if _excel_template_dir.is_dir():
    from fastapi.staticfiles import StaticFiles

    app.mount(
        "/excel-templates",
        StaticFiles(directory=str(_excel_template_dir)),
        name="excel-templates",
    )
    logger.info("Excel templates mounted at /excel-templates -> %s", _excel_template_dir)
else:
    logger.warning("Excel template directory not found: %s", _excel_template_dir)
