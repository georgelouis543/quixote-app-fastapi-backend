import os

import jwt
from dotenv import load_dotenv
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.controllers.auth.tokens_controller import create_access_token
from app.models.user import User

load_dotenv()

ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
REFRESH_TOKEN_SECRET = os.getenv("REFRESH_TOKEN_SECRET")
ALGORITHM = os.getenv("ALGORITHM")


async def handle_refresh_token(request: Request, session: AsyncSession):
    # Retrieve the refresh token from cookie
    refresh_token = request.cookies.get('jwt')

    if not refresh_token:
        raise HTTPException(401, detail="Could not authorize User!")

    print(refresh_token)
    print(request.headers)

    # Fetch user from the database
    stmt = select(User).where(User.refresh_token == refresh_token)
    result = await session.execute(stmt)
    found_user = result.scalar_one_or_none()

    if not found_user:
        raise HTTPException(403, detail="Forbidden!")

    # Decode the refresh token
    try:
        decoded_refresh_token = jwt.decode(
            refresh_token,
            REFRESH_TOKEN_SECRET,
            algorithms=ALGORITHM,
            verify=True
        )
        print(decoded_refresh_token)

    except Exception as e:
        print(f'Exited with Exception: {e}')
        raise HTTPException(403, detail="Forbidden!")

    # Validate the token email with the user email
    if decoded_refresh_token["user_email"] == found_user.user_email:
        access_token = create_access_token(
            found_user.user_email,
            found_user.user_name,
            found_user.role
        )
        data_to_return = {
            "access_token": access_token,
            "token_type": "Bearer",
            "user_email": found_user.user_email,
            "user_role": found_user.role
        }
        response = JSONResponse(content=data_to_return)
        return response

    else:
        raise HTTPException(403, detail="Forbidden")
