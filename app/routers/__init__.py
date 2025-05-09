from fastapi import APIRouter  # type: ignore

from .url import router as url_router

router = APIRouter()
router.include_router(url_router, prefix="", tags=["url"])
