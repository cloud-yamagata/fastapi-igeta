with
--第2工場ロット生産実績
v_factory2_product as
(
select
 a.lot_no
,a.process_type
,a.product_no
,sum(a.transfer_quantity) as quantity
from te_store_transfer_fa2 a
where a.transfer_type = '1'
  and a.result_type = '1'
group by a.lot_no, a.process_type, a.product_no
)
,
--第2工場ロット投入実績
v_factory2_input as
(
select
 a.lot_no
,a.process_type
,a.product_no
,sum(a.transfer_quantity) as quantity
from te_store_transfer_fa2 a
where a.transfer_type = '2'
  and a.result_type = '2'
group by a.lot_no, a.process_type, a.product_no
)
,
--第2工場仕上品販売
v_factory2_sales as
(
select
 a.lot_no
,a.process_type
,a.product_no
,sum(a.transfer_quantity) as quantity
from te_store_transfer_fa2 a
where a.transfer_type = '2'
  and a.result_type = '5'
group by a.lot_no, a.process_type, a.product_no
)
,
--第2工場仕上品調整
v_factory2_adjust as
(
select
 a.lot_no
,a.process_type
,a.product_no
,sum(a.transfer_quantity * case when a.transfer_type = '2' then -1 else 1 end) as quantity
from te_store_transfer_fa2 a
where a.result_type = '8'
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

select
 a.lot_no
,case a.process_type
  when '01' then '荒茶原料'
  when '02' then '荒茶配合'
  when '03' then '仕上製造'
  when '04' then '火入製造'
  when '05' then '仕上配合'
  else ''
end process_type
,a.product_no
,a.product_date
,a.lot_name
,a.item_name
,a.make_year
,a.count
,coalesce(b.quantity, 0) as factory2_product_quantity
,coalesce(c.quantity, 0) as factory2_input_quantity
,coalesce(d.quantity, 0) as factory2_sales_quantity
,coalesce(e.quantity, 0) as factory2_adjust_quantity
,coalesce(f.quantity, 0) - coalesce(g.quantity, 0) as factory3_receive_quantity
,coalesce(b.quantity, 0) - coalesce(c.quantity, 0) - coalesce(d.quantity, 0) + coalesce(e.quantity, 0) - coalesce(f.quantity, 0) + coalesce(g.quantity, 0) as factory2_stock
from vi_lot_material a
inner join v_factory2_product b on a.lot_no = b.lot_no
left join v_factory2_input c on a.lot_no = c.lot_no
left join v_factory2_sales d on a.lot_no = d.lot_no
left join v_factory2_adjust e on a.lot_no = e.lot_no
left join v_factory3_receive f on a.lot_no = f.lot_no
left join v_factory3_return g on a.lot_no = g.lot_no
order by a.process_type, a.item_name, product_no