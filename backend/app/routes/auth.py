from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.deps import SessionDep
from app.model_data import TokenCreate, TokenData, UserPublic, UserCreate
from app.crud.user_crud import get_user_by_name_db
from app.secret import verify_passwd_hash, create_access_token
from app.config import settings
from app.crud.user_crud import create_user_db

auto_route = APIRouter(prefix="/auth", tags=["auth"])


@auto_route.post("/login")
async def generate_user_token(
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> TokenCreate:
    user = await get_user_by_name_db(session, form_data.username)
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User login wasn't found")

    if not verify_passwd_hash(form_data.password, user.hashed_password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Wrong login or password")

    access_token = create_access_token(
        # UserToken(login=form_data.username),
        TokenData(user_id=user.id),
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return TokenCreate(access_token=access_token, token_type="bearer")


@auto_route.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(session: SessionDep, user_create: UserCreate) -> UserPublic:
    user = await create_user_db(session, user_create)
    return UserPublic.model_validate(user, from_attributes=True)
