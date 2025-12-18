from typing import Annotated, AsyncGenerator
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import async_engine
from app.model_db import AnalyticsDB, UserDB, VideoDB


async def create_session() -> AsyncGenerator[AsyncSession]:
    # WARN: async expects no expiration
    # Ref: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#preventing-implicit-io-when-using-asyncsession
    async with AsyncSession(async_engine, expire_on_commit=False) as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(create_session)]


async def get_user_obj(session: SessionDep, id: int) -> UserDB:
    user = await session.get(UserDB, id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User wasn't found"
        )
    return user


UserDep = Annotated[UserDB, Depends(get_user_obj)]


async def get_video_obj(session: SessionDep, id: int) -> VideoDB:
    video = await session.get(VideoDB, id)
    if video is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Video id={id} wasn't found"
        )
    return video


VideoDep = Annotated[VideoDB, Depends(get_video_obj)]


async def get_analytics_obj(session: SessionDep, id) -> AnalyticsDB:
    analytics = await session.get(AnalyticsDB, id)
    if analytics is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analytics id={id} wasn't found",
        )
    return analytics


AnalyticsDep = Annotated[AnalyticsDB, Depends(get_analytics_obj)]
