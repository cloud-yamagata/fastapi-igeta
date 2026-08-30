with
v_store_transfer as
(
select
 cast(to_char(a.transfer_date, 'yyyy') as integer) as year
,cast(to_char(a.transfer_date, 'mm') as integer) as month
,a.item_no
,sum(case when transfer_type = '1' and result_type = '1' and lot_type = '2' then a.transfer_quantity else 0 end) as product -- product
,sum(case when transfer_type = '2' and result_type = '2' and lot_type = '2' then a.transfer_quantity else 0 end) as consume -- consume
,sum(case when transfer_type = '1' and result_type = '4' and lot_type = '2' then a.transfer_quantity else 0 end) as purchase -- purchase
from te_store_transfer a
where (
  (transfer_type = '1' and result_type = '1' and lot_type = '2') -- product
   or
  (transfer_type = '2' and result_type = '2' and lot_type = '2') -- consume
   or
  (transfer_type = '1' and result_type = '4' and lot_type = '2') -- purchase
)
group by a.item_no, to_char(a.transfer_date, 'yyyy'), to_char(a.transfer_date, 'mm')
order by a.item_no, to_char(a.transfer_date, 'yyyy'), to_char(a.transfer_date, 'mm')
)
,
v_plan as
(
select
plan.year
,plan.month
,bulk_no as item_no
,max(item_name) as item_name
,sum(need_size) as need_size
,cast(null as text) as remarks
from te_monthly_product_plan plan
group by plan.year, plan.month, bulk_no
order by plan.year, plan.month, bulk_no
)
,
v_stoc as
(
select 
    a.item_no,
    b.item_name,
    a.year,
    a.month,
    a.product + a.purchase as product,
    a.consume,
    (a.product + a.purchase - a.consume) as stoc_change,
    -- cumulative stock through this month
    sum(a.product + a.purchase - a.consume) over (
        partition by a.item_no 
        order by a.year, a.month
    ) as closing_stock
from v_store_transfer a
inner join tr_item b on a.item_no = b.item_no
order by 
    a.item_no, 
    a.year,
    a.month
)
,
v_raw as
(
select
 plan.year
,plan.month
,plan.item_no
,plan.item_name
,coalesce(stoc.product, 0) as product
,coalesce(stoc.consume, 0) as consume
,coalesce(stoc.stoc_change, 0) as stoc_change
,coalesce(stoc.closing_stock, 0) as closing_stock
,plan.need_size
,plan.remarks
from v_plan plan
left join v_stoc stoc
  on plan.year = stoc.year and plan.month = stoc.month and plan.item_no = stoc.item_no
where 0=0
  and (case when :item_no != '' then CAST(plan.item_no AS text) else '1' end) = (case when :item_no != '' then :item_no else '1' end)
  and (case when :item_name != '%' then plan.item_name else '1' end) like (case when :item_name != '%' then :item_name else '1' end)
)
,
v_flag as
(
select
 a.*
,(a.product = 0 and a.consume = 0 and a.stoc_change = 0 and a.closing_stock = 0) as is_zero
from v_raw a
)
,
v_streak as
(
select
 a.*
,sum(case when a.is_zero then 0 else 1 end)
   over (partition by a.item_no order by a.year, a.month) as streak_id
from v_flag a
)
,
v_adj as
(
select
 a.year
,a.month
,a.item_no
,a.item_name
,a.product
,a.consume
,a.stoc_change
,a.need_size
,a.remarks
,case
   when a.is_zero then
     coalesce(
       max(case when not a.is_zero then a.closing_stock end)
         over (partition by a.item_no, a.streak_id),
       0
     )
     - sum(case when a.is_zero then a.need_size else 0 end)
         over (partition by a.item_no, a.streak_id order by a.year, a.month)
   else a.closing_stock
 end as closing_stock
from v_streak a
)

select
 year
,month
,item_no
,item_name
,product
,consume
,stoc_change
,closing_stock
,need_size
,case
   when closing_stock >= need_size then '達成'
   else '遅延'
 end as complete
,remarks
from v_adj
order by item_no, year, month
