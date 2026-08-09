with
use_tea_stock as
(
select
 a.item_no
,a.transfer_date
,a.product_no
,b.make_year
,b.count 
,a.transfer_type
,text(case a.transfer_type
 when '1' then '入庫'
 when '2' then '出庫'
 when '3' then '移動'
 else ''
end) as transfer_name
,a.result_type
,text(case a.result_type
 when '1' then '生産'
 when '2' then '使用'
 when '3' then '受入'
 when '4' then '入荷'
 when '5' then '出荷'
 when '6' then '引当'
 when '7' then '返品'
 when '9' then '調整'
 else ''
end) as result_name
,a.reason
,case
 when a.transfer_type = '1' then a.transfer_quantity
 when a.transfer_type = '2' then -(a.transfer_quantity)
 else a.transfer_quantity
end transfer_quantity
from te_store_transfer a
left join te_blend_lot_base b on a.product_no = b.product_no
where (a.transfer_type = '1' and a.result_type = '1' and a.lot_type = '3' and a.store_no = 3)
   or (a.transfer_type = '2' and a.result_type = '6' and a.lot_type = '3'and a.store_no = 3)
   or (a.result_type = '9' and a.lot_type = '3' and a.store_no = 3)
order by a.item_no, a.transfer_date, a.transfer_type, a.result_type
)

select
 a.item_no
,b.item_name
,a.transfer_date
,a.product_no
--,a.make_year
--,a.count 
,a.transfer_type
,a.transfer_name
,a.result_type
,a.result_name
,a.reason
,a.transfer_quantity
,sum(a.transfer_quantity) over(
partition by a.item_no
order by a.item_no, a.transfer_date, a.transfer_type, a.result_type
rows between unbounded preceding and current row
) as summation_use_quantity
from
(
select * from use_tea_stock
--union select all
-- item_no
--,transfer_date
--,null as lot_no
--,null as make_year
--,null as count
--,transfer_type
--,transfer_name
--,result_type
--,result_name
--,reason
--,transfer_quantity
--from vi_stock_inventory
--where item_type = '2'
) a
inner join tr_item b on a.item_no = b.item_no
where 0=0
--and (case when :transfer_date != '%' then to_char(a.transfer_date,'YYYY/MM/DD') else '1' end) like (case when :transfer_date != '%' then :transfer_date else '1' end)
  and (case when :item_name != '%' then b.item_name else '1' end) = (case when :item_name != '%' then :item_name else '1' end)
--order by a.item_no, a.transfer_date, a.product_no, a.transfer_type, a.result_type