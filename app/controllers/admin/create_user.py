import logging

from fastapi import HTTPException
from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate


async def create_user_handler(user: UserCreate, session: AsyncSession):
    stmt = insert(User).values(user_email=user.user_email,
                               user_name=user.user_name,
                               role=user.role).returning(User)
    try:
        result = await session.execute(stmt)
        new_user = result.scalar_one_or_none()

        if not new_user:
            raise HTTPException(status_code=400, detail="Failed to create user")

        await session.commit()
        logging.info(f"Created new user with ID: {new_user.id} and email: {new_user.user_email}")
        return new_user

    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
