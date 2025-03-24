from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.get("")
async def root() -> dict:
    return {"message": "Auth Routes"}
