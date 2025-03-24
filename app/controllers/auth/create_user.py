from fastapi import HTTPException
from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserBase


async def create_user_handler(user: UserBase, session: AsyncSession):
    stmt = insert(User).values(user_email=user.user_email,
                               user_name=user.user_email,
                               role=user.role).returning(User)
    try:
        result = await session.execute(stmt)
        new_user = result.scalar_one_or_none()

        if not new_user:
            raise HTTPException(status_code=400, detail="Failed to create product")

        await session.commit()
        return new_user

    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
