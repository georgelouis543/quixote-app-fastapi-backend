from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.controllers.auth.create_user import create_user_handler
from app.models.user import User
from app.schemas.user import UserBase

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.get("")
async def root() -> dict:
    return {"message": "Auth Routes"}


@router.post("/add-user")
async def add_user(user: UserBase, session: AsyncSession = Depends(get_session)):
    new_user = await create_user_handler(user, session)
    return new_user
