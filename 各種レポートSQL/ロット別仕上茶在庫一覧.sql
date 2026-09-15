with
v_lot as
(
select
a.lot_no
,b.work_date as product_date
,b.product_no
,a.make_year
,a.count
,b.lot_name as process_name
,b.organic_class
,b.unit_weight * b.unit_number + b.fraction_weight + b.fraction_number as transfer_quantity
,b.remarks
from te_lot_use_item a
inner join te_lot_base b
  on a.lot_no = b.lot_no
order by b.product_no 
)
,
--第2工場ロット投入実績
v_lot_list as
(
select
a.item_no
,a.product_no
,b.item_name
,a.transfer_date as product_date
,a.reason as process_name
,c.make_year
,c.count
,a.store_no
,case when a.store_no = 2 then a.transfer_quantity else 0 end factory2_product_quantity
,case when a.store_no = 3 then a.transfer_quantity else 0 end factory3_product_quantity
from te_store_transfer a
left join tr_item b on a.item_no = b.item_no
left join v_lot c on a.product_no = c.product_no
where (
 (a.transfer_type = '1' and a.result_type = '1' and a.lot_type = '2' and a.reason = '通常品生産')
  or
 (a.transfer_type = '1' and a.result_type = '4' and a.lot_type = '2' and a.reason = '仕上品仕入')
  or 
 (a.transfer_type = '1' and a.result_type = '4' and a.lot_type = '2' and a.reason = '外部委託納品')
)
)
,
--第3工場受入実績
v_factory3_receive as
(
select
 a.item_no
,a.product_no
,sum(case a.store_no when 3 then a.transfer_quantity else -(a.transfer_quantity) end) as quantity
from te_store_transfer a
where a.transfer_type = '3'
  and a.result_type in ('3', '7')
group by a.item_no, a.product_no
)
,
--第3工場ロット投入実績
v_factory3_input as
(
select
 a.item_no
,a.product_no
,sum(a.transfer_quantity) as quantity
from te_store_transfer a
where a.transfer_type = '2'
  and a.result_type = '2'
  and a.store_no = 3
group by a.item_no, a.product_no
)
,
--第3工場出荷実績
v_factory3_ship as
(
select
 a.item_no
,a.product_no
,sum(a.transfer_quantity) as quantity
from te_store_transfer a
where a.transfer_type = '2'
  and a.result_type = '5'
  and a.store_no = 3
group by a.item_no, a.product_no 
)
,
--第3工場仕上品調整
v_factory3_adjust as
(
select
 a.item_no
,a.product_no
,sum(case a.transfer_type when '2' then -(a.transfer_quantity) else a.transfer_quantity end) as quantity
from te_store_transfer a
where a.lot_type = '2'
  and a.result_type = '9'
  and a.store_no = 3
group by a.item_no, a.product_no 
)

select
 a.item_no
,a.item_name
,a.product_date
,a.product_no
,a.make_year
,a.count
,a.process_name
,a.store_no
,a.factory2_product_quantity
,a.factory3_product_quantity
,coalesce(e.quantity, 0) as factory3_receive_quantity
,coalesce(f.quantity, 0) as factory3_input_quantity
,coalesce(g.quantity, 0) as factory3_ship_quantity
,coalesce(h.quantity, 0) as factory3_adjust_quantity
,case when coalesce(a.factory2_product_quantity, 0) > 0 then coalesce(a.factory2_product_quantity, 0) - coalesce(f.quantity, 0) else 0 end factory2_stock
,coalesce(a.factory3_product_quantity, 0) + coalesce(e.quantity, 0) - coalesce(f.quantity, 0) - coalesce(g.quantity, 0) + coalesce(h.quantity, 0) as factory3_stock
from v_lot_list a
left join v_factory3_receive e on a.item_no = e.item_no and a.product_no = e.product_no
left join v_factory3_input f on a.item_no = f.item_no and a.product_no = f.product_no
left join v_factory3_ship g on a.item_no = g.item_no and a.product_no = g.product_no
left join v_factory3_adjust h on a.item_no = h.item_no and a.product_no = h.product_no
order by item_no, product_no, product_date