from fastapi import APIRouter, status

from app.deps import SessionDep, UserDep

from app.model_data import UserPublic, UserUpdate
from app.crud.user_crud import update_user_db

user_route = APIRouter(prefix="/user", tags=["user"])


@user_route.get("/")
async def get_own_user(user: UserDep) -> UserPublic:
    return UserPublic.model_validate(user, from_attributes=True)


@user_route.patch("/")
async def update_own_user(
    session: SessionDep, user: UserDep, user_update: UserUpdate
) -> UserPublic:
    user = await update_user_db(session, user, user_update)
    return UserPublic.model_validate(user, from_attributes=True)


@user_route.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_own_user(session: SessionDep, user: UserDep) -> None:
    await session.delete(user)
    await session.commit()
