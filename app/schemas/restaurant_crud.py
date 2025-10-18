from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.restaurant import Restaurant


async def create_restaurant(db: AsyncSession, restaurant_name: str, area: str):
    restaurant = Restaurant(restaurant_name=restaurant_name, area=area)
    db.add(restaurant)
    await db.commit()
    await db.refresh(restaurant)
    return restaurant


async def get_restaurant(db: AsyncSession, restaurant_id: str):
    result = await db.execute(select(Restaurant).where(Restaurant.restaurant_id == restaurant_id))
    return result.scalars().first()


async def list_restaurants(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(Restaurant).offset(skip).limit(limit))
    return result.scalars().all()