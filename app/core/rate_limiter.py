from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.core.config import settings

# Select storage backend based on configuration
if settings.rate_limit_storage_uri:
    from slowapi.storage import RedisStorage
    import redis
    
    # Connect to Redis 
    redis_client = redis.from_url(settings.rate_limit_storage_uri)
    storage = RedisStorage(redis_client)
    
    # Initialize with Redis backend for distributed deployments
    limiter = Limiter(
        key_func=get_remote_address,
        storage=storage,
        default_limits=[settings.rate_limit_default_limits["general"]],
        strategy="fixed-window", # moving-window is another option
        key_prefix=settings.rate_limit_key_prefix
    )
else:
    # Fallback to memory storage for development/testing
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=[settings.rate_limit_default_limits["general"]],
        key_prefix=settings.rate_limit_key_prefix
    )

async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    """Handle rate limit exceeded exceptions with a standardized response format"""
    
    # Build response with detailed information
    response = JSONResponse(
        status_code=429,
        content={
            "error": "Rate limit exceeded",
            "detail": str(exc),
            "retry_after": exc.retry_after if hasattr(exc, "retry_after") else None
        }
    )
    
    # Add RFC-compliant retry header when available
    if hasattr(exc, "retry_after"):
        response.headers["Retry-After"] = str(exc.retry_after)
    
    return response
