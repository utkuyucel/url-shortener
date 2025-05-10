# Rate Limiting in URL Shortener

This document explains how rate limiting is implemented in the URL Shortener application.

## Overview

The URL Shortener implements rate limiting to protect against abuse and ensure equitable resource distribution. The system uses `slowapi` with configurable backends, supporting both local development (in-memory) and production deployments (Redis).

## Architecture

Rate limiting is integrated into the existing architecture as follows:

1. **Configuration Layer**: Settings in `app/core/config.py`
2. **Rate Limiter Module**: Implementation in `app/core/rate_limiter.py`
3. **Application Middleware**: Applied in `main.py`
4. **Endpoint-specific Limits**: Defined in `app/routers/url.py`

## Configuration Options

Rate limiting is highly configurable through environment variables:

| Environment Variable | Description | Default |
|---------------------|-------------|---------|
| `RATE_LIMIT_ENABLED` | Enable/disable rate limiting | `true` |
| `RATE_LIMIT_STORAGE_URI` | Redis URI for distributed rate limiting | `null` (in-memory) |
| `RATE_LIMIT_DEFAULT_LIMITS__create_url` | Limit for URL creation endpoint | `30/minute` |
| `RATE_LIMIT_DEFAULT_LIMITS__redirect_url` | Limit for URL redirection endpoint | `100/minute` |
| `RATE_LIMIT_DEFAULT_LIMITS__general` | General fallback limit | `100/minute` |
| `RATE_LIMIT_KEY_PREFIX` | Prefix for rate limit keys in storage | `url_shortener_ratelimit` |

## Rate Limiting Strategies

Two rate limiting algorithms are available:

1. **Fixed Window** - Simple counter that resets at regular intervals
2. **Moving Window** - Tracks requests across a continuously sliding time period

## Storage Backends

Rate limit data can be stored in:

1. **Memory** - Fast but isolated to a single instance
2. **Redis** - Shared state across distributed deployments

## Headers

Rate limiting information is exposed through HTTP headers:

- `X-RateLimit-Limit`: Maximum requests per period
- `X-RateLimit-Remaining`: Requests remaining in the current period
- `X-RateLimit-Reset`: Time when the current limit window resets (Unix timestamp)
- `Retry-After`: Seconds to wait before making another request (only sent when rate limited)

## Error Response

When a client exceeds the rate limit, they receive a 429 Too Many Requests response with a JSON body:

```json
{
  "error": "Rate limit exceeded",
  "detail": "30 per 1 minute",
  "retry_after": 45
}
```

## Production Considerations

When deploying to production environments, consider the following:

- Adjust rate limits based on observed traffic patterns and user behavior
- Configure Redis storage for multi-instance deployments
- Set up monitoring for rate limit events to detect abuse patterns 
- Consider implementing IP allow/blocklists for known trusted/malicious clients

## Implementation Details

The current implementation:
- Uses client IP addresses as the default rate limiting key
- Provides standardized HTTP headers for limit information
- Configures endpoint-specific limits for critical operations
- Includes a custom response handler with useful debugging information
