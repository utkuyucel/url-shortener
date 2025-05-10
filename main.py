from fastapi import FastAPI, Response, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from slowapi.errors import RateLimitExceeded

from app.routers import router as api_router
from app.services.url_service import get_url, increment_visit
from app.db.session import get_db
from app.core.config import settings
from app.core.rate_limiter import limiter, rate_limit_exceeded_handler

app = FastAPI(title="URL Shortener")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if settings.rate_limit_enabled:
    from slowapi.middleware import SlowAPIMiddleware
    app.state.limiter = limiter
    app.add_middleware(SlowAPIMiddleware)
    app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

@app.middleware("http")
async def add_rate_limit_headers(request: Request, call_next):
    """Middleware to propagate rate limit information via HTTP headers"""
    response = await call_next(request)
    if hasattr(request.state, "rate_limit_headers"):
        for key, value in request.state.rate_limit_headers.items():
            response.headers[key] = str(value)
    return response

app.include_router(api_router, prefix="/api/v1")

@app.get("/", response_class=Response)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/{short_key}")
async def redirect_url(short_key: str, db: Session = Depends(get_db)):
    url_info = get_url(short_path=short_key)
    if url_info is None:
        raise HTTPException(status_code=404, detail="URL not found")
    increment_visit(short_path=short_key)
    return Response(status_code=307, headers={"Location": str(url_info.original_url)})

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=True)
