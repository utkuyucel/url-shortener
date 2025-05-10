import time
from fastapi.testclient import TestClient
import pytest

from main import app
from app.core.config import settings


@pytest.fixture
def client():
    # Use a test client with temporary rate limiting settings
    app.state.limiter._storage.clear()  # Reset rate limit counters
    return TestClient(app)


def test_rate_limit_create_url(client):
    """Verify URL creation endpoint respects configured rate limits"""
    
    # Parse configured limit from settings
    limit_value = settings.rate_limit_default_limits["create_url"].split("/")[0]
    limit = int(limit_value)
    
    # Exhaust the rate limit
    for i in range(limit):
        response = client.post(
            "/urls",
            json={"original_url": f"https://example.com/{i}"}
        )
        assert response.status_code == 200
        # Verify rate limit headers are included
        assert "X-RateLimit-Limit" in response.headers or "X-RateLimit-Remaining" in response.headers
    
    # Attempt to exceed limit
    response = client.post(
        "/urls",
        json={"original_url": "https://example.com/over-limit"}
    )
    assert response.status_code == 429
    assert "Rate limit exceeded" in response.json()["error"]
    assert "Retry-After" in response.headers


def test_rate_limit_redirect(client):
    """Verify redirect endpoint enforces rate limits correctly"""
    
    # Create test URL for redirection testing
    create_response = client.post(
        "/urls",
        json={"original_url": "https://example.com/test-redirect"}
    )
    assert create_response.status_code == 200
    short_path = create_response.json()["key"]
    
    # Clear rate limiter between tests
    app.state.limiter._storage.clear()
    
    # Parse configured redirect limit
    limit_value = settings.rate_limit_default_limits["redirect_url"].split("/")[0]
    limit = int(limit_value)
    
    # Exhaust the redirect rate limit
    for _ in range(limit):
        response = client.get(f"/u/{short_path}", allow_redirects=False)
        assert response.status_code == 307  # Temporary redirect
    
    # Verify limit is enforced
    response = client.get(f"/u/{short_path}", allow_redirects=False)
    assert response.status_code == 429
    assert "Rate limit exceeded" in response.json()["error"]
