from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1000)
    session_id: str = Field(default="demo-session", max_length=100)

class OrderItemRequest(BaseModel):
    product_id: int
    quantity: int = Field(gt=0, le=10)

class PurchaseRequest(BaseModel):
    customer_id: int = Field(gt=0)
    items: list[OrderItemRequest] = Field(min_length=1, max_length=10)

class ConfirmPurchaseRequest(BaseModel):
    proposal_id: str = Field(min_length=1, max_length=100)
