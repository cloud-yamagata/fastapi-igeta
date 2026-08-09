with
use_tea_stock as
(
select
 c.use_no as item_no
,a.transfer_date
,a.lot_no
,a.product_no
,text(case a.process_type
 when '01' then '荒茶原料'
 when '02' then '荒茶配合'
 when '03' then '仕上製造'
 when '04' then '火入製造'
 when '05' then '仕上配合'
 else ''
end) as process_name
,c.make_year
,c.count
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
 when a.transfer_type = '3' and a.result_type = '7' then a.transfer_quantity
 else -(a.transfer_quantity)
end transfer_quantity
from te_store_transfer_fa2 a
inner join te_lot_base b on a.lot_no = b.lot_no
inner join te_lot_use_item c on b.lot_no = c.lot_no
where ((a.transfer_type = '1' )
   or (a.transfer_type = '2' and a.result_type = '2')
   or (a.transfer_type = '2' and a.result_type = '5')
   or (a.transfer_type = '3' and a.result_type = '3')
   or (a.transfer_type = '3' and a.result_type = '7')
   or (a.lot_type = '2' and a.result_type = '9'))
)

select
 a.item_no
,b.item_name
,a.transfer_date
,a.product_no
,a.process_name
,a.make_year
,a.count
,a.transfer_type
,a.transfer_name
,a.result_type
,a.result_name
,a.reason
,a.transfer_quantity
,sum(a.transfer_quantity) over(
partition by a.item_no, a.lot_no
order by a.item_no, a.transfer_date, a.transfer_type, a.result_type
rows between unbounded preceding and current row
) as summation_use_quantity
from
(
select * from use_tea_stock
) a
inner join tr_item b on a.item_no = b.item_no
