-- model: mart_daily_revenue
select date(order_ts_utc) as order_date, currency, sum(amount) as gross_revenue, count(*) as orders
from analytics.fct_orders
where status = 'completed'
group by 1,2;
