from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.model_db import UserDB
from app.model_data import UserCreate, UserUpdate
from app.secret import get_passwd_hash


async def get_user_by_name_db(session: AsyncSession, user_login: str) -> UserDB | None:
    statment = select(UserDB).where(UserDB.login == user_login)
    user = await session.scalar(statment)
    return user


async def create_user_db(session: AsyncSession, user_create: UserCreate) -> UserDB:
    # TODO: check do i need to set up model_dump("JSON")
    hashed_password = get_passwd_hash(user_create.password)
    user_date = user_create.model_dump(exclude={"password"})
    user = UserDB(**user_date, hashed_password=hashed_password)

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def update_user_db(
    session: AsyncSession, user: UserDB, user_update: UserUpdate
) -> UserDB:
    update_data = user_update.model_dump(exclude_unset=True, exclude_defaults=True)
    if update_data.get("password") is not None:
        hashed_password = get_passwd_hash(update_data["password"])
        update_data["hashed_password"] = hashed_password
        update_data.pop("password")

    for key, value in update_data.items():
        if hasattr(user, key):
            setattr(user, key, value)

    await session.commit()
    await session.refresh(user)
    return user
