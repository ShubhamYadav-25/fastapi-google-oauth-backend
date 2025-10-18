from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.order import Order


async def create_order(db: AsyncSession, food_item: str, transaction_id: str, restaurant_id: str, customer_id: str):
    order = Order(food_item=food_item, transaction_id=transaction_id, restaurant_id=restaurant_id, customer_id=customer_id)
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order


async def get_orders_by_restaurant(db: AsyncSession, restaurant_id: str):
    result = await db.execute(select(Order).where(Order.restaurant_id == restaurant_id))
    return result.scalars().all()


async def get_order(db: AsyncSession, order_id: str):
    result = await db.execute(select(Order).where(Order.order_id == order_id))
    order = result.scalars().first()
    return order

# ----------------- Update Order -----------------
async def update_order(db: AsyncSession, order_id: str, updates: dict):
    order = await get_order(db, order_id)
    if not order:
        return None

    for key, value in updates.items():
        setattr(order, key, value)

    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order

# ----------------- Delete Order -----------------
async def delete_order(db: AsyncSession, order_id: str):
    order = await get_order(db, order_id)
    if not order:
        return False

    await db.delete(order)
    await db.commit()
    return True