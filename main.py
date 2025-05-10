from fastapi import FastAPI, Response, Request  # type: ignore
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from app.routers import router as api_router
from app.core.config import settings
from app.core.rate_limiter import limiter, rate_limit_exceeded_handler

app = FastAPI(title="URL Shortener")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modify in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure rate limiting 
if settings.rate_limit_enabled:
    from slowapi.middleware import SlowAPIMiddleware
    # Register limiter instance with the app
    app.state.limiter = limiter
    # Apply middleware for request processing
    app.add_middleware(SlowAPIMiddleware)
    # Register custom handler for better error messages
    app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

@app.middleware("http")
async def add_rate_limit_headers(request: Request, call_next):
    """Middleware to propagate rate limit information via HTTP headers"""
    response = await call_next(request)
    
    # Transfer rate limit data from request state to response headers
    if hasattr(request.state, "rate_limit_headers"):
        for key, value in request.state.rate_limit_headers.items():
            response.headers[key] = str(value)
    
    return response

app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "URL Shortener Service is running."}

@app.get("/favicon.ico", include_in_schema=False)  # handle browser favicon requests
async def favicon():
    return Response(status_code=204)

if __name__ == "__main__":
    import uvicorn  # type: ignore
    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=True)
