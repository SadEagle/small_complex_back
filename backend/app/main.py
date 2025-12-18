from fastapi import FastAPI, APIRouter

from app.routes.analytics import analytics_route
from app.routes.user import user_route
from app.routes.video import video_route
from app.routes.login import login_route

app_route = APIRouter(prefix="/api")
app_route.include_router(analytics_route)
app_route.include_router(user_route)
app_route.include_router(video_route)
app_route.include_router(login_route)


api = FastAPI()
api.include_router(app_route)
