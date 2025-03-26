from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


async def list_users_handler(session: AsyncSession):
    try:
        stmt = select(User).order_by(User.id.asc())
        result = await session.execute(stmt)
        all_users = result.scalars().all()

        if not all_users:
            raise HTTPException(status_code=404, detail="No users found")

        return all_users

    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
