from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.controllers.admin.create_user import create_user_handler
from app.controllers.admin.delete_user import delete_user_handler
from app.controllers.admin.list_all_users import list_users_handler
from app.controllers.admin.update_user import update_user_handler
from app.middleware.verify_jwt import verify_access_token
from app.middleware.verify_roles import verify_user_role
from app.routers.auth_routes import oauth2_scheme
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

ALLOWED_ROLES = ["admin"]


@router.get("")
async def root() -> dict:
    return {"message": "Admin Routes for user management"}


@router.post("/add-user")
async def add_user(
        user: UserCreate,
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(get_session)
):
    decoded_access_token = verify_access_token(token)
    verify_user_role(decoded_access_token, ALLOWED_ROLES)
    new_user = await create_user_handler(user, session)
    return new_user


@router.get("/get-all-users", response_model=List[UserRead])
async def get_all_users(
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(get_session)
) -> list:
    decoded_access_token = verify_access_token(token)
    verify_user_role(decoded_access_token, ALLOWED_ROLES)
    all_users = await list_users_handler(session)
    return all_users


@router.put("/update-user/{user_id}")
async def update_user(
        user_id: int,
        update_info: UserUpdate,
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(get_session)
) -> dict:
    decoded_access_token = verify_access_token(token)
    verify_user_role(decoded_access_token, ALLOWED_ROLES)
    update_user_info = await update_user_handler(user_id, update_info, session)
    return update_user_info


@router.delete("/delete-user/{user_id}")
async def delete_user(
        user_id: int,
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(get_session)
) -> dict:
    decoded_access_token = verify_access_token(token)
    verify_user_role(decoded_access_token, ALLOWED_ROLES)
    delete_result = await delete_user_handler(user_id, session)
    return delete_result
