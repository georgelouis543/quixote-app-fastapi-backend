import logging

from fastapi import HTTPException
from sqlalchemy import insert, select, or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate


async def create_user_handler(user: UserCreate, session: AsyncSession):
    # Checking for duplicates (both username and email must be unique)
    find_duplicate_user_stmt = select(User).where(
        or_(
            User.user_email == user.user_email,
            User.user_name == user.user_name
        )
    )
    exec_find_user_stmt = await session.execute(find_duplicate_user_stmt)
    found_duplicate = exec_find_user_stmt.scalars().first()  # Checking if at least one match exists

    if found_duplicate:
        raise HTTPException(status_code=409, detail="User already exists!")

    # insert new user
    insert_user_stmt = insert(User).values(user_email=user.user_email,
                                           user_name=user.user_name,
                                           role=user.role).returning(User)
    try:
        exec_insert_user_stmt = await session.execute(insert_user_stmt)
        new_user = exec_insert_user_stmt.scalar_one_or_none()

        if not new_user:
            raise HTTPException(status_code=400, detail="Failed to create user")

        await session.commit()
        logging.info(f"Created new user with ID: {new_user.id} and email: {new_user.user_email}")
        return new_user

    # Adding Error boundaries below
    except HTTPException as e:
        raise e

    except SQLAlchemyError as e:
        await session.rollback()
        logging.error(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    except Exception as e:
        await session.rollback()
        logging.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
