from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.controllers.admin.create_user import create_user_handler
from app.controllers.admin.list_all_users import list_users_handler
from app.schemas.user import UserCreate, UserRead

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)


@router.get("")
async def root() -> dict:
    return {"message": "Admin Routes for user management"}


@router.post("/add-user")
async def add_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    new_user = await create_user_handler(user, session)
    return new_user


@router.get("/get-all-users", response_model=List[UserRead])
async def get_all_users(session: AsyncSession = Depends(get_session)) -> list:
    all_users = await list_users_handler(session)
    return all_users
