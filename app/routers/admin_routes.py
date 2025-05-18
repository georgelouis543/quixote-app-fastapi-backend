from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.controllers.admin.create_user import create_user_handler
from app.controllers.admin.list_all_users import list_users_handler
from app.middleware.verify_jwt import verify_access_token
from app.middleware.verify_roles import verify_user_role
from app.routers.auth_routes import oauth2_scheme
from app.schemas.user import UserCreate, UserRead

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)


@router.get("")
async def root() -> dict:
    return {"message": "Admin Routes for user management"}


@router.post("/add-user")
async def add_user(user: UserCreate,
                   token: str = Depends(oauth2_scheme),
                   session: AsyncSession = Depends(get_session)):
    decoded_access_token = verify_access_token(token)
    verify_user_role(decoded_access_token, ["admin"])
    new_user = await create_user_handler(user, session)
    return new_user


@router.get("/get-all-users", response_model=List[UserRead])
async def get_all_users(token: str = Depends(oauth2_scheme),
                        session: AsyncSession = Depends(get_session)
                        ) -> list:
    decoded_access_token = verify_access_token(token)
    verify_user_role(decoded_access_token, ["admin"])
    all_users = await list_users_handler(session)
    return all_users
