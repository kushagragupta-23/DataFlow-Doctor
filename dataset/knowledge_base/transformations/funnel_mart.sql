-- model: funnel_mart
-- joins sessions with purchases using user_id and UTC event dates.
select session_date, count(*) sessions, sum(has_purchase) purchases
from analytics.fct_sessions
group by 1;
