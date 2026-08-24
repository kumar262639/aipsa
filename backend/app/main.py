from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import Base, engine
from app.models.models import Product, Customer, Order, OrderItem
from app.api.routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI-Powered Shopping Assistant",version="1.0.0",
             description="Tool-grounded e-commerce shopping assistant POC")
app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:5173","http://127.0.0.1:5173"],
                   allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.include_router(router,prefix="/api")
