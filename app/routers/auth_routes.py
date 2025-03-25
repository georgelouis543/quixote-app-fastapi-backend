from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.controllers.auth.login_controller import handle_login
from app.middleware.verify_gjwt import verify_google_token
from app.schemas.token import TokenResponse

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.get("")
async def root() -> dict:
    return {"message": "Auth Routes"}


@router.get("/login", response_model=TokenResponse)
async def login(
        google_token_verification_result: dict = Depends(verify_google_token),
        session: AsyncSession = Depends(get_session)
):
    response = await handle_login(google_token_verification_result["email"], session)
    return response
