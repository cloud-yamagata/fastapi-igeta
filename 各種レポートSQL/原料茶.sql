select * from tr_item
where system_class = :system_class
  and display = true
order by display_order, item_name