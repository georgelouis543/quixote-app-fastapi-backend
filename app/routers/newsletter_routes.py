from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse

from app.config.database import get_session
from app.controllers.newsletters.platform_analytics import get_all_analytics, convert_to_csv_stream
from app.controllers.newsletters.save_analytics import save_analytics_data_handler

router = APIRouter(
    prefix="/newsletter-analytics",
    tags=["newsletter-analytics"]
)


@router.get("")
async def root() -> dict:
    return {
        "message": "You can Export all Newsletter related Analytics here"
    }


@router.get("/get-platform-analytics")
async def get_platform_analytics(newsletter_id: str, auth_token: str,
                                 session: AsyncSession = Depends(get_session)) -> StreamingResponse:
    analytics_data = await get_all_analytics(newsletter_id, auth_token)
    await save_analytics_data_handler(newsletter_id, analytics_data, session)
    csv_stream = convert_to_csv_stream(analytics_data)
    return StreamingResponse(
        csv_stream,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={newsletter_id}_analytics.csv"}
    )
