from fastapi import APIRouter, HTTPException
from starlette.responses import RedirectResponse
from app.schemas.url import UrlCreate, UrlInfo
from app.services.url_service import create_url, get_url, increment_visit

router = APIRouter()

@router.post("/urls", response_model=UrlInfo)
async def create_short_url(payload: UrlCreate):
    return create_url(payload)

@router.get("/u/{short_path}")
async def redirect_url(short_path: str):
    url = get_url(short_path)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    increment_visit(short_path)
    return RedirectResponse(url.original_url)

@router.get("/urls/{short_path}/info", response_model=UrlInfo)
async def url_info(short_path: str):
    url = get_url(short_path)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    return url
