from datetime import datetime,timedelta
from pathlib import Path
from app.db.database import Base,engine,SessionLocal
from app.models.models import Product,Customer,Order,OrderItem

def seed():
    Path("data").mkdir(exist_ok=True)
    Base.metadata.create_all(bind=engine)
    db=SessionLocal()
    try:
        if db.query(Product).count():
            print("Database already seeded.")
            return
        products=[
            Product(id=1,sku="NK-001",name="Nike Dri-FIT T-Shirt",brand="Nike",category="T-Shirt",
                    description="Moisture-wicking athletic t-shirt",price=29.99,stock_quantity=42,color="Black"),
            Product(id=2,sku="NK-002",name="Nike Sportswear T-Shirt",brand="Nike",category="T-Shirt",
                    description="Everyday cotton t-shirt",price=24.99,stock_quantity=25,color="White"),
            Product(id=3,sku="AD-001",name="Adidas Essentials Hoodie",brand="Adidas",category="Hoodie",
                    description="Classic fleece hoodie",price=49.99,stock_quantity=17,color="Gray"),
            Product(id=4,sku="AD-002",name="Adidas Runfalcon Shoes",brand="Adidas",category="Shoes",
                    description="Lightweight running shoes",price=69.99,stock_quantity=12,color="Black"),
            Product(id=5,sku="LV-001",name="Levi's 501 Jeans",brand="Levi's",category="Jeans",
                    description="Classic straight-fit jeans",price=79.99,stock_quantity=8,color="Blue"),
            Product(id=6,sku="PM-001",name="Puma Essentials T-Shirt",brand="Puma",category="T-Shirt",
                    description="Comfort cotton t-shirt",price=22.99,stock_quantity=30,color="Red")]
        db.add_all(products)
        db.add(Customer(id=1,name="Alex Customer",email="alex@example.com"))
        db.flush()
        now=datetime.utcnow()
        db.add_all([
            Order(id=1001,customer_id=1,status="Shipped",total_amount=59.98,order_date=now-timedelta(days=2),
                  estimated_delivery=now+timedelta(days=2),tracking_number="UPS-DEMO-1001"),
            Order(id=1002,customer_id=1,status="Processing",total_amount=49.99,order_date=now-timedelta(days=1),
                  estimated_delivery=now+timedelta(days=4),tracking_number="PENDING")])
        db.flush()
        db.add_all([
            OrderItem(order_id=1001,product_id=1,quantity=2,unit_price=29.99),
            OrderItem(order_id=1002,product_id=3,quantity=1,unit_price=49.99)])
        products[0].stock_quantity-=2
        products[2].stock_quantity-=1
        db.commit()
        print("Seeded shopping assistant database.")
    finally:
        db.close()

if __name__=="__main__":
    seed()
