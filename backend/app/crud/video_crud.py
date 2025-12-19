from typing import Sequence

from pydantic import TypeAdapter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.model_db import VideoDB
from app.model_data import Video, VideoCreate, VideoUpdate


ListVideo = TypeAdapter(list[Video])


async def get_video_list_db(session: AsyncSession, user_id: int) -> Sequence[VideoDB]:
    statement = select(VideoDB).where(VideoDB.user_id == user_id)
    user_videos_list = (await session.scalars(statement)).all()
    return user_videos_list


async def create_video_db(
    session: AsyncSession, video_create: VideoCreate, user_id: int
) -> VideoDB:
    # TODO: check do i need to set up model_dump("JSON")
    video_dict = video_create.model_dump(exclude_unset=True)
    video = VideoDB(**video_dict, user_id=user_id)

    session.add(video)
    await session.commit()
    await session.refresh(video)
    return video


async def update_video_db(
    session: AsyncSession, video: VideoDB, video_update: VideoUpdate
) -> VideoDB:
    update_data = video_update.model_dump(exclude_unset=True, exclude_defaults=True)

    for key, value in update_data.items():
        if hasattr(video, key):
            setattr(video, key, value)

    session.add(video)
    await session.commit()
    await session.refresh(video)
    return video
