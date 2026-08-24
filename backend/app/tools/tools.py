from datetime import datetime, timedelta
from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from app.models.models import Product, Order, OrderItem
from app.schemas.schemas import PurchaseRequest

ALLOWED_TOOLS = {"search_products","get_order_status","get_delivery_estimate","create_order"}

def search_products(db: Session, brand=None, category=None, query=None, max_price=None):
    stmt = select(Product).where(Product.stock_quantity > 0)
    if brand:
        stmt = stmt.where(Product.brand.ilike(f"%{brand}%"))
    if category:
        stmt = stmt.where(Product.category.ilike(f"%{category}%"))
    if query:
        term = f"%{query}%"
        stmt = stmt.where(or_(Product.name.ilike(term), Product.description.ilike(term), Product.brand.ilike(term)))
    if max_price is not None:
        stmt = stmt.where(Product.price <= max_price)
    return [
        {"id":p.id,"sku":p.sku,"name":p.name,"brand":p.brand,"category":p.category,
         "price":p.price,"stock_quantity":p.stock_quantity,"color":p.color}
        for p in db.scalars(stmt.order_by(Product.name)).all()
    ]

def get_order_status(db: Session, order_id: int, customer_id: int = 1):
    order = db.scalar(select(Order).where(Order.id == order_id, Order.customer_id == customer_id))
    if not order:
        return {"found": False}
    return {"found":True,"order_id":order.id,"status":order.status,"total_amount":order.total_amount,
            "tracking_number":order.tracking_number,"estimated_delivery":order.estimated_delivery.date().isoformat()}

def get_delivery_estimate(db: Session, order_id: int, customer_id: int = 1):
    result = get_order_status(db, order_id, customer_id)
    if not result["found"]:
        return result
    return {"found":True,"order_id":result["order_id"],
            "estimated_delivery":result["estimated_delivery"],"status":result["status"]}

def create_order(db: Session, request: PurchaseRequest):
    products, total = {}, 0.0
    for item in request.items:
        product = db.get(Product, item.product_id)
        if not product:
            raise ValueError(f"Product {item.product_id} was not found")
        if product.stock_quantity < item.quantity:
            raise ValueError(f"Only {product.stock_quantity} unit(s) of {product.name} are available")
        products[item.product_id] = product
        total += product.price * item.quantity

    order = Order(customer_id=request.customer_id,status="Processing",total_amount=round(total,2),
                  estimated_delivery=datetime.utcnow()+timedelta(days=4),tracking_number="PENDING")
    db.add(order)
    db.flush()

    for item in request.items:
        product = products[item.product_id]
        product.stock_quantity -= item.quantity
        db.add(OrderItem(order_id=order.id,product_id=product.id,quantity=item.quantity,unit_price=product.price))

    db.commit()
    db.refresh(order)
    return {"success":True,"order_id":order.id,"total_amount":order.total_amount,
            "status":order.status,"estimated_delivery":order.estimated_delivery.date().isoformat()}
