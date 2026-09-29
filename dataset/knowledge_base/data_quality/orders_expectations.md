# Orders Data Quality

- order_id: non-null and unique
- customer_id: non-null >= 99.9%
- amount: between 0 and 1,000,000
- currency: in approved ISO currency list
- daily revenue control total variance <= 0.5% versus source settlement extract
