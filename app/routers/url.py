from fastapi import APIRouter, HTTPException, Request, status
from starlette.responses import RedirectResponse, Response
from app.schemas.url import UrlCreate, UrlInfo
from app.services.url_service import create_url, get_url, increment_visit, get_all_urls, delete_all_urls
from app.core.config import settings
from typing import List
from app.core.rate_limiter import limiter

router = APIRouter()

@router.post("/url/shorten", response_model=UrlInfo)
@limiter.limit(settings.rate_limit_default_limits["create_url"])
async def create_short_url(request: Request, payload: UrlCreate):
    """Create a new shortened URL"""
    return create_url(payload)

@router.get("/u/{short_path}")
@limiter.limit(settings.rate_limit_default_limits["redirect_url"])
async def redirect_url(request: Request, short_path: str):
    """Handle URL redirection"""
    url = get_url(short_path)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    increment_visit(short_path)
    return RedirectResponse(url.original_url)

@router.get("/urls/{short_path}/info", response_model=UrlInfo)
async def url_info(short_path: str):
    """Fetch metadata for a shortened URL"""
    url = get_url(short_path)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    return url

@router.get("/urls", response_model=List[UrlInfo])
async def list_all_urls():
    """Fetch all shortened URLs"""
    return get_all_urls()

@router.delete("/urls", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit(settings.rate_limit_default_limits["delete_url"])
async def remove_all_urls(request: Request):
    """Delete all shortened URLs"""
    delete_all_urls()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
