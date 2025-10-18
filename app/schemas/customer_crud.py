from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.customer import Customer


async def get_customer_by_google_id(db: AsyncSession, google_id: str):
    result = await db.execute(select(Customer).where(Customer.google_id == google_id))
    return result.scalars().first()


async def create_customer(db: AsyncSession, name: str, google_id: str, age: int):
    customer = Customer(name=name, google_id=google_id, age=age)
    db.add(customer)
    await db.commit()
    await db.refresh(customer)
    return customer

async def get_customer(db: AsyncSession, uuid: str):
    result = await db.execute(select(Customer).where(Customer.id == uuid))
    return result.scalars().first()