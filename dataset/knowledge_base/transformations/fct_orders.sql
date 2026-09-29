-- model: fct_orders
select o.order_id, o.customer_id, o.order_ts_utc, o.amount, o.currency, o.status
from analytics.stg_orders o
where o.status not in ('test','cancelled_test');
