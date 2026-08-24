from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.schemas import ChatRequest, ConfirmPurchaseRequest
from app.services.orchestrator import handle_chat, confirm_purchase
from app.services.audit import audit_tool_call
from app.tools.tools import search_products

router = APIRouter()
pending_proposals = {}

@router.get("/health")
def health():
    return {"status":"ok"}

@router.get("/products")
def products(brand: str|None=None, category: str|None=None, db: Session=Depends(get_db)):
    return {"products":search_products(db,brand=brand,category=category)}

@router.post("/chat")
def chat(request: ChatRequest, db: Session=Depends(get_db)):
    result = handle_chat(db,request.message,pending_proposals)
    audit_tool_call(request.session_id,result.get("tool"),True,{})
    return result

@router.post("/purchase/confirm")
def purchase_confirm(request: ConfirmPurchaseRequest, db: Session=Depends(get_db)):
    proposal = pending_proposals.pop(request.proposal_id,None)
    if not proposal:
        raise HTTPException(status_code=404,detail="Purchase proposal not found or expired.")
    try:
        result = confirm_purchase(db,proposal)
        audit_tool_call("demo-session","create_order",True,{"customer_id":proposal["customer_id"],
                                                          "item_count":len(proposal["items"])})
        return {"message":f"Purchase successful. Your order number is #{result['order_id']}. Total: ${result['total_amount']:.2f}.",
                "tool":"create_order","tool_result":result,"verified":True}
    except ValueError as exc:
        audit_tool_call("demo-session","create_order",False,{})
        raise HTTPException(status_code=400,detail=str(exc))
