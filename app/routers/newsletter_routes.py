from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse

from app.config.database import get_session
from app.controllers.newsletters.excel_generator_for_platform_analytics import dataframe_to_excel_stream
from app.controllers.newsletters.platform_analytics import get_all_analytics
from app.controllers.newsletters.save_analytics import save_analytics_data_handler
from app.helpers.dist_filter_by_time import TimeWindow
from app.middleware.verify_jwt import verify_access_token
from app.middleware.verify_roles import verify_user_role
from app.routers.auth_routes import oauth2_scheme

router = APIRouter(
    prefix="/newsletter-analytics",
    tags=["newsletter-analytics"]
)

ALLOWED_ROLES = ["admin"]


@router.get("")
async def root() -> dict:
    return {
        "message": "You can Export all Newsletter related Analytics here"
    }


@router.get("/get-platform-analytics")
async def get_platform_analytics(
        newsletter_id: str,
        auth_token: str,
        date_range: TimeWindow = Query("7d", description="7d, 1m, 3m or 6m"),
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(get_session)
) -> StreamingResponse:
    decoded_access_token = verify_access_token(token)
    verify_user_role(decoded_access_token, ALLOWED_ROLES)
    analytics_data = await get_all_analytics(newsletter_id, auth_token, date_range)
    xlsx_stream = dataframe_to_excel_stream(analytics_data)
    filename = f"{newsletter_id}_analytics.xlsx"
    return StreamingResponse(
        xlsx_stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )
