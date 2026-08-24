from datetime import datetime,timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.database import Base
from app.models.models import Product,Customer,Order
from app.tools.tools import search_products,get_order_status,create_order
from app.schemas.schemas import PurchaseRequest,OrderItemRequest

engine=create_engine("sqlite:///./test_shop.db",connect_args={"check_same_thread":False})
TestingSession=sessionmaker(bind=engine)

def setup_function():
    Base.metadata.drop_all(engine); Base.metadata.create_all(engine)
    db=TestingSession()
    db.add(Customer(id=1,name="Test",email="test@example.com"))
    db.add(Product(id=1,sku="X1",name="Nike Test Shirt",brand="Nike",category="T-Shirt",
                   description="",price=10,stock_quantity=5,color="Black"))
    db.add(Order(id=1,customer_id=1,status="Shipped",total_amount=10,
                 estimated_delivery=datetime.utcnow()+timedelta(days=2),tracking_number="T1"))
    db.commit(); db.close()

def test_search_products():
    db=TestingSession(); result=search_products(db,brand="Nike",category="T-Shirt")
    assert len(result)==1 and result[0]["brand"]=="Nike"; db.close()

def test_order_status_is_customer_scoped():
    db=TestingSession()
    assert get_order_status(db,1,1)["found"] is True
    assert get_order_status(db,1,999)["found"] is False
    db.close()

def test_create_order_decrements_inventory():
    db=TestingSession()
    result=create_order(db,PurchaseRequest(customer_id=1,items=[OrderItemRequest(product_id=1,quantity=2)]))
    assert result["success"] is True and result["total_amount"]==20
    assert db.get(Product,1).stock_quantity==3
    db.close()
