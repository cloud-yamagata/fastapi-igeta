with
v_store_transfer as
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
 else ''
end) as transfer_name
,a.result_type
,text(case a.result_type
 when '1' then '生産'
 when '6' then '引当'
 else ''
end) as result_name
,a.reason
,case
 when a.transfer_type = '1' then a.transfer_quantity
 when a.transfer_type = '2' then -(a.transfer_quantity)
 else a.transfer_quantity
end transfer_quantity
,a.store_party_name
,min(transfer_date) over( partition by a.item_no, a.lot_no) as product_date
,max(transfer_date) over( partition by a.item_no, a.lot_no) as max_date
,max(a.result_type) over( partition by a.item_no, a.lot_no) as result_max
,rank() over(partition by a.item_no, a.lot_no order by a.item_no, a.lot_no, a.transfer_date desc, a.transfer_type desc , a.result_type desc, a.store_party_name desc) as rank
,sum(case when a.transfer_type = '1' then a.transfer_quantity else 0 end)
over(partition by a.item_no, a.lot_no) as product_quantity
,sum(case when a.transfer_type = '2' then a.transfer_quantity else 0 end)
over(partition by a.item_no, a.lot_no) as transfer_quantity_sum
,sum(
case
 when a.transfer_type = '1' then a.transfer_quantity
 when a.transfer_type = '2' then -(a.transfer_quantity)
 else a.transfer_quantity
end)
over(partition by a.item_no, a.lot_no order by a.item_no, a.product_no, a.transfer_date, a.transfer_type, a.result_type, a.store_party_name
rows between unbounded preceding and current row
) as rem_stock_quantity
from te_store_transfer a
left join te_blend_lot_base b on a.product_no = b.product_no
where (a.transfer_type = '1' and a.result_type = '1' and a.store_no = 3)
   or (a.transfer_type = '2' and a.result_type = '6' and a.store_no = 3)
order by a.item_no, a.transfer_date, a.transfer_type, a.result_type
)

select
 a.item_no
,b.item_name
,a.product_no
,a.product_date
,a.transfer_date
,a.transfer_name
,a.result_name
,a.store_party_name
,a.transfer_quantity
,a.rem_stock_quantity
--,a.result_max
from v_store_transfer a
inner join tr_item b on a.item_no = b.item_no
where 0=0
--and a.product_date != a.max_date
  and a.product_quantity > a.transfer_quantity_sum
  and (case when :item_name != '%' then b.item_name else '1' end) like (case when :item_name != '%' then :item_name else '1' end)
order by a.item_no, a.product_no, a.product_date desc , a.transfer_date, a.transfer_type, a.result_type