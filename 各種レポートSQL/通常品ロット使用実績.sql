select
 c.work_date as work_date_part
,c.item_no as item_no_part
,a.material_name_base as item_name_part
,a.part_lot_no
,c.product_quantity as complete_quantity
,a.make_year as make_year_part
,a.count as count_part
,b.work_date as work_date_blend
,b.item_no as item_no_blend
,b.product_name as item_name_blend
,a.product_no
,b.make_year as make_year_blend
,b.count as count_blend
,a.use_quantity
,a.remarks
from (select * from te_blend_lot_part where part_lot_no != '') a
inner join te_blend_lot_base b on a.product_no = b.product_no
inner join vi_lot_list c on to_number(a.part_lot_no, '000000') = c.product_no and a.material_name_base = c.product_name
order by c.item_no, a.part_lot_no , b.work_date desc, b.product_no