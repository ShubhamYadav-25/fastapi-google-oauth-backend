from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.payment import Payment, PaymentStatusEnum


async def get_payment(db: AsyncSession, transaction_id: str):
    result = await db.execute(select(Payment).where(Payment.transaction_id == transaction_id))
    return result.scalars().first()


async def create_payment(db: AsyncSession, status: PaymentStatusEnum, payment_type: str, amount: float):
    payment = Payment(status=status, payment_type=payment_type, amount=amount)
    db.add(payment)
    await db.commit()
    await db.refresh(payment)
    return payment


async def get_successful_payments(db: AsyncSession):
    result = await db.execute(select(Payment).where(Payment.status == PaymentStatusEnum.pass_status))
    return result.scalars().all()

async def get_unsuccessful_payments(db: AsyncSession):
    result = await db.execute(select(Payment).where(Payment.status == PaymentStatusEnum.fail))
    return result.scalars().all()

async def get_unsuccessful_payments(db):
    result = await db.execute(select(Payment).where(Payment.status == "fail"))
    return result.scalars().all()

async def get_payments_above_amount(db, min_amount: float):
    result = await db.execute(select(Payment).where(Payment.amount >= min_amount))
    return result.scalars().all()

async def get_payments_by_type(db, payment_type):
    result = await db.execute(select(Payment).where(Payment.payment_type == payment_type))
    return result.scalars().all()