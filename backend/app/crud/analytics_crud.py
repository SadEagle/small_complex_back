from sqlalchemy.ext.asyncio import AsyncSession

from app.model_db import AnalyticsDB, VideoDB
from app.model_data import AnalyticsCreate, AnalyticsUpdate


async def create_analytics_db(
    session: AsyncSession, video: VideoDB, analytics_create: AnalyticsCreate
) -> AnalyticsDB:
    # TODO: check do i need to set up model_dump("JSON")
    analytics_dict = analytics_create.model_dump(exclude_unset=True)
    analytics = AnalyticsDB(**analytics_dict)

    session.add(analytics)
    await session.commit()
    await session.refresh(analytics)

    # Add analytics_id into video element
    video.analytics_id = analytics.id
    await session.commit()
    return analytics


async def update_analytics_db(
    session: AsyncSession, analytics: AnalyticsDB, analytics_update: AnalyticsUpdate
) -> AnalyticsDB | None:
    update_data = analytics_update.model_dump(exclude_unset=True, exclude_defaults=True)

    for key, value in update_data.items():
        if hasattr(analytics, key):
            setattr(analytics, key, value)

    session.add(analytics)
    await session.commit()
    await session.refresh(analytics)
    return analytics
