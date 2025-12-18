from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.model_db import UserDB
from app.model_data import UserCreate, UserUpdate


async def get_user_by_name_db(session: AsyncSession, user_login: str) -> UserDB | None:
    statment = select(UserDB).where(UserDB.login == user_login)
    user = await session.scalar(statment)
    return user


async def create_user_db(session: AsyncSession, user_create: UserCreate) -> UserDB:
    # TODO: check do i need to set up model_dump("JSON")
    user_dict = user_create.model_dump(exclude_unset=True)
    user = UserDB(**user_dict)

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def update_user_db(
    session: AsyncSession, user: UserDB, user_update: UserUpdate
) -> UserDB:
    update_data = user_update.model_dump(exclude_unset=True, exclude_defaults=True)

    for key, value in update_data.items():
        if hasattr(user, key):
            setattr(user, key, value)

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
