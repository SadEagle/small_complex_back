from datetime import datetime
from typing import Annotated, TypeAlias
from pydantic import Field, BaseModel, JsonValue, TypeAdapter


VideoList = TypeAdapter(list["Video"])

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


class VideoCreate(VideoBase):
    pass


class VideoUpdate(BaseModel):
    video_path: str | None = None


class AnalyticsBase(BaseModel):
    bbox_data: JsonValue
    video_id: int


class Analytics(AnalyticsBase):
    id: int


class AnalyticsCreate(AnalyticsBase):
    pass


# May be needed when will add new columns
class AnalyticsUpdate(BaseModel):
    bbox_data: JsonValue | None = None
    video_id: int


class TokenCreate(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int
