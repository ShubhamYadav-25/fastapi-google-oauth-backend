from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.deps import get_db
from app.schemas import order_crud, payment_crud, customer_crud
from pydantic import BaseModel


router = APIRouter()


class CreateOrderRequest(BaseModel):
    food_item: str
    transaction_id: str
    restaurant_id: str
    customer_id: str


@router.post("/place")
async def place_order(req: CreateOrderRequest, db: AsyncSession = Depends(get_db)):
    payment = await payment_crud.get_payment(db, req.transaction_id)
    if not payment or payment.status != payment_crud.PaymentStatusEnum.pass_status:
        raise HTTPException(status_code=400, detail="Payment not successful")
    
    customer = await customer_crud.get_customer(db, req.customer_id)
    if not customer:
        raise HTTPException(status_code=400, detail="Payment not successful")
    order = await order_crud.create_order(db, req.food_item, req.transaction_id, req.restaurant_id, req.customer_id)
    return order

@router.get("/{order_id}")
async def get_order(order_id: str, db: AsyncSession = Depends(get_db)):
    order = await order_crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.delete("/{order_id}")
async def delete_order(order_id: str, db: AsyncSession = Depends(get_db)):
    success = await order_crud.delete_order(db, order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"detail": "Order deleted successfully"}