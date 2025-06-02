from fastapi import HTTPException
from sqlalchemy import select, or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserUpdate


async def update_user_handler(
        user_id: int,
        update_info: UserUpdate,
        session: AsyncSession
) -> dict:
    try:
        user_id = user_id
        update_info = update_info

        get_existing_user_stmt = select(User).where(User.id == user_id)
        exec_get_existing_user = await session.execute(get_existing_user_stmt)
        existing_user = exec_get_existing_user.scalar_one_or_none()

        if not existing_user:
            raise HTTPException(status_code=400, detail="User not found!")

        if update_info.user_email or update_info.user_name:
            find_duplicate_user_stmt = select(User).where(
                or_(
                    User.user_email == update_info.user_email,
                    User.user_name == update_info.user_name
                )
            )
            exec_find_user_stmt = await session.execute(find_duplicate_user_stmt)
            found_duplicate = exec_find_user_stmt.scalars().first()  # Checking if at least one match exists

            if found_duplicate and found_duplicate.id != user_id:
                raise HTTPException(
                    status_code=409,
                    detail="Another user with the same email or username already exists."
                )

        # below check is to ensure no unnecessary updates are made (checking if the same data is being re-saved)
        if (
                (update_info.user_email is None or update_info.user_email == existing_user.user_email) and
                (update_info.user_name is None or update_info.user_name == existing_user.user_name) and
                (update_info.role is None or update_info.role == existing_user.role)
        ):
            raise HTTPException(status_code=400, detail="No changes detected!")

        if update_info.user_email is not None and update_info.user_email != existing_user.user_email:
            existing_user.user_email = update_info.user_email

        if update_info.user_name is not None and update_info.user_name != existing_user.user_name:
            existing_user.user_name = update_info.user_name

        if update_info.role is not None and update_info.role != existing_user.role:
            existing_user.role = update_info.role

        await session.commit()
        await session.refresh(existing_user)

        return {
            "message": f"User with ID {user_id} successfully updated!"
        }

    except HTTPException as e:
        raise e

    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"An Unknown error occurred: {str(e)}")


