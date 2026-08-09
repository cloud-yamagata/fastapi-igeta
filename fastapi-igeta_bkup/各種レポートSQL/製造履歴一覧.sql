with
v_blend as
(
select
 a.product_no as parent_no
,cast(b.part_lot_no as integer) as child_no
from te_blend_lot_base a
inner join te_blend_lot_part b on a.product_no = b.product_no and b.part_lot_no != ''
--inner join te_blend_lot_base c on cast(b.part_lot_no as numeric) = c.product_no
)
,
--パッケージ情報
v_package as
(
select product_no as parent_no, part_lot_no_1 as child_no from te_package_base where part_lot_no_1 != 0
union select all product_no, part_lot_no_2 as child_no from te_package_base where part_lot_no_2 != 0
union select all product_no, part_lot_no_3 as child_no from te_package_base where part_lot_no_3 != 0
)
,
--委託情報
v_consign as
(
select consign_no as parent_no, supply_product_no as child_no from te_consign_product a where consign_no != 0
)

select
 b.work_date::date as product_date
--,b.process_type
,b.process_name::text
,a.parent_no::integer as parent_no
,b.lot_description::text as parent_name
,a.child_no::integer as child_no
,c.lot_description::text as child_name
from
(
select * from v_blend
union select all * from v_consign
union select all * from v_package
) a
inner join te_lot b on a.parent_no = b.product_no
left join te_lot c on a.child_no = c.product_no
order by b.work_date desc, b.process_type, b.product_no