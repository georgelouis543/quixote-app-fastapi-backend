from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from app.controllers.auth.tokens_controller import create_refresh_token, create_access_token
from app.models.user import User


async def handle_login(user_email: str, session: AsyncSession):
    try:
        # Fetch user from the database using select
        stmt = select(User).where(User.user_email == user_email)
        result = await session.execute(stmt)
        found_user = result.scalar_one_or_none()

        if not found_user:
            raise HTTPException(status_code=401, detail="Unauthorized!")

        # Generate tokens
        refresh_token = create_refresh_token(
            found_user.user_email,
            found_user.user_name,
            found_user.role
        )

        access_token = create_access_token(
            found_user.user_email,
            found_user.user_name,
            found_user.role
        )

        # Update refresh token in the database
        found_user.refresh_token = refresh_token
        await session.commit()

        # Prepare response data
        data_to_return = {
            "access_token": access_token,
            "token_type": "Bearer",
            "user_email": found_user.user_email,
            "user_role": found_user.role
        }

        # Set JWT token as HTTP-only cookie
        response = JSONResponse(content=data_to_return)
        response.set_cookie(
            key="jwt",
            value=refresh_token,
            expires=3600,
            httponly=True,
            samesite="none",
            secure=True
        )

        return response

    except HTTPException as e:
        print(f"Exited with Exception {e}")
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error!")
