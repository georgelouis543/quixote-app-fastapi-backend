from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.models.user import User


async def handle_logout(request: Request, session: AsyncSession):
    # Get the refresh token from cookies
    refresh_token = request.cookies.get("jwt")

    if not refresh_token:
        raise HTTPException(204, detail="Could not authorize User!")

    # Fetch user from database
    stmt = select(User).where(User.refresh_token == refresh_token)
    result = await session.execute(stmt)
    found_user = result.scalar_one_or_none()

    if not found_user:
        raise HTTPException(401, detail="Could not authorize User!")

    # The following try-catch is to handle DB Errors (if any)
    try:
        # Clear refresh token in database
        found_user.refresh_token = ""
        await session.commit()

        # Create response and delete cookie
        response = JSONResponse(content={"message": "Logout success!"},
                                status_code=200)
        response.delete_cookie(
            key="jwt",
            httponly=True,
            samesite='none',
            secure=True
        )
        print("LOGOUT SUCCESS")
        return response

    except Exception as e:
        print(f"Exited with Exception {e}")
        await session.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
