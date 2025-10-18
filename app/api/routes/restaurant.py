from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import restaurant_crud
from app.deps import get_db
from pydantic import BaseModel
from app.models.restaurant import AreaEnum

router = APIRouter()

class CreateRestaurantRequest(BaseModel):
    restaurant_name: str
    area: AreaEnum


@router.post("/", response_model=dict)
async def create_restaurant(data: CreateRestaurantRequest, db: AsyncSession = Depends(get_db)):
    restaurant = await restaurant_crud.create_restaurant(db, data.restaurant_name, data.area)
    return {"restaurant_id": restaurant.restaurant_id, "name": restaurant.restaurant_name}


@router.get("/{restaurant_id}")
async def get_restaurant(restaurant_id: str, db: AsyncSession = Depends(get_db)):
    restaurant = await restaurant_crud.get_restaurant(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant


@router.get("/")
async def list_restaurants(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1), db: AsyncSession = Depends(get_db)):
    restaurants = await restaurant_crud.list_restaurants(db, skip, limit)
    return restaurants
