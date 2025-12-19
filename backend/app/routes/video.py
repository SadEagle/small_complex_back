from fastapi import APIRouter, HTTPException, status

from app.deps import SessionDep, VideoDep, UserDep

from app.model_data import Video, VideoCreate, VideoUpdate, VideoList
from app.crud.video_crud import create_video_db, get_video_list_db, update_video_db

video_route = APIRouter(prefix="/video", tags=["video"])


@video_route.get("/{id}")
async def get_video(video: VideoDep, user: UserDep) -> Video:
    if user.id != video.user_id:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, "Current video doen't belong to user"
        )
    return Video.model_validate(video, from_attributes=True)


@video_route.get("/")
async def get_user_video_list(session: SessionDep, user: UserDep) -> list[Video]:
    video_list = await get_video_list_db(session, user.id)
    return VideoList.validate_python(video_list, from_attributes=True)


@video_route.post("/", status_code=status.HTTP_201_CREATED)
async def create_video(
    session: SessionDep, video_create: VideoCreate, user: UserDep
) -> Video:
    video = await create_video_db(session, video_create, user.id)
    return Video.model_validate(video, from_attributes=True)


@video_route.patch("/{id}")
async def update_video(
    session: SessionDep, video: VideoDep, video_update: VideoUpdate, user: UserDep
) -> Video:
    if user.id != video.user_id:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, "Current video doen't belong to user"
        )
    video = await update_video_db(session, video, video_update)
    return Video.model_validate(video, from_attributes=True)


@video_route.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_video(session: SessionDep, video: VideoDep, user: UserDep) -> None:
    if user.id != video.user_id:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, "Current video doen't belong to user"
        )
    await session.delete(video)
    await session.commit()
