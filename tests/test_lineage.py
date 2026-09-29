from lineage import downstream_assets, upstream_assets

def test_downstream_orders():
    assets = [x["asset"] for x in downstream_assets("raw.orders")]
    assert "analytics.fct_orders" in assets
    assert "analytics.mart_daily_revenue" in assets

def test_upstream_customer_360():
    assets = [x["asset"] for x in upstream_assets("analytics.customer_360")]
    assert "raw.customers" in assets
    assert "raw.orders" in assets
