from fastapi import APIRouter

from app.controllers.newsletters.platform_analytics import get_all_analytics

router = APIRouter(
    prefix="/newsletter-analytics",
    tags=["Newsletter Analytics"]
)


@router.get("/")
async def root() -> dict:
    return {
        "message": "You can Export all Newsletter related Analytics here"
    }


@router.get("/get-platform-analytics")
async def get_platform_analytics(newsletter_id: str, auth_token: str) -> list:
    analytics_data = await get_all_analytics(newsletter_id, auth_token)
    return analytics_data
