from fastapi import APIRouter, status

from app.deps import SessionDep, VideoDep

from app.model_data import Video, VideoCreate, VideoUpdate
from app.crud.video_crud import create_video_db, update_video_db

video_route = APIRouter(prefix="/video", tags=["video"])


@video_route.get("/{id}")
async def get_video(video: VideoDep) -> Video:
    return Video.model_validate(video, from_attributes=True)


@video_route.post("/", status_code=status.HTTP_201_CREATED)
async def create_video(session: SessionDep, video_create: VideoCreate) -> Video:
    video = await create_video_db(session, video_create)
    return Video.model_validate(video, from_attributes=True)


@video_route.patch("/{id}")
async def update_video(
    session: SessionDep, video: VideoDep, video_update: VideoUpdate
) -> Video:
    video = await update_video_db(session, video, video_update)
    return Video.model_validate(video, from_attributes=True)


@video_route.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_video(session: SessionDep, video: VideoDep) -> None:
    await session.delete(video)
    await session.commit()
