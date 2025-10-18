from app.models import AsyncSessionLocal
from fastapi import Depends

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
