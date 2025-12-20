from typing import Sequence
from fastapi import APIRouter, HTTPException, status
from starlette.status import HTTP_204_NO_CONTENT

from app.deps import SessionDep, VideoDep, UserDep

from app.model_data import (
    Video,
    VideoCreate,
    VideoUpdate,
    VideoList,
    Analytics,
    AnalyticsCreate,
    AnalyticsUpdate,
)
from app.crud.video_crud import create_video_db, get_video_list_db, update_video_db
from app.crud.analytics_crud import create_analytics_db, update_analytics_db

video_route = APIRouter(prefix="/video", tags=["video"])


@video_route.post("/", status_code=status.HTTP_201_CREATED)
async def create_video(
    session: SessionDep, video_create: VideoCreate, user: UserDep
) -> Video:
    video = await create_video_db(session, video_create, user.id)
    return Video.model_validate(video, from_attributes=True)


@video_route.get("/all")
async def get_user_video_list(session: SessionDep, user: UserDep) -> Sequence[Video]:
    video_list = list(await get_video_list_db(session, user.id))
    return VideoList.validate_python(video_list, from_attributes=True)


@video_route.get("/{id}")
async def get_video(video: VideoDep, user: UserDep) -> Video:
    if user.id != video.user_id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "Current video doesn't belong to user"
        )
    return Video.model_validate(video, from_attributes=True)


@video_route.patch("/{id}")
async def update_video(
    session: SessionDep, video: VideoDep, video_update: VideoUpdate, user: UserDep
) -> Video:
    if user.id != video.user_id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "Current video doen't belong to user"
        )
    video = await update_video_db(session, video, video_update)
    return Video.model_validate(video, from_attributes=True)


@video_route.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_video(session: SessionDep, video: VideoDep, user: UserDep) -> None:
    if user.id != video.user_id:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, "Current video doesn't belong to user"
        )
    await session.delete(video)
    await session.commit()


# Analytics data
@video_route.get("/{id}/analytics")
async def get_analytics(video: VideoDep, user: UserDep) -> Analytics:
    if video.user_id != user.id:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, "Current video doesn't belong to user"
        )
    if video.analytics_id is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "Current video analytics doesn't exist"
        )
    return Analytics.model_validate(
        (await video.awaitable_attrs.analytics), from_attributes=True
    )


@video_route.post("/{id}/analytics", status_code=status.HTTP_201_CREATED)
async def create_analytics(
    session: SessionDep,
    video: VideoDep,
    user: UserDep,
    analytics_create: AnalyticsCreate,
) -> Analytics:
    if video.user_id != user.id:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, "Current video doesn't belong to user"
        )
    analytics = await create_analytics_db(session, video, analytics_create)
    return Analytics.model_validate(analytics, from_attributes=True)


@video_route.patch("/{id}/analytics")
async def update_analytics(
    session: SessionDep,
    video: VideoDep,
    analytics_update: AnalyticsUpdate,
    user: UserDep,
) -> Analytics:
    if video.user_id != user.id:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, "Current video doesn't belong to user"
        )
    analytics = await update_analytics_db(
        session, (await video.awaitable_attrs.analytics), analytics_update
    )
    return Analytics.model_validate(analytics, from_attributes=True)
