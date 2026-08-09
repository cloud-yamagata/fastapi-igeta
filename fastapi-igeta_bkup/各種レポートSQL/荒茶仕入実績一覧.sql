select 
 a.year
,a.bid_no
,a.purchase_date
,a.purchase
,a.variety
,a.tea_life
,a.grade
,a.tea_type
,a.tea_rank
,a.field_no
,a.unit_number + a.fraction_number as total_number
,a.unit_weight * a.unit_number + a.fraction_weight * a.fraction_number as total_weight
,(a.unit_weight * a.unit_number + a.fraction_weight * a.fraction_number) * (1 - a.discount) as yield_weight
,round((a.unit_weight * a.unit_number + a.fraction_weight * a.fraction_number) * (1 - a.discount) * a.cost,0) as total_cost
,a.producer
,a.cost
,a.unit_weight
,a.unit_number
,a.fraction_weight
,a.fraction_number
,a.discount
,a.target
,a.target_plan
,b.transfer_weight
,a.unit_weight * a.unit_number + a.fraction_weight * a.fraction_number - coalesce(b.transfer_weight, 0) as rem_weight
,a.remarks
from te_purchase_tea a
left join
(
select
 year
,purchase
,bid_no
,sum(unit_weight * unit_number + fraction_weight * fraction_number) as transfer_weight
from te_purchase_transfer
group by year, purchase, bid_no
) b on a.year = b.year and a.purchase = b.purchase and a.bid_no = b.bid_no
order by a.year, a.purchase_date, a.bid_no