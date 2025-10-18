from fastapi import Depends, HTTPException
from httpx import AsyncClient
from google.oauth2 import id_token
from google.auth.transport import requests
from app.config import settings
from app.schemas import customer_crud
from app.models.customer import Customer
from app.deps import get_db
from sqlalchemy.ext.asyncio import AsyncSession


# Your Google OAuth client ID
GOOGLE_CLIENT_ID = "930013363401-1g7t4rqlvanqpjl9sv0hp34u9pnbqtfk.apps.googleusercontent.com"


async def get_google_user_info(token: str):
    try:
        # Verify the token and get user info
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
        
        # Verify iss claim
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')
            
        return idinfo
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid Google token: {str(e)}")


async def login_or_create_user(token: str, db: AsyncSession = Depends(get_db)) -> Customer:
    info = await get_google_user_info(token)
    google_id = info.get("sub")
    if not google_id:
        raise HTTPException(status_code=400, detail="Google ID not found")
    
    user = await customer_crud.get_customer_by_google_id(db, google_id)
    if not user:
        name = info.get("name", "Unknown")
        user = await customer_crud.create_customer(db, name=name, google_id=google_id, age=None)
    return user