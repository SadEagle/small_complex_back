from fastapi import FastAPI, APIRouter


app_api = APIRouter(prefix="/api")


api = FastAPI()
api.include_router(app_api)
