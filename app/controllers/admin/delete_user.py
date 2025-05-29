import logging

from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


async def delete_user_handler(
        user_id: int,
        session: AsyncSession
) -> dict:
    try:
        find_user_stmt = select(User).where(User.id == user_id)
        find_user_stmt_execute = await session.execute(find_user_stmt)
        found_user = find_user_stmt_execute.scalar_one_or_none()

        if not found_user:
            raise HTTPException(status_code=404, detail="user not found!")

        delete_stmt = delete(User).where(User.id == user_id)
        await session.execute(delete_stmt)
        await session.commit()

        logging.info(f"Successfully deleted user with id: {user_id}")
        return {
            "message": f"User with ID {user_id} deleted successfully!"
        }

    except HTTPException as e:
        raise e

    except SQLAlchemyError as e:
        logging.error(f"There was a database error deleting user with ID {user_id} | Error: {e}")
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    except Exception as e:
        logging.error(f"There was an error deleting user with ID {user_id} | Error: {e}")
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")






