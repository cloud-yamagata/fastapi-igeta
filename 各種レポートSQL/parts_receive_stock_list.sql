with
--第2工場ロット生産実績
v_factory2_product as
(
select
 a.lot_no
,a.process_type
,a.product_no
,max(a.transfer_date) as product_date
,sum(a.transfer_quantity) as quantity
from te_store_transfer_fa2 a
where a.transfer_type = '1'
  and a.result_type = '1'
  and a.process_type = '05'
group by a.lot_no, a.process_type, a.product_no
)
,
--第3工場受入実績
v_factory3_receive as
(
select
 a.lot_no
,a.process_type
,a.product_no
,sum(a.transfer_quantity) as quantity
from te_store_transfer_fa2 a
where a.transfer_type = '3'
  and a.result_type in ('3')
group by a.lot_no, a.process_type, a.product_no
)
,
--第3工場投入実績
v_factory3_input as
(
select
 a.product_no
,'05' as process_type
,sum(a.transfer_quantity) as quantity
from te_store_transfer a
where a.transfer_type = '2'
  and a.result_type in ('2')
  and a.store_no = 3
  and a.lot_type = '2'
group by a.product_no
)
,
--第3工場返品実績
v_factory3_return as
(
select
 a.lot_no
,a.process_type
,a.product_no
,sum(a.transfer_quantity) as quantity
from te_store_transfer_fa2 a
where a.transfer_type = '3'
  and a.result_type in ('7')
group by a.lot_no, a.process_type, a.product_no
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
 a.product_date
,b.use_no as item_no
,a.product_no
,b.use_name as product_name
,b.make_year
,b.count
,coalesce(a.quantity, 0) as product_quantity
,coalesce(c.factory2_stock, 0)  as factory2_stock
,coalesce(d.quantity, 0) - coalesce(e.quantity, 0) - coalesce(f.quantity, 0) + coalesce(g.quantity, 0) as factory3_stock
from v_factory2_product a
inner join te_lot_use_item b on a.lot_no = b.lot_no
left join vi_factory2_stock c on a.product_no = c.product_no and c.process_type = '05'
left join v_factory3_receive d on a.lot_no = d.lot_no
left join v_factory3_return e on a.lot_no = e.lot_no
left join v_factory3_input f on a.product_no = f.product_no
left join v_factory3_adjust g on a.product_no = g.product_no
where 0=0
order by b.use_no, a.product_no
