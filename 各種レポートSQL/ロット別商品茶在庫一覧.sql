with
--第3工場ロット別生産実績
v_factory3_product_result as
(
select
 a.transfer_date
,a.item_no
,a.product_no
,a.reason
,a.lot_type
,a.transfer_quantity as factory3_product_quantity
from te_store_transfer a
where 0=0
  and a.transfer_type = '1'
  and a.result_type = '1'
  and a.lot_type = '3'
  and a.store_no = 3
)
,
--第3工場ロット別出荷引当実績
v_factory3_stock_allocation as
(
select
 x.item_no
,x.product_no
,max(x.transfer_date) as transfer_date
,count(x.product_no) as count
,sum(x.transfer_quantity) as factory3_sales_quantity
from
(
select
 a.transfer_date
,a.item_no
,a.product_no
,a.reason
,a.lot_type
,a.transfer_quantity
from te_store_transfer a
where 0=0
  and a.transfer_type = '2'
  and a.result_type = '6'
  and a.store_no = 3
) x
group by x.item_no, x.product_no
)

,
--第3工場ロット別商品茶在庫調整
v_factory3_stock_adjust as
(
select
 x.item_no
,x.product_no
,max(x.transfer_date) as transfer_date
,count(x.product_no) as count
,sum(x.transfer_quantity) as factory3_adjust_quantity
from
(
select
 a.transfer_date
,a.item_no
,a.product_no
,a.reason
,a.lot_type
,case a.transfer_type when '2' then -(a.transfer_quantity) else a.transfer_quantity end as  transfer_quantity
from te_store_transfer a
where 0=0
  and a.lot_type = '3'
  and a.result_type = '9'
  and a.store_no = 3
) x
group by x.item_no, x.product_no
)

select
 a.item_no
,item.item_name
,item.organic_class
,a.product_no
,a.transfer_date
--,a.lot_type
,a.factory3_product_quantity
,coalesce(b.factory3_sales_quantity, 0) as factory3_sales_quantity
,coalesce(c.factory3_adjust_quantity, 0) as factory3_adjust_quantity
,a.factory3_product_quantity - coalesce(b.factory3_sales_quantity, 0) + coalesce(c.factory3_adjust_quantity, 0) as factory3_stock
from v_factory3_product_result a
inner join tr_item item on a.item_no = item.item_no
left join v_factory3_stock_allocation b on a.item_no = b.item_no and a.product_no = b.product_no
left join v_factory3_stock_adjust c on a.item_no = c.item_no and a.product_no = c.product_no
where 0=0
  and (case when :item_name != '%' then item_name else '1' end) like (case when :item_name != '%' then :item_name else '1' end)
order by a.item_no, a.product_no