from fastapi import APIRouter, status

from app.deps import SessionDep, UserDep

from app.model_data import UserPublic, UserCreate, UserUpdate, Video, VideoList
from app.crud.user_crud import create_user_db, update_user_db

user_route = APIRouter(prefix="/user", tags=["user"])


@user_route.get("/{id}/videos")
async def get_user_video_list(session: SessionDep, id: int) -> list[Video]:
    video_list = await get_user_video_list(session, id)
    return VideoList.validate_python(video_list, from_attributes=True)


@user_route.get("/{id}")
async def get_user(user: UserDep) -> UserPublic:
    return UserPublic.model_validate(user, from_attributes=True)


# TODO: add hashed_passwd field instead of passwd
# @user_route.post("/", status_code=status.HTTP_201_CREATED)
# async def create_user(session: SessionDep, user_create: UserCreate) -> UserPublic:
#     user = await create_user_db(session, user_create)
#     return UserPublic.model_validate(user, from_attributes=True)


@user_route.patch("/{id}")
async def update_analytics(
    session: SessionDep, user: UserDep, user_update: UserUpdate
) -> UserPublic:
    user = await update_user_db(session, user, user_update)
    return UserPublic.model_validate(user, from_attributes=True)


@user_route.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(session: SessionDep, user: UserDep) -> None:
    await session.delete(user)
    await session.commit()
