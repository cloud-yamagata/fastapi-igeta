with
v_product as
(
--パッケージロット
select
 '12' as process_type
,product_no
,work_date as transfer_date
,item_no
,1 as item_group_no
,product_name
,complete_quantity as product_quantity
,remarks as lot_description
from te_package_base
--ブレンドロット
union select all
case store_no
 when 2 then '05'
 when 3 then '11'
 else ''
end as process_type 
,product_no
,work_date as transfer_date
,item_no
,3 as item_group_no
,product_name
,unit_weight * unit_number + fraction_weight * fraction_number as product_quantity
,remarks as lot_description
from te_blend_lot_base
--仕上品仕入
union select all
 '08' as process_type
,purchase_no as product_no
,purchase_date as transfer_date
,item_no
,6 as item_group_no
,item_name as product_name
,purchase_quantity as product_quantity  
,supplier as lot_description
from te_material_purchase
--外注委託
union select all
 '10' as process_type
,consign_no as product_no
,consign_date  as transfer_date
,item_no
,5 as item_group_no
,item_name as product_name
,consign_quantity as product_quantity
,supplier as lot_description
from te_consign_product
)

--ロット履歴一覧
select
 a.lot_no
,a.product_no
,a.work_date
,a.process_type
,a.process_name
,a.lot_name
--,case when a.lot_description != b.product_name then a.lot_description else '' end as lot_description
,b.lot_description
,b.item_no
,coalesce(b.product_name, '実績削除') as product_name
,case when a.work_date != b.transfer_date then to_char(b.transfer_date,'YYYY/MM/DD') else '' end as transfer_date
,b.product_quantity
from te_lot a
left join v_product b on a.product_no = b.product_no and a.process_type = b.process_type
where 0=0
  and (case when :item_name != '%' then b.product_name else '1' end) = (case when :item_name != '%' then :item_name else '1' end)