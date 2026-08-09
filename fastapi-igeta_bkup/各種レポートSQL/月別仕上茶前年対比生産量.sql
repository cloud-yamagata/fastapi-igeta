select * from
(
(
select
'今年度' as year
,a.item_name
,coalesce(b."04月", 0) as month_04
,coalesce(b."05月", 0) as month_05
,coalesce(b."06月", 0) as month_06
,coalesce(b."07月", 0) as month_07
,coalesce(b."08月", 0) as month_08
,coalesce(b."09月", 0) as month_09
,coalesce(b."10月", 0) as month_10
,coalesce(b."11月", 0) as month_11
,coalesce(b."12月", 0) as month_12
,coalesce(b."01月", 0) as month_01
,coalesce(b."02月", 0) as month_02
,coalesce(b."03月", 0) as month_03
from tr_item a
left join blend_report_this_weight b on a.item_name = b.商品名
where 0=0
  and a.system_class = '2'
  and a.item_group_no in (3)
  and a.display = true
)
union
(
select
'前年度' as year
,a.item_name
,coalesce(b."04月", 0) as month_04
,coalesce(b."05月", 0) as month_05
,coalesce(b."06月", 0) as month_06
,coalesce(b."07月", 0) as month_07
,coalesce(b."08月", 0) as month_08
,coalesce(b."09月", 0) as month_09
,coalesce(b."10月", 0) as month_10
,coalesce(b."11月", 0) as month_11
,coalesce(b."12月", 0) as month_12
,coalesce(b."01月", 0) as month_01
,coalesce(b."02月", 0) as month_02
,coalesce(b."03月", 0) as month_03
from tr_item a
left join blend_report_last_weight b on a.item_name = b.商品名
where 0=0
  and a.system_class = '2'
  and a.item_group_no in (3)
  and a.display = true
)
) x
order by x.item_name, x.year