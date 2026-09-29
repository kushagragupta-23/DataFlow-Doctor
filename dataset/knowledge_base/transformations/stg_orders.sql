-- model: stg_orders
select
  cast(order_id as varchar) as order_id,
  cast(customer_id as varchar) as customer_id,
  convert_timezone('UTC', order_ts) as order_ts_utc,
  cast(amount as decimal(12,2)) as amount,
  currency, status, discount_code
from raw.orders
where order_id is not null;
