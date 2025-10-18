from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.google_oauth import get_google_user_info
from app.auth.jwt_handler import create_access_token, create_refresh_token
from app.schemas import customer_crud
from app.deps import get_db
from pydantic import BaseModel

router = APIRouter()

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class GoogleToken(BaseModel):
    token: str


@router.post("/signup", response_model=TokenResponse)
async def google_signup(data: GoogleToken, db: AsyncSession = Depends(get_db)):
    info = await get_google_user_info(data.token)
    google_id = info.get("sub")
    name = info.get("name")
    if not google_id:
        raise HTTPException(status_code=400, detail="Invalid Google token")

    user = await customer_crud.get_customer_by_google_id(db, google_id)
    if user:
        raise HTTPException(status_code=400, detail="User already exists")

    user = await customer_crud.create_customer(db, name=name, google_id=google_id, age=None)
    access_token = create_access_token(subject=user.google_id)
    refresh_token = create_refresh_token(subject=user.google_id)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/login", response_model=TokenResponse)
async def google_login(data: GoogleToken, db: AsyncSession = Depends(get_db)):
    print(data.token)
    info = await get_google_user_info(data.token)
    google_id = info.get("sub")
    if not google_id:
        raise HTTPException(status_code=400, detail="Invalid Google token")

    user = await customer_crud.get_customer_by_google_id(db, google_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found. Please sign up first.")

    access_token = create_access_token(subject=user.google_id)
    refresh_token = create_refresh_token(subject=user.google_id)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)

# Utility endpoint: decode Google token and return user info (for testing in Postman)
@router.post("/google-token-info")
async def google_token_info(data: GoogleToken):
    info = await get_google_user_info(data.token)
    return info
