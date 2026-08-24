from app.services.orchestrator import fallback_route

def test_product_route():
    r=fallback_route("What Nike t shirts are available?")
    assert r["kind"]=="search" and r["brand"]=="Nike" and r["category"]=="t-shirt"

def test_order_route():
    r=fallback_route("What is the status of order 1001?")
    assert r["kind"]=="order_status" and r["order_id"]==1001

def test_delivery_route():
    r=fallback_route("When will order 1001 be delivered?")
    assert r["kind"]=="delivery" and r["order_id"]==1001

def test_purchase_route():
    r=fallback_route("Buy 2 Nike t shirts")
    assert r["kind"]=="purchase" and r["quantity"]==2
