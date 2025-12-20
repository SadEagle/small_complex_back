from datetime import datetime
from typing import Annotated, Sequence, TypeAlias
from pydantic import Field, BaseModel, JsonValue, TypeAdapter


VideoList = TypeAdapter(Sequence["Video"])

# Bcrypt may has up to 72 characters passwd
PasswordType: TypeAlias = Annotated[str, Field(max_length=72)]


class UserBase(BaseModel):
    login: str


class UserPublic(UserBase):
    id: int
    created_at: datetime


class UserCreate(UserBase):
    password: PasswordType


class UserUpdate(BaseModel):
    login: str | None
    password: PasswordType | None


class VideoBase(BaseModel):
    video_path: str


class Video(VideoBase):
    id: int
    analytics_id: int


class VideoCreate(VideoBase):
    pass


class VideoUpdate(BaseModel):
    video_path: str | None = None


class AnalyticsBase(BaseModel):
    bbox_data: JsonValue


class Analytics(AnalyticsBase):
    id: int


class AnalyticsCreate(AnalyticsBase):
    pass


# May be needed when will add new columns
class AnalyticsUpdate(BaseModel):
    bbox_data: JsonValue | None = None


class TokenCreate(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int


# NOTE: Need if TypeAdapter was defined before inner classes
# Ref: https://docs.pydantic.dev/2.11/errors/usage_errors/#class-not-fully-defined
VideoList.rebuild()
