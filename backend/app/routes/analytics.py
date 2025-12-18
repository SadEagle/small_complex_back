from fastapi import APIRouter, status

from app.deps import SessionDep, AnalyticsDep
from app.model_data import Analytics, AnalyticsCreate, AnalyticsUpdate
from app.crud.analytics_crud import create_analytics_db, update_analytics_db

analytics_route = APIRouter(prefix="/analytics", tags=["analytics"])


@analytics_route.get("/{id}")
async def get_analytics(analytics: AnalyticsDep) -> Analytics:
    return Analytics.model_validate(analytics, from_attributes=True)


@analytics_route.post("/", status_code=status.HTTP_201_CREATED)
async def create_analytics(
    session: SessionDep, analytics_create: AnalyticsCreate
) -> Analytics:
    analytics = await create_analytics_db(session, analytics_create)
    return Analytics.model_validate(analytics, from_attributes=True)


@analytics_route.patch("/{id}")
async def update_analytics(
    session: SessionDep, analytics: AnalyticsDep, analytics_update: AnalyticsUpdate
) -> Analytics:
    analytics = await update_analytics_db(session, analytics, analytics_update)
    return Analytics.model_validate(analytics, from_attributes=True)


@analytics_route.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_analytics(session: SessionDep, analytics: AnalyticsDep) -> None:
    await session.delete(analytics)
    await session.commit()
