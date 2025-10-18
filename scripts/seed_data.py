import asyncio
import sys
import os

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import Base, get_db, engine
from app.models.customer import Customer
from app.models.payment import Payment, PaymentStatusEnum, PaymentTypeEnum
from app.models.restaurant import Restaurant, AreaEnum
from app.models.order import Order, FoodItemEnum


async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async for db in get_db():
        # Seed restaurants
        r1 = Restaurant(restaurant_name='Spice Heaven', area=AreaEnum.mumbai)
        r2 = Restaurant(restaurant_name='Curry House', area=AreaEnum.bangalore)
        db.add_all([r1, r2])
        await db.commit()
        await db.refresh(r1)
        await db.refresh(r2)
        
        # Seed customers
        c1 = Customer(name='Alice', google_id='alice123', age=25)
        c2 = Customer(name='Bob', google_id='bob123', age=30)
        db.add_all([c1, c2])
        await db.commit()
        
        # Seed payments
        p1 = Payment(status=PaymentStatusEnum.pass_status, payment_type=PaymentTypeEnum.upi, amount=250.0)
        p2 = Payment(status=PaymentStatusEnum.pass_status, payment_type=PaymentTypeEnum.card, amount=150.0)
        db.add_all([p1, p2])
        await db.commit()
        
        # Seed orders
        o1 = Order(food_item=FoodItemEnum.veg_manchurian, transaction_id=p1.transaction_id, restaurant_id=r1.restaurant_id)
        o2 = Order(food_item=FoodItemEnum.chicken_noodles, transaction_id=p2.transaction_id, restaurant_id=r2.restaurant_id)
        db.add_all([o1, o2])
        await db.commit()


if __name__ == '__main__':
    asyncio.run(seed())