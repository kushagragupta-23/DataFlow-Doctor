-- model: customer_360
select c.customer_id, c.country, c.segment, count(o.order_id) as lifetime_orders, coalesce(sum(o.amount),0) as lifetime_revenue
from analytics.dim_customers c
left join analytics.fct_orders o using(customer_id)
group by 1,2,3;
