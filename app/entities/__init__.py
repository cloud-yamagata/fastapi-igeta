"""ORM 全テーブル集約（DB辞書と対応）。Alembic / メタデータ用。"""
from __future__ import annotations

from app.entities.blend_no.model import BlendNo
from app.entities.bulk_no.model import BulkNo
from app.entities.finish_no.model import FinishNo
from app.entities.firepan_no.model import FirepanNo
from app.entities.te_blend_lot_base.model import TeBlendLotBase
from app.entities.te_blend_lot_part.model import TeBlendLotPart
from app.entities.te_consign_product.model import TeConsignProduct
from app.entities.te_factory1_result.model import TeFactory1Result
from app.entities.te_factory1_transfer.model import TeFactory1Transfer
from app.entities.te_factory2_result.model import TeFactory2Result
from app.entities.te_factory3_result.model import TeFactory3Result
from app.entities.te_factory3_stock.model import TeFactory3Stock
from app.entities.te_grade.model import TeGrade
from app.entities.te_lot.model import TeLot
from app.entities.te_lot_base.model import TeLotBase
from app.entities.te_lot_bom.model import TeLotBom
from app.entities.te_lot_categorys_blend.model import TeLotCategorysBlend
from app.entities.te_lot_categorys_common.model import TeLotCategorysCommon
from app.entities.te_lot_categorys_finish.model import TeLotCategorysFinish
from app.entities.te_lot_categorys_firepan.model import TeLotCategorysFirepan
from app.entities.te_lot_divide.model import TeLotDivide
from app.entities.te_lot_part.model import TeLotPart
from app.entities.te_lot_use_item.model import TeLotUseItem
from app.entities.te_material.model import TeMaterial
from app.entities.te_material_purchase.model import TeMaterialPurchase
from app.entities.te_material_result.model import TeMaterialResult
from app.entities.te_monthly_plan.model import TeMonthlyPlan
from app.entities.te_package_base.model import TePackageBase
from app.entities.te_package_base_new.model import TePackageBaseNew
from app.entities.te_package_categorys_new.model import TePackageCategorysNew
from app.entities.te_purchase_receive.model import TePurchaseReceive
from app.entities.te_purchase_tea.model import TePurchaseTea
from app.entities.te_purchase_transfer.model import TePurchaseTransfer
from app.entities.te_store_transfer.model import TeStoreTransfer
from app.entities.te_store_transfer_fa2.model import TeStoreTransferFa2
from app.entities.tr_constant.model import TrConstant
from app.entities.tr_customer.model import TrCustomer
from app.entities.tr_direct_shipment.model import TrDirectShipment
from app.entities.tr_item.model import TrItem
from app.entities.tr_item_bom.model import TrItemBom
from app.entities.tr_item_group.model import TrItemGroup
from app.entities.tr_purchase.model import TrPurchase
from app.entities.tr_report.model import TrReport
from app.entities.tr_report_item.model import TrReportItem
from app.entities.tr_resale.model import TrResale
from app.entities.tr_store.model import TrStore
from app.entities.tr_supplier.model import TrSupplier

__all__ = [
    "BlendNo",
    "BulkNo",
    "FinishNo",
    "FirepanNo",
    "TeBlendLotBase",
    "TeBlendLotPart",
    "TeConsignProduct",
    "TeFactory1Result",
    "TeFactory1Transfer",
    "TeFactory2Result",
    "TeFactory3Result",
    "TeFactory3Stock",
    "TeGrade",
    "TeLot",
    "TeLotBase",
    "TeLotBom",
    "TeLotCategorysBlend",
    "TeLotCategorysCommon",
    "TeLotCategorysFinish",
    "TeLotCategorysFirepan",
    "TeLotDivide",
    "TeLotPart",
    "TeLotUseItem",
    "TeMaterial",
    "TeMaterialPurchase",
    "TeMaterialResult",
    "TeMonthlyPlan",
    "TePackageBase",
    "TePackageBaseNew",
    "TePackageCategorysNew",
    "TePurchaseReceive",
    "TePurchaseTea",
    "TePurchaseTransfer",
    "TeStoreTransfer",
    "TeStoreTransferFa2",
    "TrConstant",
    "TrCustomer",
    "TrDirectShipment",
    "TrItem",
    "TrItemBom",
    "TrItemGroup",
    "TrPurchase",
    "TrReport",
    "TrReportItem",
    "TrResale",
    "TrStore",
    "TrSupplier",
]

