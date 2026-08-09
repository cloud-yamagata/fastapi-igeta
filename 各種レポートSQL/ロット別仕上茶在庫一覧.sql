with
--第2工場ロット投入実績
v_lot_list as
(
select
 a.lot_no
,a.item_no
,b.make_year
,a.product_no
,b.count
,a.product_name
,a.work_date as product_date
,a.process_type
,a.process_name
,a.store_no
,case when a.store_no = 2 then product_quantity else 0 end factory2_product_quantity
,case when a.store_no = 3 then product_quantity else 0 end factory3_product_quantity
from vi_lot_list a
left join te_blend_lot_base b on a.product_no = b.product_no
where 0=0
  and a.product_name != '実績削除'
--and to_char(a.work_date, 'YYYYMMDD') >= :transfer_date
)
,--第3工場受入実績
v_factory3_receive as
(
select
 a.item_no
,a.product_no
,sum(case a.store_no when 3 then a.transfer_quantity else -(a.transfer_quantity) end) as quantity
from te_store_transfer a
where a.transfer_type = '3'
  and a.result_type in ('3', '7')
--and to_char(a.transfer_date, 'YYYYMMDD') >= :transfer_date
--and a.store_no = 3
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
--and to_char(a.transfer_date, 'YYYYMMDD') >= :transfer_date
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
--and to_char(a.transfer_date, 'YYYYMMDD') >= :transfer_date
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
--and to_char(a.transfer_date, 'YYYYMMDD') >= :transfer_date
group by a.item_no, a.product_no 
)

select
 a.item_no
,a.product_name
--,a.process_type
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
,coalesce(i.factory2_stock, 0) as factory2_stock
,coalesce(a.factory3_product_quantity, 0) + coalesce(e.quantity, 0) - coalesce(f.quantity, 0) - coalesce(g.quantity, 0) + coalesce(h.quantity, 0) as factory3_stock
from v_lot_list a
left join v_factory3_receive e on a.item_no = e.item_no and a.product_no = e.product_no
left join v_factory3_input f on a.item_no = f.item_no and a.product_no = f.product_no
left join v_factory3_ship g on a.item_no = g.item_no and a.product_no = g.product_no
left join v_factory3_adjust h on a.item_no = h.item_no and a.product_no = h.product_no
left join vi_factory2_stock i on a.product_no = i.product_no and i.process_type = '05'
where 0=0
  and a.process_type != '12'
  and (case when :item_name != '%' then a.product_name else '1' end) like (case when :item_name != '%' then :item_name else '1' end)
order by a.process_type, item_no, product_date, product_no