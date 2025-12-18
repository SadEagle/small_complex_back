from datetime import datetime
from pydantic import BaseModel, JsonValue, TypeAdapter


VideoList = TypeAdapter(list["Video"])


class UserBase(BaseModel):
    login: str
    created_at: datetime


class UserPublic(UserBase):
    id: int


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    login: str | None
    password: str | None


class VideoBase(BaseModel):
    video_path: str
    user_id: int


class Video(VideoBase):
    id: int


class VideoCreate(VideoBase):
    pass


class VideoUpdate(BaseModel):
    video_path: str | None = None
    user_id: int | None = None


class AnalyticsBase(BaseModel):
    bbox_data: JsonValue
    video_id: int


class Analytics(AnalyticsBase):
    id: int


class AnalyticsCreate(AnalyticsBase):
    pass


# May be needed when will add new columns
class AnalyticsUpdate(BaseModel):
    id: int
    bbox_data: JsonValue | None = None
    video_id: int


class TokenCreate(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int
