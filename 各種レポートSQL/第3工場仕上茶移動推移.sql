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
 when a.transfer_type = '1' and a.store_no = 3 then a.transfer_quantity
 when a.transfer_type = '3' and a.store_no = 3 then a.transfer_quantity
 else -(a.transfer_quantity)
end transfer_quantity
from te_store_transfer a
left join te_blend_lot_base b on a.product_no = b.product_no
where a.lot_type= '2' and
     ((a.transfer_type = '3' and a.store_no = 3)
   or (a.transfer_type = '1' and a.result_type = '1' and a.store_no = 3)
   or (a.transfer_type = '1' and a.result_type = '4' and a.store_no = 3)
   or (a.transfer_type = '2' and a.result_type = '2' and a.store_no = 3)
   or (a.transfer_type = '2' and a.result_type = '5' and a.store_no = 3)
   or (a.transfer_type = '3' and a.result_type = '7' and a.store_no = 2)
   or (a.lot_type = '2' and a.result_type = '9' and a.store_no = 3))
order by a.item_no, a.transfer_date, a.transfer_type, a.result_type
)

select
 a.item_no
,b.item_name
,a.transfer_date
,a.product_no
,a.make_year
,a.count 
,a.transfer_type
,a.transfer_name
,a.result_type
,a.result_name
,a.reason
,a.transfer_quantity
,sum(a.transfer_quantity) over(
partition by a.item_no, a.product_no
order by a.item_no, a.transfer_date, a.transfer_type, a.result_type
rows between unbounded preceding and current row
) as summation_use_quantity
from
(
select * from use_tea_stock
) a
inner join tr_item b on a.item_no = b.item_no
