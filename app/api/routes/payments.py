from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional, List

from app.schemas import payment_crud
from app.models.payment import PaymentStatusEnum, PaymentTypeEnum
from app.deps import get_db

router = APIRouter()

# ---------- Schemas ----------

class CreatePaymentRequest(BaseModel):
    status: PaymentStatusEnum
    payment_type: PaymentTypeEnum
    amount: float


# ---------- Endpoints ----------

@router.post("/", response_model=dict)
async def create_payment(data: CreatePaymentRequest, db: AsyncSession = Depends(get_db)):
    """
    Create a new payment entry.
    """
    payment = await payment_crud.create_payment(
        db, data.status, data.payment_type, data.amount
    )
    return {"transaction_id": payment.transaction_id, "status": payment.status}


@router.get("/{transaction_id}")
async def get_payment(transaction_id: str, db: AsyncSession = Depends(get_db)):
    """
    Get payment details by transaction ID.
    """
    payment = await payment_crud.get_payment(db, transaction_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@router.get("/")
async def list_payments(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    db: AsyncSession = Depends(get_db)
):
    """
    List all successful payments with pagination.
    """
    payments = await payment_crud.get_successful_payments(db)
    return payments[skip: skip + limit]


# ---------- New Endpoints ----------

@router.get("/unsuccessful/")
async def list_unsuccessful_payments(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    db: AsyncSession = Depends(get_db)
):
    """
    List payments where status = 'fail'
    """
    payments = await payment_crud.get_unsuccessful_payments(db)
    return payments[skip: skip + limit]


@router.get("/filter/amount/")
async def filter_payments_by_amount(
    min_amount: float = Query(..., description="Minimum payment amount (inclusive)"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all payments with amount >= given value.
    """
    payments = await payment_crud.get_payments_above_amount(db, min_amount)
    return payments


@router.get("/filter/type/")
async def filter_payments_by_type(
    payment_type: PaymentTypeEnum = Query(..., description="Filter by payment type (UPI or card)"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all payments of a given type.
    """
    payments = await payment_crud.get_payments_by_type(db, payment_type)
    return payments
